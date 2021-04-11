%global _hardened_build 1

%global selinux_types %(%{__awk} '/^#[[:space:]]*SELINUXTYPE=/,/^[^#]/ { if ($3 == "-") printf "%s ", $2 }' /etc/selinux/config 2>/dev/null)
%global selinux_variants %([ -z "%{selinux_types}" ] && echo mls targeted || echo %{selinux_types})

%if 0%{?fedora} >= 31
%global _hardlink /usr/bin/hardlink
%else
%global _hardlink /usr/sbin/hardlink
%endif

Summary:   Open source remote desktop protocol (RDP) server
Name:      xrdp
Epoch:     1
Version:   0.9.15
Release:   3a%{?dist}
License:   ASL 2.0 and GPLv2+ and MIT
URL:       http://www.xrdp.org/
Source0:   https://github.com/neutrinolabs/xrdp/releases/download/v%{version}/xrdp-%{version}.tar.gz
Source1:   xrdp-sesman.pamd
Source2:   xrdp.sysconfig
Source3:   xrdp.logrotate
Source4:   openssl.conf
Source5:   README.Fedora
Source6:   xrdp.te
Source7:   xrdp-polkit-1.rules
Patch0:    xrdp-0.9.9-sesman.patch
Patch1:    xrdp-0.9.14-xrdp-ini.patch
Patch2:    xrdp-0.9.4-service.patch
Patch3:    xrdp-0.9.10-scripts-libexec.patch
Patch4:    xrdp-0.9.6-script-interpreter.patch
Patch5:    xrdp-0.9.15-arch.patch
Patch6:    xrdp-0.9.14-vnc-uninit.patch
%if 0%{?fedora} >= 32 || 0%{?rhel} >= 8
Patch7:    xrdp-0.9.15-sesman-ini.patch
%endif
Patch8:    dynamic-link.patch

BuildRequires: gcc
BuildRequires: libX11-devel
BuildRequires: libXfixes-devel
BuildRequires: libXrandr-devel
BuildRequires: openssl
BuildRequires: pam-devel
BuildRequires: pkgconfig(fuse)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(pixman-1)
BuildRequires: pkgconfig(systemd)
BuildRequires: nasm

BuildRequires: checkpolicy, selinux-policy-devel
BuildRequires: %{_hardlink}

# tigervnc-server-minimal provides Xvnc (default for now)
# xorgxrdp is another back end, depends on specific Xorg binary, omit
#Requires: tigervnc-server-minimal
#Requires: xorg-x11-xinit
#Requires: util-linux

%if 0%{?fedora} || 0%{?rhel} >= 8
Recommends: %{name}-selinux = %{epoch}:%{version}-%{release}
%endif

Requires(post): systemd
Requires(post): systemd-sysv
Requires(post): /sbin/ldconfig
Requires(posttrans): openssl
Requires(preun): systemd
Requires(posttrans): systemd


%package devel
Summary: Headers and pkg-config files needed to compile xrdp backends

%description
xrdp provides a fully functional RDP server compatible with a wide range
of RDP clients, including FreeRDP and Microsoft RDP client.

%description devel
This package contains headers necessary for developing xrdp backends that
talk to xrdp.

%package selinux
Summary: SELinux policy module required tu run xrdp

Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: selinux-policy >= %{_selinux_policy_version}
Requires(post): /usr/sbin/semodule
Requires(postun): /usr/sbin/semodule

%description selinux
This package contains SELinux policy module necessary to run xrdp.

%package neutrinordp
Summary: RDP Proxy module for xrdp

Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: NeutrinoRDP-libs

%description neutrinordp
This package contains RDP Proxy module for xrdp (neutrinordp-any)

%prep
%autosetup -p1
%{__cp} %{SOURCE5} .

# SELinux policy module
%{__mkdir} SELinux
%{__cp} -p %{SOURCE6} SELinux

# create 'bash -l' based startwm, to pick up PATH etc.
echo '#!/bin/bash -l
. %{_libexecdir}/xrdp/startwm.sh' > sesman/startwm-bash.sh

%build
./bootstrap
%configure --enable-fuse --enable-pixman --enable-painter --enable-vsock \
           --enable-neutrinordp --enable-jpeg --enable-tjpeg \
           --with-socketdir=%{_rundir}/%{name}
