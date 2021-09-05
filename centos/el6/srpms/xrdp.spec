%define	xrdpver		0.9.17
%define	xrdpbranch	v0.9

%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
%global with_systemd 1
%else
%global with_systemd 0
%endif

Summary:	Open source Remote Desktop Protocol (RDP) server
Name:		xrdp
Version:	%{xrdpver}
License:	ASL 2.0
Release:	1%{?dist}
URL:		http://www.xrdp.org/
Source0:	xrdp-0.9.17.tar.gz
Source1:	xrdp.init
Source2:	xrdp.sysconfig
Source3:	xrdp.logrotate
# Patch0:		xrdp-0.9.16-neutrinordp.patch

# Basic dependensies
BuildRequires:	autoconf268
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	openssl
BuildRequires:	openssl-devel
BuildRequires:	pam-devel
BuildRequires:	libX11-devel
BuildRequires:	libXfixes-devel
BuildRequires:	libXrandr-devel
BuildRequires:	which
BuildRequires:	make
BuildRequires:	nasm
# Additional dependencies which vary on depending on build options
BuildRequires:	libjpeg-turbo-devel fuse-devel
# Runtime dependencies
Requires:	fuse

BuildRoot:	%{_tmppath}/%{name}-%{version}-root

# initscripts is required for /sbin/service
%if 0%{?with_systemd}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires(post): chkconfig initscripts
Requires(preun): chkconfig initscripts
Requires(postun): initscripts
%endif

%description
RDP server for Linux

%prep
%setup -q -n xrdp-%{xrdpver}
# %patch0 -p 2

%build
if [ -d libpainter ]; then
	(cd libpainter && ./bootstrap && %configure && %{__make})
fi
if [ -f librfxcodec/bootstrap ]; then
	(cd librfxcodec && ./bootstrap && %configure && %{__make})
elif [ -f librfxcodec/Makefile ]; then
	%{__make} -C librfxcodec
fi
./bootstrap
%configure \
	--enable-fuse --enable-jpeg --enable-tjpeg --enable-neutrinordp --disable-static \
        --enable-pixman --enable-painter
%{__make}

%install
%{__make} install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete
# workaround to support after 1fe368c5b3fa05f287731e57d748afb4556d554f and before
%{__mkdir} -p %{buildroot}%{_includedir}
if [ ! -f %{buildroot}%{_includedir}/xrdp_client_info.h ]; then
%{__install} -c -m 644 common/xrdp_{client_info,constants,rail}.h %{buildroot}%{_includedir}
fi
#install xrdp initscript /etc/rc.d/init.d/xrdp
%if !%{with_systemd}
%{__install} -Dp -m 755 %{SOURCE1} %{buildroot}%{_initddir}/xrdp
%endif
#install xrdp sysconfig /etc/sysconfig/xrdp
%{__install} -Dp -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/xrdp
#install logrotate /etc/logrotate.d/xrdp
%{__install} -Dp -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/xrdp
# delete files installed for debian
%{__rm} -rf %{buildroot}/etc/init.d %{buildroot}/etc/default
# delete keys, certificates
%{__rm} -f %{buildroot}%{_sysconfdir}/xrdp/rsakeys.ini
%{__rm} -f %{buildroot}%{_sysconfdir}/xrdp/cert.pem
%{__rm} -f %{buildroot}%{_sysconfdir}/xrdp/key.pem

%post
# generate RSA key pair
if [ ! -s %{_sysconfdir}/xrdp/rsakeys.ini ]; then
    umask 077 && %{_bindir}/xrdp-keygen xrdp %{_sysconfdir}/xrdp/rsakeys.ini 2048 >/dev/null
fi
# generate certificate
if [ ! -f %{_sysconfdir}/xrdp/cert.pem -a ! -f %{_sysconfdir}/xrdp/key.pem ]; then
    openssl req -x509 \
      -newkey rsa:2048 -nodes -sha256 \
      -keyout %{_sysconfdir}/xrdp/key.pem \
      -out %{_sysconfdir}/xrdp/cert.pem \
      -days 365 -subj /CN=$(hostname)
fi
%if 0%{?with_systemd}
%systemd_post xrdp.service xrdp-sesman.service
%else
# This adds the proper /etc/rc*.d links for the script
if [ "$1" -eq "1" ]; then
    /sbin/chkconfig --add %{name}
fi
%endif
# workaround for Red Hat Bug 1177202
# https://bugzilla.redhat.com/show_bug.cgi?id=1177202
/usr/bin/chcon -t bin_t %{_sbindir}/xrdp %{_sbindir}/xrdp-sesman

%preun
%if 0%{?with_systemd}
%systemd_preun xrdp.service xrdp-sesman.service
%else
if [ "$1" -eq "0" ] ; then
    /sbin/chkconfig --del %{name}
fi
%endif

%postun
%if 0%{?with_systemd}
%systemd_postun_with_restart xrdp.service xrdp-sesman.service
%else
if [ "$1" -ge "1" ] ; then
    /sbin/service %{name} condrestart >/dev/null 2>&1 || :
fi
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING *.txt
%dir %{_libdir}/xrdp
%dir %{_datadir}/xrdp
%dir %{_sysconfdir}/xrdp
%dir %{_sysconfdir}/xrdp/pulse
%config(noreplace) %{_sysconfdir}/xrdp/sesman.ini
%config(noreplace) %{_sysconfdir}/xrdp/xrdp.ini
%config(noreplace) %{_sysconfdir}/xrdp/xrdp_keyboard.ini
%config(noreplace) %{_sysconfdir}/pam.d/xrdp-sesman
%config(noreplace) %{_sysconfdir}/logrotate.d/xrdp
%config(noreplace) %{_sysconfdir}/sysconfig/xrdp
%config(noreplace) %{_sysconfdir}/xrdp/pulse/*
%config(noreplace) %{_sysconfdir}/xrdp/km-*.ini
%{_sysconfdir}/xrdp/*.sh
%{_libdir}/xrdp/*
# devel: pkgconfig files
%{_libdir}/*
%{_datadir}/xrdp/*
%{_sbindir}/*
%{_bindir}/*
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%if 0%{?with_systemd}
%{_unitdir}/xrdp-sesman.service
%{_unitdir}/xrdp.service
%else
%{_initrddir}/*
%endif

%changelog
* Sun Sep 05 2021 TOMATO <junker.tomato@gmaill.com> - 0.9.17-1
- Bump up to 0.9.17

* Sun May 16 2021 TOMATO <junker.tomato@gmaill.com> - 0.9.16-1
- NeutrinoRDP Proxy logging patch #1875 

* Tue May 26 2020 TOMATO <junker.tomato@gmaill.com> - 0.9.16-0
- Initial build for xrdp version 0.9.16
