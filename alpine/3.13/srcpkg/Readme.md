# xrdp-proxy
これはNeutrinoRDP-any (RDP Proxy)モジュールを有効にしたxrdpをbuildするためのAlpine Linux用source pakage です。  
libneutrinordp.so に依存するためNeutrinoRDP のbuildも必要です。  
NeutrinoRDPはFreeRDP 1.0.1からforkしたRDP client ですがファイル名の関係でFreeRDPと共存できません。  

インストール直後のAlpine Linux 3.13 から以下の手順でbinary package をbuild できます。

```
# Alpine Linux community リポジトリを有効化
sed -i'.bak' -e "s/^#\(http:\/\/mirror.xtom.com.hk\/alpine\/v3.13\/community\)/\1/1" /etc/apk/repositories

# build用ユーザの作成と準備
apk add --update --no-cache alpine-sdk sudo
adduser -D builduser
addgroup builduser abuild
echo "ALL ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/builduser
su builduser
cd ~
abuild-keygen -a -i -n -q

# NeutrinoRDP のbuild
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.13/srcpkg/neutrinordp-1.0.1-0.src.tar.gz
tar zxvf ./neutrinordp-1.0.1-0.src.tar.gz
cd NeutrinoRDP/
sudo apk update
abuild -r

# xrdp に必要なneutrinordp-libs,neutrinordp-dev のインストール
sudo apk add --update --no-cache ~/packages/src/`uname -m`/neutrinordp-dev-1.0.1-r1.apk ~/packages/src/`uname -m`/neutrinordp-libs-1.0.1-r0.apk

# xrdp のbuild
cd ~ 
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.13/srcpkg/xrdp-0.9.16-0.src.tar.gz
tar zxf ./xrdp-0.9.16-0.src.tar.gz
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