%make_build

# SELinux policy module
cd SELinux
for selinuxvariant in %{selinux_variants}
do
  %{__make} NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile
  %{__mv} %{name}.pp %{name}.pp.${selinuxvariant}
  %{__make} NAME=${selinuxvariant} -f /usr/share/selinux/devel/Makefile clean
done
cd -

%install
%make_install

#install sesman pam config /etc/pam.d/xrdp-sesman
%{__install} -Dp -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/xrdp-sesman

#install xrdp sysconfig /etc/sysconfig/xrdp
%{__install} -Dp -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/xrdp

#install logrotate /etc/logrotate.d/xrdp
%{__install} -Dp -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/xrdp

#install openssl.conf /etc/xrdp
%{__install} -Dp -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/xrdp/openssl.conf

#install 'bash -l' startwm script
%{__install} -Dp -m 755 sesman/startwm-bash.sh %{buildroot}%{_libexecdir}/xrdp/startwm-bash.sh

#move startwm and reconnectwm scripts to libexec
%{__mv} -f %{buildroot}%{_sysconfdir}/xrdp/startwm.sh %{buildroot}%{_libexecdir}/xrdp/
%{__mv} -f %{buildroot}%{_sysconfdir}/xrdp/reconnectwm.sh %{buildroot}%{_libexecdir}/xrdp/

#install xrdp.rules /usr/share/polkit-1/rules.d
%{__install} -Dp -m 644 %{SOURCE7} %{buildroot}%{_datadir}/polkit-1/rules.d/xrdp.rules

# SELinux policy module
for selinuxvariant in %{selinux_variants}
do
  %{__install} -d %{buildroot}%{_datadir}/selinux/${selinuxvariant}
  %{__install} -p -m 644 SELinux/%{name}.pp.${selinuxvariant} \
               %{buildroot}%{_datadir}/selinux/${selinuxvariant}/%{name}.pp
done
%{_hardlink} -cv %{buildroot}%{_datadir}/selinux

%post
%{?ldconfig}
%systemd_post xrdp.service

%preun
%systemd_preun xrdp.service
if [ $1 -eq 0 ]; then
  # Stop services on package removal (see bug 1349083)
  systemctl stop xrdp.service > /dev/null 2>&1 || :
fi

%triggerun -- xrdp < 0.6.0-1
systemd-sysv-convert --save xrdp >/dev/null 2>&1 ||:

# If the package is allowed to autostart:
systemctl preset xrdp.service >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del xrdp >/dev/null 2>&1 || :
if [ "`systemctl is-active xrdp.service`" = 'active' ]; then
    systemctl stop xrdp.service >/dev/null 2>&1 || :
    systemctl start xrdp.service >/dev/null 2>&1 || :
fi

%ldconfig_postun

%posttrans
if [ ! -s %{_sysconfdir}/xrdp/rsakeys.ini ]; then
  (umask 377; touch %{_sysconfdir}/xrdp/rsakeys.ini; %{_bindir}/xrdp-keygen xrdp %{_sysconfdir}/xrdp/rsakeys.ini &>/dev/null)
fi

if [ ! -s %{_sysconfdir}/xrdp/cert.pem ]; then
  (umask 377; openssl req -x509 -newkey rsa:2048 -sha256 -nodes -days 3652 \
    -keyout %{_sysconfdir}/xrdp/key.pem \
    -out %{_sysconfdir}/xrdp/cert.pem \
    -config %{_sysconfdir}/xrdp/openssl.conf >/dev/null 2>&1)
fi

%post selinux
for selinuxvariant in %{selinux_variants}
do
  /usr/sbin/semodule -s ${selinuxvariant} -i \
    %{_datadir}/selinux/${selinuxvariant}/%{name}.pp &> /dev/null || :
done

%postun selinux
if [ $1 -eq 0 ] ; then
  for selinuxvariant in %{selinux_variants}
  do
    /usr/sbin/semodule -s ${selinuxvariant} -r %{name} &> /dev/null || :
  done
fi


