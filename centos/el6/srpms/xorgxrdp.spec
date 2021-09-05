%define	xorgxrdpver	0.2.17
%define xrdpver         0.9.17
%define	xorgxrdpbranch	v0.9
%define moduledir	%(pkg-config xorg-server --variable=moduledir)
%define driverdir	%{moduledir}/drivers
%define inputdir	%{moduledir}/input
%define	xrdpxorgconfdir	%{_sysconfdir}/X11/xrdp

Summary:	Xorg X11 rdp driver for xrdp
Name:		xorgxrdp
Version:	%{xorgxrdpver}
License:	the X11 License
Release:	1%{?dist}
URL:		http://www.xrdp.org/
Source0:	xorgxrdp-%{xorgxrdpver}.tar.gz
Source1:	xrdp-%{xrdpver}.tar.gz

# Dependencies don't vary depending on build options
Requires:	xorg-x11-server-Xorg
BuildRequires:	automake
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	make
BuildRequires:	gcc
BuildRequires:	pam-devel
BuildRequires:	pkgconfig
BuildRequires:	xorg-x11-server-devel
BuildRequires:	nasm
# this should be libXfont2-devel or libXfont-devel
BuildRequires:	libXfont-devel

BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
Xorg X11 rdp driver for xrdp

%prep
%setup -b 1 -n xrdp-%{xrdpver}
%setup -n xorgxrdp-%{xorgxrdpver}
# find . -type f | xargs sed -i.bak -e 's|#define LOG_LEVEL [0-9]*|#define LOG_LEVEL 20|'

%build
./bootstrap
./configure XRDP_CFLAGS=-I%{_builddir}/xrdp-%{xrdpver}/common
%{__make}

%install
%{__make} install DESTDIR=%{buildroot}
%{__install} -p -d -m 0755 %{buildroot}%{xrdpxorgconfdir}
%{__install} -p -m 0644 xrdpdev/xorg.conf %{buildroot}%{xrdpxorgconfdir}
find %{buildroot} -name \*.la -delete
find %{buildroot} -name \*.a -delete

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{moduledir}/libxorgxrdp.so
%{driverdir}/xrdpdev_drv.so
%{inputdir}/xrdpmouse_drv.so
%{inputdir}/xrdpkeyb_drv.so
%config(noreplace) %{xrdpxorgconfdir}/xorg.conf
