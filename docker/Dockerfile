ARG ALPINE_VERSION="3.13"
ARG XRDP_VERSION="0.9.15"
ARG XRDP_PKG_RELEASE="0"
ARG XRDP_GITHASH="f24b7b7"
ARG NEUTRINORDP_VERSION="1.0.1"
ARG NEUTRINORDP__VERSION="devel"
ARG NEUTRINORDP_PKG_RELEASE="0"
ARG NEUTRINORDP_GITHASH="f7832d6"


FROM alpine:$ALPINE_VERSION as NeutrinoRDP_builder

ARG ALPINE_VERSION
ARG XRDP_VERSION
ARG XRDP_PKG_RELEASE
ARG XRDP_GITHASH
ARG NEUTRINORDP_VERSION
ARG NEUTRINORDP__VERSION
ARG NEUTRINORDP_PKG_RELEASE
ARG NEUTRINORDP_GITHASH

RUN  \
   apk add --no-cache alpine-sdk sudo \
&& apk update \
&& adduser -D builduser \
&& addgroup builduser abuild \
&& echo "ALL ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/builduser 

USER builduser
WORKDIR  /home/builduser
RUN   wget https://raw.githubusercontent.com/TOMATO-ONE/xrdp-proxy/devel/alpine/3.13/srcpkg/xcuroroff.patch    
      
RUN { \
      echo '# Contributor: Dummy user <your@email.address>'; \
      echo '# Maintainer: Dummy user <your@email.address>'; \
      echo 'pkgname="neutrinordp"'; \
      echo '_pkgname="NeutrinoRDP"'; \
      echo "pkgver=$NEUTRINORDP_VERSION"; \
      echo "_pkgver=$NEUTRINORDP__VERSION"; \
      echo "pkgrel=$NEUTRINORDP_PKG_RELEASE"; \
      echo 'pkgdesc="NeutrinoRDP fork of FreeRDP 1.0.1"'; \
      echo 'url="https://github.com/neutrinolabs/NeutrinoRDP"'; \
      echo '_giturl="https://github.com/neutrinolabs/NeutrinoRDP.git"'; \
      echo '_gitbranch="devel"'; \
      echo "_githash=\"$NEUTRINORDP_GITHASH\""; \
      echo 'arch="all"'; \
      echo 'license="Apache-2.0"'; \
      echo 'replaces="freerdp"'; \
      echo 'options="!check"'; \
      echo 'makedepends="cmake gcc libc-dev automake autoconf make zlib-dev openssl-dev libxcursor-dev'; \
      echo '         cups-dev alsa-lib-dev ffmpeg-dev libxkbfile-dev libxinerama-dev libxv-dev'; \
      echo '         libxdamage-dev libjpeg-turbo-dev libxi-dev cmake bsd-compat-headers'; \
      echo '         gst-plugins-base-dev gsm-dev linux-headers libusb-dev libxtst-dev libxrandr-dev"'; \
      echo 'subpackages="$pkgname-dev $pkgname-plugins $pkgname-libs"'; \
      echo 'source="$pkgname-$_pkgver.tar.gz::https://github.com/neutrinolabs/NeutrinoRDP/archive/devel.tar.gz'; \
      echo '        xcuroroff.patch"'; \
      echo ''; \
      echo 'builddir="$srcdir"/$_pkgname-$_pkgver'; \
      echo ''; \
      echo 'prepare() {'; \
      echo '  default_prepare'; \
      echo '}'; \
      echo ''; \
      echo ''; \
      echo 'build() {'; \
      echo '        local _SSE2_opt=""'; \
      echo '        case "$CARCH" in'; \
      echo '                aarch64*|arm*|ppc64le|x86|s390x) _SSE2_opt="-DWITH_SSE2=OFF" ;;'; \
      echo '                x86_64)                          _SSE2_opt="-DWITH_SSE2=ON" ;;'; \
      echo '                *)                               msg "Unable to determine architecture from (CARCH=$CARCH)" ; return 1 ;;'; \
      echo '        esac'; \
      echo ''; \
      echo '        export CFLAGS="$CFLAGS -D_BSD_SOURCE"'; \
      echo '        cmake -DCMAKE_BUILD_TYPE=Release \'; \
      echo '                -DCMAKE_INSTALL_PREFIX=/usr \'; \
      echo '                -DCMAKE_INSTALL_LIBDIR=lib \'; \
      echo '               -DWITH_ALSA=ON \'; \
      echo '               -DWITH_CUPS=ON \'; \
      echo '               -DWITH_DIRECTFB=OFF \'; \
      echo '               -DWITH_FFMPEG=OFF \'; \
      echo '               -DWITH_JPEG=ON \'; \
      echo '               -DWITH_PCSC=OFF \'; \
      echo '               -DWITH_SERVER=OFF \'; \
      echo '               -DWITH_X11=ON \'; \
      echo '               -DWITH_XCURSOR=ON \'; \
      echo '               -DWITH_XEXT=ON \'; \
      echo '               -DWITH_XKBFILE=ON \'; \
      echo '               -DWITH_XINERAMA=ON \'; \
      echo '               -DWITH_XV=ON \'; \
      echo '               -DWITH_NEON=OFF \'; \
      echo '               ${_SSE2_opt}'; \
      echo '        make'; \
      echo '}'; \
      echo ''; \
      echo 'package() {'; \
      echo '        make DESTDIR="$pkgdir" install'; \
      echo '}'; \
      echo ''; \
      echo 'libs() {'; \
      echo '        pkgdesc="NeutrinoRDP client - Libraries"'; \
      echo '        replaces="libfreerdp"'; \
      echo '        mkdir -p "$subpkgdir"/usr'; \
      echo '        mv "$pkgdir"/usr/lib "$subpkgdir"/usr/'; \
      echo '}'; \
      echo ''; \
      echo 'plugins() {'; \
      echo '        pkgdesc="NeutrinoRDP client - Plugins"'; \
      echo '        replaces="libfreerdp"'; \
      echo '        mkdir -p "$subpkgdir"/usr/lib'; \
      echo '        mv "$pkgdir"/usr/lib/freerdp "$subpkgdir"/usr/lib/'; \
      echo '}'; \
} > APKBUILD