%files
%doc COPYING *.txt README.Fedora
%dir %{_libdir}/xrdp
%dir %{_sysconfdir}/xrdp
%dir %{_sysconfdir}/xrdp/pulse
%dir %{_datadir}/xrdp
%dir %{_libexecdir}/xrdp
%config(noreplace) %{_sysconfdir}/xrdp/xrdp.ini
%config(noreplace) %{_sysconfdir}/pam.d/xrdp-sesman
%config(noreplace) %{_sysconfdir}/logrotate.d/xrdp
%config(noreplace) %{_sysconfdir}/sysconfig/xrdp
%config(noreplace) %{_sysconfdir}/xrdp/sesman.ini
%config(noreplace) %{_sysconfdir}/xrdp/km*.ini
%config(noreplace) %{_sysconfdir}/xrdp/openssl.conf
%config(noreplace) %{_sysconfdir}/xrdp/xrdp_keyboard.ini
%config(noreplace) %{_sysconfdir}/xrdp/pulse/default.pa
%exclude %ghost %{_sysconfdir}/xrdp/*.pem
%exclude %ghost %{_sysconfdir}/xrdp/rsakeys.ini
%{_libexecdir}/xrdp/startwm*.sh
%{_libexecdir}/xrdp/reconnectwm.sh
%{_bindir}/xrdp-genkeymap
%{_bindir}/xrdp-sesadmin
%{_bindir}/xrdp-keygen
%{_bindir}/xrdp-sesrun
%{_bindir}/xrdp-dis
%{_sbindir}/xrdp-chansrv
%{_sbindir}/xrdp
%{_sbindir}/xrdp-sesman
%{_datadir}/xrdp/ad256.bmp
%{_datadir}/xrdp/cursor0.cur
%{_datadir}/xrdp/cursor1.cur
%{_datadir}/xrdp/xrdp256.bmp
%{_datadir}/xrdp/sans-10.fv1
%{_datadir}/xrdp/ad24b.bmp
%{_datadir}/xrdp/xrdp24b.bmp
%{_datadir}/xrdp/xrdp_logo.bmp
%{_datadir}/polkit-1/rules.d/xrdp.rules
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_mandir}/man1/*
%{_libdir}/lib*.so.*
%exclude %{_libdir}/librfxencode.so
%{_libdir}/xrdp/lib*.so.*
%exclude %{_libdir}/xrdp/libcommon.so
%{_libdir}/xrdp/libmc.so
%exclude %{_libdir}/xrdp/libscp.so
%{_libdir}/xrdp/libvnc.so
%exclude %{_libdir}/xrdp/libxrdp.so
%{_libdir}/xrdp/libxup.so
%exclude %{_libdir}/xrdp/libxrdpapi.so
%{_unitdir}/xrdp-sesman.service
%{_unitdir}/xrdp.service
%exclude %{_includedir}/painter.h
%exclude %{_libdir}/libpainter.*
%exclude %{_libdir}/pkgconfig/libpainter.pc
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%exclude %{_libdir}/xrdp/*.a
%exclude %{_libdir}/xrdp/*.la
%ghost %{_localstatedir}/log/xrdp.log
%ghost %{_localstatedir}/log/xrdp-sesman.log
#%{_libdir}/xrdp/libxrdpneutrinordp.so

%files devel
%{_includedir}/ms-*
%{_includedir}/xrdp*
%{_includedir}/rfxcodec_*.h
%{_libdir}/pkgconfig/xrdp.pc
%{_libdir}/pkgconfig/rfxcodec.pc

%files selinux
%doc SELinux/%{name}.te
%{_datadir}/selinux/*/%{name}.pp

%files neutrinordp
%{_libdir}/xrdp/libxrdpneutrinordp.so


%changelog
* Sat Jan  2 2021 Bojan Smojver <bojan@rexurive.com> - 1:0.9.15-3
- Remove setpriv patch and adjust SELinux policy to match

* Fri Jan  1 2021 Bojan Smojver <bojan@rexurive.com> - 1:0.9.15-2
- Use /usr/libexec/Xorg or Xorg session of Fedora and RHEL8+

* Tue Dec 29 2020 Bojan Smojver <bojan@rexurive.com> - 1:0.9.15-1
- Bump up to 0.9.15

* Tue Sep  1 2020 Bojan Smojver <bojan@rexurive.com> - 1:0.9.14-3
- Add a patch for uninitialised variables, courtesy of Dan Horák

