Name:           xorgxrdp
Version:        0.2.17
Release:        1%{?dist}
Summary:        Implementation of xrdp backend as Xorg modules

License:        MIT
URL:            https://github.com/neutrinolabs/xorgxrdp
Source0:        https://github.com/neutrinolabs/xorgxrdp/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: make
BuildRequires:  nasm
BuildRequires:  xorg-x11-server-devel
BuildRequires:  xrdp-devel >= 1:0.9.16
%if 0%{?fedora} > 0 && 0%{?fedora} <= 24
BuildRequires:  libXfont-devel
%else
BuildRequires:  libXfont2-devel
%endif
Requires:       Xorg %(xserver-sdk-abi-requires videodrv)
Requires:       Xorg %(xserver-sdk-abi-requires xinput)


%description
xorgxrdp is a set of X11 modules that make Xorg act as a backend for
xrdp. Xorg with xorgxrdp is the most advanced xrdp backend with support
for screen resizing and multiple monitors.

%prep
%autosetup -p1


%build
%configure
%make_build


%install
%make_install


%files
%license COPYING
%doc README.md
%dir %{_sysconfdir}/X11/xrdp
%{_sysconfdir}/X11/xrdp/xorg.conf
%{_libdir}/xorg/modules/drivers/xrdpdev_drv.so
%{_libdir}/xorg/modules/input/xrdpkeyb_drv.so
%{_libdir}/xorg/modules/input/xrdpmouse_drv.so
%{_libdir}/xorg/modules/libxorgxrdp.so
%exclude %{_libdir}/xorg/modules/*.a
%exclude %{_libdir}/xorg/modules/*.la
%exclude %{_libdir}/xorg/modules/input/*.a
%exclude %{_libdir}/xorg/modules/input/*.la
%exclude %{_libdir}/xorg/modules/drivers/*.a
%exclude %{_libdir}/xorg/modules/drivers/*.la


%changelog
* Tue Aug 31 2021 Bojan Smojver <bojan@rexursive.com> - 0.2.17-1
- Bump up to 0.2.17

* Sat Aug 21 2021 Carl George <carl@george.computer> - 0.2.16-3
- Use xserver-sdk-abi-requires to require xserver ABI versions

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May  1 2021 Bojan Smojver <bojan@rexursive.com> - 0.2.16-1
- Bump up to 0.2.16

* Wed Apr 14 2021 Bojan Smojver <bojan@rexursive.com> - 0.2.15-2
- Rebuild against xorg-x11-server 1.20.11

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 23 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.15-1
- Bump up to 0.2.15

* Thu Dec  3 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.14-4
- Rebuild against xorg-x11-server 1.20.10

* Mon Oct 12 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.14-3
- Rebuild against xorg-x11-server 1.20.9

* Tue Sep  1 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.14-2
- Enable s390x

* Tue Sep  1 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.14-1
- Bump up to 0.2.14

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 16 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.13-2
- Rebuild against Xorg 1.20.8

* Wed Mar 11 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.13-1
- Bump up to 0.2.13

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan  4 2020 Bojan Smojver <bojan@rexursive.com> - 0.2.12-2
- Revert 228e9091af79a76819292467f17ad1ad7c6483c3 (#153) upstream
- Bug #1787612

* Wed Dec 11 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.12-1
- Bump up to 0.2.12

* Tue Nov 26 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.11-2
- Rebuild against Xorg 1.20.6

* Fri Aug 16 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.11-1
- Bump up to 0.2.11

* Sat Aug 10 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.10-4
- Add RHEL8/EPEL8 conditional.

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.10-2
- Rebuild against Xorg 1.20.5

* Thu May 30 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.10-1
- Bump up to 0.2.10

* Fri Mar  1 2019 Bojan Smojver <bojan@rexursive.com> - 0.2.9-3
- Rebuild against Xorg 1.20.4

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Dec 22 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.9-1
- Bump up to 0.2.9

* Fri Nov  2 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.8-3
- Rebuild against Xorg 1.20.3

* Thu Oct 25 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.8-2
- Rebuild against Xorg 1.20.2

* Wed Sep 19 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.8-1
- Bump up to 0.2.8

* Thu Sep  6 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.7-3
- Rebuild against Xorg 1.20.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.7-1
- Bump up to 0.2.7

* Thu May 17 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.6-3
- Rebuild against Xorg 1.20.0 from F29

* Wed Apr 11 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.6-2
- Rebuild against Xorg 1.19.5 from RHEL 7.5

* Sun Mar 25 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.6-1
- Bump up to 0.2.6

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 15 2018 Bojan Smojver <bojan@rexursive.com> - 0.2.5-3
- Add patch for gnome-settings-daemon crash

* Fri Dec 22 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.5-2
- Bump and rebuild against latest xorg-x11-server

* Sat Dec 16 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.5-1
- Bump up to 0.2.5

* Fri Oct 13 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.4-5
- Bump and rebuild against latest xorg-x11-server

* Sat Oct  7 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.4-4
- Bump and rebuild against latest xorg-x11-server

* Sat Sep 23 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.4-3
- Require xorg-x11-server-Xorg we built against

* Wed Sep 20 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.4-2
- Require libXfont2-devel on RHEL7 at build time

* Wed Sep 20 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.4-1
- Bump up to 0.2.4

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.3-1
- Bump up to 0.2.3

* Thu Jun 22 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.2-1
- Bump up to 0.2.2

* Thu Mar 30 2017 Bojan Smojver <bojan@rexursive.com> - 0.2.1-1
- Bump up to 0.2.1

* Thu Mar  9 2017 Pavel Roskin <plroskin@gmail.com> - 0.2.0-2
- Add build dependency on libXfont2-devel for f24

* Sun Mar  5 2017 Pavel Roskin <plroskin@gmail.com> - 0.2.0-1
- Package created