RUN echo build \
&&  abuild-keygen -a -i -n -q \
&&  abuild checksum \
&&  abuild -r \
&&  abuild srcpkg 

#RUN ls -al ~/packages/home/x86_64/ \
#&&  ls -al ~/packages/src/
VOLUME ~/packages

RUN find ~/packages -name "*.apk" -exec mv {} ~/packages/ \; \
&&  find ~/packages/src/ -name "*.apk" -exec mv {} ~/packages/ \; \
&&  ls -al ~/packages/ 

FROM alpine:$ALPINE_VERSION as xrdp_builder

ARG ALPINE_VERSION
ARG XRDP_VERSION
ARG XRDP_PKG_RELEASE
ARG XRDP_GITHASH
ARG NEUTRINORDP_VERSION
ARG NEUTRINORDP__VERSION
ARG NEUTRINORDP_PKG_RELEASE
ARG NEUTRINORDP_GITHASH

COPY --from=NeutrinoRDP_builder /home/builduser/packages/*.apk ./

RUN \ 
     apk add --update --no-cache ./neutrinordp-dev-$NEUTRINORDP_VERSION-r$NEUTRINORDP_PKG_RELEASE.apk ./neutrinordp-libs-$NEUTRINORDP_VERSION-r$NEUTRINORDP_PKG_RELEASE.apk  --allow-untrusted

RUN  \
   apk add --no-cache alpine-sdk sudo \
&& apk update \
&& adduser -D builduser \
&& addgroup builduser abuild \
&& echo "ALL ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/builduser

USER builduser
WORKDIR  /home/builduser


RUN { \
     echo '# Contributor: Alan Lacerda <alacerda@alpinelinux.org>'; \
     echo '# Maintainer: Alan Lacerda <alacerda@alpinelinux.org>'; \
     echo 'pkgname=xrdp'; \
     echo "pkgver=$XRDP_VERSION"; \
     echo 'pkgrel=$XRDP_PKG_RELEASE'; \
     echo 'pkgdesc="Open source RDP server with RDP/VNC proxy"'; \
     echo 'url="https://www.xrdp.org/"'; \
     echo 'arch="all"'; \
     echo 'license="Apache-2.0"'; \
     echo 'makedepends="autoconf automake libtool openssl-dev libx11-dev'; \
     echo '	libxfixes-dev libxrandr-dev libjpeg-turbo-dev fuse-dev linux-headers'; \
     echo '	nasm linux-pam-dev'; \
     echo '	neutrinordp-libs"'; \
     echo 'subpackages="$pkgname-doc $pkgname-dev $pkgname-openrc"'; \
     echo 'source="https://github.com/neutrinolabs/xrdp/releases/download/v$pkgver/xrdp-$pkgver.tar.gz'; \
     echo '	xrdp.initd'; \
     echo '	dynamic-link.patch'; \
     echo '	xrdp_ini.patch'; \
     echo '     xrdp-neutrinordp.c.patch'; \
     echo '	"'; \
     echo ''; \
     echo ''; \
     echo 'build() {'; \
     echo '	local _simd_opt=""'; \
     echo '	if [ "$CARCH" = "x86" ]; then'; \
     echo '		_simd_opt="--without-simd"'; \
     echo '	fi'; \
     echo ''; \
     echo '	./bootstrap'; \
     echo '	./configure \'; \
     echo '		--prefix=/usr \'; \
     echo '		--disable-static \'; \
     echo '		--sysconfdir=/etc \'; \
     echo '		--localstatedir=/var \'; \
     echo '		--sbindir=/usr/sbin \'; \
     echo '		--enable-fuse \'; \
     echo '		--enable-tjpeg \'; \
     echo '		--enable-neutrinordp \'; \
     echo '		--enable-rdpsndaudin \'; \
     echo '		$_simd_opt'; \
     echo '	make'; \
     echo '}'; \
     echo ''; \
     echo 'package() {'; \
     echo '	make DESTDIR="$pkgdir" install'; \
     echo ''; \
     echo '	install -m755 -D "$srcdir"/$pkgname.initd \'; \
     echo '		"$pkgdir"/etc/init.d/$pkgname'; \
     echo '	ln -s $pkgname $pkgdir/etc/init.d/$pkgname-sesman'; \
     echo '}'; \
     echo ''; \
} > APKBUILD


RUN { \
     echo '#!/sbin/openrc-run'; \
     echo ''; \
     echo 'command=/usr/sbin/$SVCNAME'; \
     echo 'pidfile=/var/run/$SVCNAME.pid'; \
     echo ''; \
     echo 'depend() {'; \
     echo '	need net'; \
     echo '	after firewall'; \
     echo '}'; \
} > xrdp.initd

RUN \
    wget https://raw.githubusercontent.com/TOMATO-ONE/xrdp-proxy/devel/alpine/3.13/srcpkg/dynamic-link.patch \
&&  wget https://raw.githubusercontent.com/TOMATO-ONE/xrdp-proxy/devel/alpine/3.13/srcpkg/xrdp_ini.patch \
&&  wget https://raw.githubusercontent.com/TOMATO-ONE/xrdp-proxy/devel/alpine/3.13/srcpkg/xrdp-neutrinordp.c.patch \
&&  abuild-keygen -a -i -n -q \
&&  abuild checksum \
&&  abuild -r \
&&  abuild srcpkg 

#RUN ls -al ~/packages/home/x86_64/ \
#&&  ls -al ~/packages/src/
VOLUME ~/packages

RUN find ~/packages -name "*.apk" -exec mv {} ~/packages/ \; \
&&  find ~/packages/src/ -name "*.apk" -exec mv {} ~/packages/ \; \
&&  ls -al ~/packages/ 

FROM alpine:$ALPINE_VERSION as target

ARG ALPINE_VERSION
ARG XRDP_VERSION
ARG XRDP_PKG_RELEASE
ARG XRDP_GITHASH
ARG NEUTRINORDP_VERSION
ARG NEUTRINORDP__VERSION
ARG NEUTRINORDP_PKG_RELEASE
ARG NEUTRINORDP_GITHASH


WORKDIR  /tmp

COPY --from=NeutrinoRDP_builder /home/builduser/packages/neutrinordp-libs-$NEUTRINORDP_VERSION-r$NEUTRINORDP_PKG_RELEASE.apk ./
COPY --from=xrdp_builder /home/builduser/packages/xrdp-$XRDP_VERSION-r$XRDP_PKG_RELEASE.apk ./
COPY --from=xrdp_builder /home/builduser/packages/xrdp-openrc-$XRDP_VERSION-r$XRDP_PKG_RELEASE.apk ./

RUN \
     apk add --update --no-cache \
             /tmp/neutrinordp-libs-$NEUTRINORDP_VERSION-r$NEUTRINORDP_PKG_RELEASE.apk \
             /tmp/xrdp-$XRDP_VERSION-r$XRDP_PKG_RELEASE.apk \
             /tmp/xrdp-openrc-$XRDP_VERSION-r$XRDP_PKG_RELEASE.apk \
             openrc \
             linux-pam \
             shadow \
             --allow-untrusted \
&&   rm -f /tmp/*.apk

# config
RUN sed -i 's/#rc_sys=""/rc_sys="lxc"/g' /etc/rc.conf  \
&&    sed -i 's/^#rc_provide="!net"/rc_provide="loopback net"/' /etc/rc.conf  \
&&    sed -i '/getty/d' /etc/inittab  \
&&    sed -i 's/mount -t tmpfs/# mount -t tmpfs/' /lib/rc/sh/init.sh  \
&&    sed -i 's/hostname $opts/# hostname $opts/' /etc/init.d/hostname \
&&    mkdir -p /run/openrc  \
&&    touch /run/openrc/softlevel  \
&&    rc-status  \
&&    rc-update add xrdp-sesman  \
#   rc-update add xrdp  \
&&    wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/docker/entrypoint.sh -O /root/entrypoint.sh  \
&&    chmod +x /root/entrypoint.sh

EXPOSE 3389
VOLUME /sys/fs/cgroup
VOLUME /var/log

ENTRYPOINT [ "/root/entrypoint.sh" ]