* Mon Aug 31 2020 Bojan Smojver <bojan@rexurive.com> - 1:0.9.14-2
- Bump up to 0.9.14
- Add a set of patches to deal with new GCC warnings/errors
- Do not emit warning on failed architecture detection
- Exclude s390x arch for now

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.13.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Bojan Smojver <bojan@rexurive.com> - 1:0.9.13.1-1
- Bump up to 0.9.13.1
- CVE-2022-4044

* Thu May 14 2020 Bojan Smojver <bojan@rexurive.com> - 1:0.9.13-2
- Move sockets to /run/xrdp, bug #1834178

* Wed Mar 11 2020 Bojan Smojver <bojan@rexurive.com> - 1:0.9.13-1
- Bump up to 0.9.13

* Sat Feb 22 2020 Bojan Smojver <bojan@rexursive.com> - 1:0.9.12-6
- patch a segfault
- issue #1487 and #1501, pointed out by oden dot eriksson at vattenfall dot com

* Thu Feb 20 2020 Tom Callaway <spot@fedoraproject.org> - 1:0.9.12-5
- fix license tag (bz1804932)

* Thu Jan 30 2020 Bojan Smojver <bojan@rexurive.com> - 1:0.9.12-4
- README.Fedora: VSOCK support
- README.Fedora: possibly incorrect SELinux context of the sessions
- Add polkit-1 rules for colord access and repo refresh

* Mon Jan 13 2020 Bojan Smojver <bojan@rexurive.com> - 1:0.9.12-3
- Add vsock items to SELinux policy (thanks to mm19827 of gmail.com)

