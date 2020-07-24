FROM alpine:3.11

LABEL MAINTAINER TOMATO

# package install
RUN  wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.11/x86_64/xrdp-0.9.13.1-r0.apk -P /tmp/ && \
     wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.11/x86_64/xrdp-openrc-0.9.13.1-r0.apk -P /tmp/ && \
     wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.11/x86_64/neutrinordp-libs-1.0.1-r0.apk -P /tmp/ && \
     wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.11/x86_64/neutrinordp-plugins-1.0.1-r0.apk -P /tmp/ && \
     apk add --update --no-cache \
             /tmp/neutrinordp-libs-1.0.1-r0.apk \
             /tmp/xrdp-0.9.13.1-r0.apk \
             /tmp/xrdp-openrc-0.9.13.1-r0.apk \
             openrc \
             linux-pam \
             shadow \
             --allow-untrusted && \
     rm -f /tmp/*.apk

# config
RUN sed -i 's/#rc_sys=""/rc_sys="lxc"/g' /etc/rc.conf ; \
    sed -i 's/^#rc_provide="!net"/rc_provide="loopback net"/' /etc/rc.conf ; \
    sed -i '/getty/d' /etc/inittab ; \
    sed -i 's/mount -t tmpfs/# mount -t tmpfs/' /lib/rc/sh/init.sh ; \
    sed -i 's/hostname $opts/# hostname $opts/' /etc/init.d/hostname ;\
    mkdir -p /run/openrc && \
    touch /run/openrc/softlevel && \
    rc-status && \
    rc-update add xrdp-sesman && \
#   rc-update add xrdp && \
    wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/docker/entrypoint.sh -O /root/entrypoint.sh && \
    chmod +x /root/entrypoint.sh

EXPOSE 3389
VOLUME /sys/fs/cgroup
VOLUME /var/log

ENTRYPOINT [ "/root/entrypoint.sh" ]
