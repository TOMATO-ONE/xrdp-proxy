%global debug_package %{nil}
# cmake
# make package_source
%define gittag 836b738ae3739c275ed9b3eedb7d581067911b70
%define gittag_s 836b738
%define _unpackaged_files_terminate_build 0

Summary: NeutrinoRDP RDP Client fork from FreeRDP 1.0.1
Name: neutrinordp
Version: git%{gittag_s}
Release: 1%{?dist}
License: Apache License 2.0
Group: Applications/Communications
URL: https://github.com/neutrinolabs/NeutrinoRDP
Source: https://github.com/neutrinolabs/NeutrinoRDP/archive/%{gittag}.tar.gz#/neutrinolabs-neutrinordp-%{gittag_s}.tar.gz
Patch0: CMakeLists.txt.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  openssl-devel
BuildRequires:	libX11-devel, libXcursor-devel, libXext-devel, libXinerama-devel, libXdamage-devel, libXv-devel, libxkbfile-devel
BuildRequires:	cups-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	pcsc-lite-devel
Conflicts:	freerdp1.2	
BuildConflicts:	freerdp1.2-devel

%description
NeutrinoRDP is a free implementation of the Remote Desktop Protocol (RDP)
according to the Microsoft Open Specifications.
This is a fork of FreeRDP 1.0.1.

%package xfreerdp
Summary: Remote Desktop Protocol client
Group: Applications/Communications
Requires: %{name}-libs = %{version}-%{release}, %{name}-plugins-standard = %{version}-%{release}
%description xfreerdp
xfreerdp is a free implementation of the Remote Desktop Protocol (RDP)
according to the Microsoft Open Specifications.
This is a fork of FreeRDP 1.0.1.

%package libs
Summary: Core libraries implementing the RDP protocol
Group: Applications/Communications
%description libs
libfreerdp-core can be embedded in applications.

libfreerdp-channels and libfreerdp-kbd might be convenient to use in X
applications together with libfreerdp-core.

libfreerdp-core can be extended with plugins handling RDP channels.

%package plugins-standard
Summary: Plugins for handling the standard RDP channels
Group: Applications/Communications
Requires: %{name}-libs = %{version}-%{release}
%description plugins-standard
A set of plugins to the channel manager implementing the standard virtual
channels extending RDP core functionality. For instance, sounds, clipboard
sync, disk/printer redirection, etc.

%package devel
Summary: Libraries and header files for embedding and extending freerdp
Group: Applications/Communications
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig
%description devel
Header files and unversioned libraries for libfreerdp-core, libfreerdp-channels,
libfreerdp-kbd, libfreerdp-cache, libfreerdp-codec, libfreerdp-rail,
libfreerdp-gdi and libfreerdp-utils.

%prep
%setup -n %{name}-%{gittag}
%patch0 

%build
cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_INSTALL_LIBDIR=lib64 -DWITH_ALSA=OFF -DWITH_CUPS=OFF -DWITH_JPEG=ON -DWITH_PCSC=OFF -DWITH_SERVER=OFF -DWITH_X11=ON -DWITH_XCURSOR=ON -DWITH_XEXT=ON -DWITH_XKBFILE=ON -DWITH_XINERAMA=ON -DWITH_XV=ON -DWITH_NEON=OFF -DWITH_SSE2=ON .

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/{freerdp/,lib}*.{a,la} # FIXME: They shouldn't be installed in the first place

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files xfreerdp
%defattr(-,root,root)
%{_bindir}/xfreerdp
# %{_mandir}/*/*

%files libs
%defattr(-,root,root)
%doc LICENSE README
%{_libdir}/lib*.so.*
%dir %{_libdir}/freerdp
%{_datadir}/freerdp/

%files plugins-standard
%defattr(-,root,root)
%{_libdir}/freerdp/*.so

%files devel
%defattr(-,root,root)
%{_includedir}/freerdp/
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%changelog
* Man Sep 19 2022 TOMATO <junker.tomato@gmaill.com> - git836b738-1
- Initial build for NeutrioRDP 
