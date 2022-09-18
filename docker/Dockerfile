ARG ALPINE_VERSION="3.16"
ARG XRDP_VERSION="0.9.20"
ARG XRDP_PKG_RELEASE="1"
ARG XRDP_GITHASH="e101d6b"
ARG NEUTRINORDP_VERSION="1.0.1"
ARG NEUTRINORDP__VERSION="devel"
ARG NEUTRINORDP_PKG_RELEASE="1"
ARG NEUTRINORDP_GITHASH="836b738"


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
      echo 'source="$pkgname-$_pkgver.tar.gz::https://github.com/neutrinolabs/NeutrinoRDP/archive/devel.tar.gz"'; \
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
&&  abuild -r 

#RUN ls -al ~/packages/home/x86_64/ \
#&&  ls -al ~/packages/src/
VOLUME ~/packages

RUN find ~/packages -name "*.apk" -exec mv {} ~/packages/ \; \
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
    echo 'diff --git a/xrdp/Makefile.am b/xrdp/Makefile.am'; \
    echo 'index a259ef3..0d8e66f 100644'; \
    echo '--- a/xrdp/Makefile.am'; \
    echo '+++ b/xrdp/Makefile.am'; \
    echo '@@ -23,7 +23,7 @@ endif'; \
    echo ' if XRDP_RFXCODEC'; \
    echo ' AM_CPPFLAGS += -DXRDP_RFXCODEC'; \
    echo ' AM_CPPFLAGS += -I$(top_srcdir)/librfxcodec/include'; \
    echo '-XRDP_EXTRA_LIBS += $(top_builddir)/librfxcodec/src/.libs/librfxencode.a'; \
    echo '+XRDP_EXTRA_LIBS += $(top_builddir)/librfxcodec/src/librfxencode.la'; \
    echo ' endif'; \
    echo ' '; \
    echo ' if XRDP_PIXMAN'; \
    echo '@@ -35,7 +35,7 @@ endif'; \
    echo ' if XRDP_PAINTER'; \
    echo ' AM_CPPFLAGS += -DXRDP_PAINTER'; \
    echo ' AM_CPPFLAGS += -I$(top_srcdir)/libpainter/include'; \
    echo '-XRDP_EXTRA_LIBS += $(top_builddir)/libpainter/src/.libs/libpainter.a'; \
    echo '+XRDP_EXTRA_LIBS += $(top_builddir)/libpainter/src/libpainter.la'; \
    echo ' endif'; \
    echo ' '; \
    echo ' sbin_PROGRAMS = \'; \
} > dynamic-link.patch

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

