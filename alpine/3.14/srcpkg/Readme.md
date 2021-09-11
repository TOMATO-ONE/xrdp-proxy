# xrdp-proxy
これはNeutrinoRDP-any (RDP Proxy)モジュールを有効にしたxrdpをbuildするためのAlpine Linux用source pakage です。  
libneutrinordp.so に依存するためNeutrinoRDP のbuildも必要です。  
NeutrinoRDPはFreeRDP 1.0.1からforkしたRDP client ですがファイル名の関係でFreeRDP 1.x とは共存できません。  

インストール直後のAlpine Linux 3.14 から以下の手順でbinary package をbuild できます。

```
# build用ユーザの作成と準備
apk add --update --no-cache alpine-sdk sudo
adduser -D builduser
addgroup builduser abuild
echo "builduser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/builduser
su builduser
cd ~
abuild-keygen -a -i -n -q

# NeutrinoRDP のbuild
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.14/srcpkg/neutrinordp-f7832d6-1.src.tar.gz
tar zxvf ./neutrinordp-f7832d6-1.src.tar.gz
cd NeutrinoRDP/
sudo apk update
abuild -r

# xrdp に必要なneutrinordp-libs,neutrinordp-dev のインストール
sudo apk add --update --no-cache ~/packages/src/`uname -m`/neutrinordp-dev-f7832d6-r1.apk ~/packages/src/`uname -m`/neutrinordp-libs-f7832d6-r1.apk

# xrdp のbuild
cd ~ 
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.14/srcpkg/xrdp-0.9.16-0.src.tar.gz
tar zxf ./xrdp-0.9.17-1.src.tar.gz
cd xrdp/
abuild -r
```
 /home/builduser/package 以下に apk binary package が生成されます。

build後のクリーンアップ
```
deluser --remove-home builduser
rm -f /etc/sudoers.d/builduser
apk del --purge neutrinordp-dev alpine-sdk
# ※ abuild -r 最中にインストールされたpkg はbuild終了時に削除されます。 
```