* Sun Jan 12 2020 Bojan Smojver <bojan@rexurive.com> - 1:0.9.12-2
- Enable vsock (bug #1787953)

* Sun Dec 29 2019 Bojan Smojver <bojan@rexurive.com> - 1:0.9.12-1
- Bump up to 0.9.12

* Mon Sep 23 2019 Bojan Smojver <bojan@rexurive.com> - 1:0.9.11-5
- Make xrdp-selinux a weak dependency on versions that support them.
- Drop xrdp-selinux dependency completely.

* Sun Sep 15 2019 Bojan Smojver <bojan@rexurive.com> - 1:0.9.11-3
- Decouple xrdp from xorgxrdp, causing repeated installation issues in RHEL.

* Tue Aug 27 2019 Bojan Smojver <bojan@rexurive.com> - 1:0.9.11-2
- Increment release for rebuild in F31.

* Thu Aug 22 2019 Bojan Smojver <bojan@rexurive.com> - 1:0.9.11-1
- Bump up to 0.9.11

* Sat Aug 10 2019 Bojan Smojver <bojan@rexurive.com> - 1:0.9.10-3
- Make sure rsakeys.ini exists (bug #1739176).

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May  3 2019 Bojan Smojver <bojan@rexurive.com> - 1:0.9.10-1
- Bump up to 0.9.10

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 11 2019 Bojan Smojver <bojan@rexurive.com> - 1:0.9.9-1
- Bump up to 0.9.9
- Fix sesman.ini patch
- Fix xrdp.ini patch

* Wed Nov 14 2018 Bojan Smojver <bojan@rexurive.com> - 1:0.9.8-2
- Make main and selinux packages codependent

* Wed Sep 26 2018 Bojan Smojver <bojan@rexurive.com> - 1:0.9.8-1
- Bump up to 0.9.8

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul  4 2018 Bojan Smojver <bojan@rexurive.com> - 1:0.9.7-1
- Bump up to 0.9.7

* Mon Apr 23 2018 Bojan Smojver <bojan@rexurive.com> - 1:0.9.6-4
- mark files in /etc/xrdp/pulse as configs
- add null command on postun, so that it is never empty

* Mon Apr 23 2018 Bojan Smojver <bojan@rexurive.com> - 1:0.9.6-3
- mark files in /etc/xrdp as configs
- run ldconfig
- remove chmod of certs/keys
- fix script interpreter

* Sun Apr 22 2018 Bojan Smojver <bojan@rexurive.com> - 1:0.9.6-2
- Allow oddjob-mkhomedir in SELinux policy (stolen from grishin-a)
- Allow no new privileges transition in SELinux policy

* Tue Mar 27 2018 Bojan Smojver <bojan@rexurive.com> - 1:0.9.6-1
- Bump up to 0.9.6

* Fri Mar  9 2018 Bojan Smojver <bojan@rexurive.com> - 1:0.9.5-2
- add gcc build requirement

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:0.9.5-2
- Escape macros in %%changelog

* Sat Dec 30 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.5-1
- Bump up to 0.9.5

* Fri Nov 24 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.4-2
- Patch CVE-2017-16927

* Fri Oct  6 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.4-1
- Bump up to 0.9.4

* Tue Sep 19 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.3-2
- Add patch to clean up sockets

* Thu Aug 10 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.3-1
- Bump up to 0.9.3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu May 18 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.2-12
- Document problems/workaround with clipboard support in TigerVNC 1.8.0

* Thu May 18 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.2-11
- Add a patch that allows equal signs in ini file values

* Thu Apr 13 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.2-10
- Use epoch in version dependency
- Provide selinux sub-package scriptlets

* Thu Apr 13 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.2-9
- Adjust Fedora README file for SELinux changes

* Wed Apr 12 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.2-8
- Add SELinux policy sub-package

* Tue Apr 11 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.2-7
- Own /usr/libexec/xrdp directory

* Tue Apr 11 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.2-6
- Move scripts to /usr/libexec/xrdp, so that they get labelled as bin_t

* Sat Apr  8 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.2-5
- Rework call to Xorg to use setpriv instead, properly

* Fri Apr  7 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.2-4
- Do not call prctl() from xrdp, use setpriv instead

* Tue Apr  4 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.2-3
- Do not attempt xrdp restarts, may cause dnf transaction problems
- Stop depending on Xorg server, xorgxrdp already does
- Add README.Fedora

* Mon Apr  3 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.2-2
- Stop using /usr/libexec/Xorg, not present on EL7

* Fri Mar 31 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.2-1
- Bump up to 0.9.2

* Tue Mar 14 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.1-8
- Require tigervnc-server-minimal again, make it default
- Comment out references to X11rdp

* Fri Mar 10 2017 Pavel Roskin <plroskin@gmail.com> - 1:0.9.1-7
- Require /etc/X11/xinit/Xsession, it's called from startwm.sh
- Call xrdp-keygen with full path in %%posttrans
- Exclude *.so files for non-modules

* Thu Mar 09 2017 Pavel Roskin <plroskin@gmail.com> - 1:0.9.1-6
- Make xrdp depend on xorgxrdp, not on tigervnc-server-minimal
- Make Xorg backend default
- Call /usr/libexec/Xorg directly to avoid permission checks

* Tue Feb 21 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.1-5
- Require openssl in posttrans phase
- Move conditional restart to posttrans phase

* Mon Feb 20 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.1-4
- Move key/cert generation to posttrans stage

* Thu Feb 16 2017 Bojan Smojver <bojan@rexurive.com> - 1:0.9.1-3
- Fix log file rotation

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Feb 07 2017 Pavel Roskin <plroskin@gmail.com> - 1:0.9.1-2
- Enable hardened build

* Tue Jan 24 2017 Pavel Roskin <plroskin@gmail.com> - 1:0.9.1-1
- Split out xrdp-devel
- Generate certificate for TLS authentication on package install
- Add fastpath hotfix
- Fix stopping services on package uninstall
- Use packaged pixman library
- Enable libpainter for compatibility with "noorders" clients
- Upgrade to 0.9.1

* Sun Mar 13 2016 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1:0.9.0-6
- enable fuse for drive redirection or clipboard file transfer

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 20 2015 Bojan Smojver <bojan@rexursive.com> - 1:0.9.0-4
- own /etc/xrdp/pulse directory

* Fri Jul 17 2015 Bojan Smojver <bojan@rexursive.com> - 1:0.9.0-3
- service files fixes and dependencies
- sesman default configuration

* Wed Jul 15 2015 Dan Horák <dan[at]danny.cz> - 1:0.9.0-2
- install epoch back to keep clean upgrade path

* Tue Jul 14 2015 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.9.0-1
- upgrade to 0.9.0

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.6.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun  4 2015 Bojan Smojver <bojan@rexursive.com> - 1:0.6.1-10
- remove -ac from X server calls: bug #1105202
- put other sesman.ini changes into a patch

* Fri May 15 2015 Bojan Smojver <bojan@rexursive.com> - 1:0.6.1-9
- hopefully better service dependencies

* Thu Apr 23 2015 Dan Horák <dan[at]danny.cz> - 1:0.6.1-8
- fix upgrade path after the 0.8 bump in 2014-09 by adding Epoch

* Mon Dec 22 2014 Bojan Smojver <bojan@rexursive.com> - 0.6.1-7
- add a delay loop when connecting to VNC back end

* Mon Dec  8 2014 Bojan Smojver <bojan@rexursive.com> - 0.6.1-6
- use systemd rpm macros: bug #850374

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 0.6.1-5
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr  1 2014 Bojan Smojver <bojan@rexursive.com> - 0.6.1-2
- try a bump to official 0.6.1
- provide format for syslog() call
- fix memset() call
- fix implicit declarations

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-0.8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jan 29 2013 Dan Horák <dan[at]danny.cz> - 0.6.0-0.7
- fix check for big endian arches (#905411)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 28 2012 Bojan Smojver <bojan@rexursive.com> - 0.6.0-0.5
- bind xrdp-sesman.service to xrdp.service, so that restarts work
- do not use forking style, but run services in the foreground instead
- dispense with ExecStop, systemd will do that for us

* Sat May 26 2012 Bojan Smojver <bojan@rexursive.com> - 0.6.0-0.4
- do explicit stop/start in order to get xrdp-sesman.service up too

* Sat May 26 2012 Bojan Smojver <bojan@rexursive.com> - 0.6.0-0.3
- also attempt to restart xrdp-sesman.service (just xrdp.service won't do it)
- stop xrdp-sesman.service when not needed by xrdp.service

* Fri May 25 2012 Bojan Smojver <bojan@rexursive.com> - 0.6.0-0.2
- bump release for rebuild with the correct e-mail address

* Fri May 25 2012 Bojan Smojver <bojan@rexursive.com> - 0.6.0-0.1
- more work on systemd support
- remove xrdp-dis for now, current HEAD is broken (explicit rpaths)

* Wed May 23 2012 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.6.0-0.1
- include patch's from Bojan Smojver bz#821569 , bz#611669

* Sat Feb 04 2012 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.16
- add support for systemd

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-0.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 18 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.13
- up to git tag a9cfc235211a49c69c3cce3f98ee5976ff8103a4

* Thu Nov 18 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.12.03172010
- fix logrotate to not restart xrdp and drop all open connections

* Mon Oct 04 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.11.03172010
- Load a default keymap when current keymap doesnt exist

* Thu Jul 08 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.10.03172010
- fix rhbz #611669 (load environment variables)

* Thu Mar 18 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.9.03172010
- buildrequires libXfixes-devel

* Thu Mar 18 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.8.03172010
- buildrequires libX11-devel

* Thu Mar 18 2010 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.7.03172010
- sync with last xrdp cvs

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 0.5.0-0.6.20090811cvs
- use password-auth instead of system-auth

* Tue Sep 08 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.5.20090811cvs
- fix xrdp-sesman pam.d to uses system-auth

* Fri Sep 04 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.4.20090811cvs
- increase encryption to 128 bit's
- include system-auth into /etc/pam.d/xrdp-sesman

* Wed Aug 26 2009 Tomas Mraz <tmraz@redhat.com> - 0.5.0-0.3.20090811cvs
- rebuild with new openssl

* Thu Aug 13 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.2.20090811cvs
- more changes to spec file https://bugzilla.redhat.com/show_bug.cgi?id=516364#c10

* Wed Aug 12 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-0.1.20090811cvs
- change versioning schema
- improve initscript
- fix some macros


* Tue Aug 11 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 0.5.0-2.20090811cvs
- changes from BZ#516364 comment 2 from Mamoru Tasaka
- changed license to "GPLv2+ with exceptions"
- dropped -libs subpackage
- use cvs version
- remove a patch and use sed instead
- remove attr's

* Thu Apr 02 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> 0.5.0-1
- Initial RPM release