RUN { \
     echo '[Globals]'; \
     echo 'ini_version=1'; \
     echo 'fork=true'; \
     echo 'port=3389'; \
     echo 'use_vsock=false'; \
     echo 'tcp_nodelay=true'; \
     echo 'tcp_keepalive=true'; \
     echo 'security_layer=negotiate'; \
     echo 'crypt_level=high'; \
     echo 'certificate='; \
     echo 'key_file='; \
     echo 'ssl_protocols=TLSv1.2, TLSv1.3'; \
     echo '#tls_ciphers=HIGH'; \
     echo '#domain_user_separator=@'; \
     echo '#xrdp.override_keyboard_type=0x04'; \
     echo '#xrdp.override_keyboard_subtype=0x01'; \
     echo '#xrdp.override_keylayout=0x00000409'; \
     echo 'autorun='; \
     echo 'allow_channels=true'; \
     echo 'allow_multimon=true'; \
     echo 'bitmap_cache=true'; \
     echo 'bitmap_compression=true'; \
     echo 'bulk_compression=true'; \
     echo '#hidelogwindow=true'; \
     echo 'max_bpp=32'; \
     echo 'new_cursors=true'; \
     echo 'use_fastpath=both'; \
     echo '#require_credentials=true'; \
     echo '#enable_token_login=true'; \
     echo '#pamerrortxt=change your password according to policy at http://url'; \
     echo 'blue=009cb5'; \
     echo 'grey=dedede'; \
     echo '#black=000000'; \
     echo '#dark_grey=808080'; \
     echo '#blue=08246b'; \
     echo '#dark_blue=08246b'; \
     echo '#white=ffffff'; \
     echo '#red=ff0000'; \
     echo '#green=00ff00'; \
     echo '#background=626c72'; \
     echo '#ls_title=My Login Title'; \
     echo 'ls_top_window_bg_color=009cb5'; \
     echo 'ls_width=350'; \
     echo 'ls_height=430'; \
     echo 'ls_bg_color=dedede'; \
     echo '#ls_background_image='; \
     echo '#ls_background_transform=none'; \
     echo 'ls_logo_filename='; \
     echo '#ls_logo_transform=none'; \
     echo '#ls_logo_width=240'; \
     echo '#ls_logo_height=140'; \
     echo 'ls_logo_x_pos=55'; \
     echo 'ls_logo_y_pos=50'; \
     echo 'ls_label_x_pos=30'; \
     echo 'ls_label_width=65'; \
     echo 'ls_input_x_pos=110'; \
     echo 'ls_input_width=210'; \
     echo 'ls_input_y_pos=220'; \
     echo 'ls_btn_ok_x_pos=142'; \
     echo 'ls_btn_ok_y_pos=370'; \
     echo 'ls_btn_ok_width=85'; \
     echo 'ls_btn_ok_height=30'; \
     echo 'ls_btn_cancel_x_pos=237'; \
     echo 'ls_btn_cancel_y_pos=370'; \
     echo 'ls_btn_cancel_width=85'; \
     echo 'ls_btn_cancel_height=30'; \
     echo ''; \
     echo '[Logging]'; \
     echo 'LogFile=xrdp.log'; \
     echo 'LogLevel=INFO'; \
     echo 'EnableSyslog=false'; \
     echo '#SyslogLevel=INFO'; \
     echo 'EnableConsole=true'; \
     echo 'ConsoleLevel=INFO'; \
     echo '#EnableProcessId=false'; \
     echo ''; \
     echo '[LoggingPerLogger]'; \
     echo '#xrdp.c=INFO'; \
     echo '#main()=INFO'; \
     echo '[Channels]'; \
     echo 'rdpdr=true'; \
     echo 'rdpsnd=true'; \
     echo 'drdynvc=true'; \
     echo 'cliprdr=true'; \
     echo 'rail=true'; \
     echo 'xrdpvr=true'; \
     echo 'tcutils=true'; \
     echo '#port=/tmp/.xrdp/xrdp_display_10'; \
     echo ''; \
     echo '[RDP-Proxy]'; \
     echo 'name=RDP-Proxy'; \
     echo 'lib=libxrdpneutrinordp.so'; \
     echo 'ip=ask'; \
     echo 'port=ask3389'; \
     echo 'username=ask'; \
     echo 'password=ask'; \
     echo '#pamusername=ask'; \
     echo '#pampassword=ask'; \
     echo '#pamsessionmng=127.0.0.1'; \
     echo 'enable_dynamic_resizing=false'; \
     echo 'perf.allow_client_experiencesettings=true'; \
     echo '#perf.wallpaper=false'; \
     echo '#perf.font_smoothing=false'; \
     echo '#perf.desktop_composition=false'; \
     echo '#perf.full_window_drag=false'; \
     echo '#perf.menu_anims=false'; \
     echo '#perf.themes=false'; \
     echo '#perf.cursor_blink=false'; \
     echo 'perf.cursor_shadow=false'; \
     echo 'neutrinordp.allow_client_keyboardLayout=true'; \
     echo '#neutrinordp.override_keyboardLayout_mask=0x0000FFFF'; \
     echo '#neutrinordp.override_kbd_type=0x04'; \
     echo '#neutrinordp.override_kbd_subtype=0x01'; \
     echo '#neutrinordp.override_kbd_fn_keys=12'; \
     echo '#neutrinordp.override_kbd_layout=0x00000409'; \
     echo 'channel.rdpdr=true'; \
     echo 'channel.rdpsnd=true'; \
     echo 'channel.drdynvc=true'; \
     echo 'channel.cliprdr=true'; \
     echo 'channel.rail=true'; \
     echo 'channel.xrdpvr=true'; \
     echo ''; \
     echo '[vnc-proxy]'; \
     echo 'name=VNC-Proxy'; \
     echo 'lib=libvnc.so'; \
     echo 'ip=ask'; \
     echo 'port=ask5900'; \
     echo 'username=na'; \
     echo 'password=ask'; \
     echo '#pamusername=asksame'; \
     echo '#pampassword=asksame'; \
     echo '#pamsessionmng=127.0.0.1'; \
     echo 'delay_ms=2000'; \
} > ~/xrdp.ini


RUN \
    abuild-keygen -a -i -n -q \
&&  abuild checksum \
&&  abuild -r 

VOLUME ~/packages

RUN find ~/packages -name "*.apk" -exec mv {} ~/packages/ \; \
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

COPY --from=xrdp_builder /home/builduser/xrdp.ini /etc/xrdp/xrdp.ini
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
