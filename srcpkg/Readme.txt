これらのファイルは NeutrinoRDP-any (RDP Proxy)モジュールを有効にしたxrdpをbuildするためのAlpine Linux の srcpkg です。
NeutrinoRDP のlib に依存するため併せてbuildが必要です。
NeutrinoRDPはFreeRDP 1.0.1からforkしたRDP client ですがファイル名の関係でFreeRDPと共存できません。


インストール直後のAlpine Linux 3.11 から以下の手順でbinary package をbuildすることができます。

apk add --update --no-cache alpine-sdk
adduser -D builduser
addgroup builduser abuild
echo "ALL ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/builduser
su builduser
cd ~
abuild-keygen -a -i -n -q


wget https://github.com/TOMATO-ONE/xrdp-proxy/blob/devel/srcpkg/neutrinordp-1.0.1-0.src.tar.gz 
tar zxvf ./neutrinordp-1.0.1-0.src.tar.gz
cd NeutrinoRDP/
abuild -r

sudo apk add --update --no-cache ~/packages/builduser/x86_64/neutrinordp-dev-1.0.1-r0.apk ~/packages/builduser/x86_64/neutrinordp-libs-1.0.1-r0.apk

wget https://github.com/TOMATO-ONE/xrdp-proxy/blob/devel/srcpkg/xrdp-0.9.13-1.src.tar.gz
tar zxf ./xrdp-0.9.13-1.src.tar.gz

cd xrdp/
abuild -r
sudo apk add --update --no-cache openrc linux-pam shadow ~/packages/NeutrinoRDP/x86_64/xrdp-0.9.13-r1.apk ~/packages/NeutrinoRDP/x86_64/xrdp-openrc-0.9.13-r1.apk

exit

sed -i 's/#rc_sys=""/rc_sys="lxc"/g' /etc/rc.conf
sed -i 's/^#rc_provide="!net"/rc_provide="loopback net"/' /etc/rc.conf
sed -i'.bak' '/getty/d' /etc/inittab
sed -i'.bak' 's/mount -t tmpfs/# mount -t tmpfs/' /lib/rc/sh/init.sh
sed -i'.bak' 's/hostname $opts/# hostname $opts/' /etc/init.d/hostname
mkdir /run/openrc
touch /run/openrc/softlevel
rc-status

rc-update add xrdp-sesman
rc-update add xrdp

groupadd tsusers

rc-service xrdp-sesman start
rc-service xrdp start

# deluser --remove-home builduser
# apk del neutrinordp-dev alpine-sdk
