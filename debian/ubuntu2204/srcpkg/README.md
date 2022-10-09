# debuild 方法

## 準備

### 最低限必要なdpkgを追加
```bash
apt update
apt install -y sudo wget curl vim git
```

### build用ユーザ追加
```bash
useradd -m -s /usr/bin/bash builduser 
usermod -aG sudo builduser
echo "builduser:P@ssw0rd" | chpasswd
echo "ALL ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/builduser

su - builduser
sudo apt install -y dpkg-dev

export DEBEMAIL="hoge@example.com"
export DEBFULLNAME="Hoge Hoge"

```
### quilt コマンドの準備とalias設定
debian/ubuntu deb pkg のパッチ管理コマンドのquilt をインストールしaliasを作る
```bash
sudo apt install quilt -y

alias dquilt="quilt --quiltrc=${HOME}/.quiltrc-dpkg"
. /usr/share/bash-completion/completions/quilt
complete -F _quilt_completion -o filenames dquilt
```

以下内容で `${HOME}/.quiltrc-dpkg` を作成する。
```bash
d=. ; while [ ! -d $d/debian -a `readlink -e $d` != / ]; do d=$d/..; done
if [ -d $d/debian ] && [ -z $QUILT_PATCHES ]; then
    QUILT_PATCHES="debian/patches"
    QUILT_PATCH_OPTS="--reject-format=unified"
    QUILT_DIFF_ARGS="-p ab --no-timestamps --no-index --color=auto"
    QUILT_REFRESH_ARGS="-p ab --no-timestamps --no-index"
    QUILT_COLORS="diff_hdr=1;32:diff_add=1;34:diff_rem=1;31:diff_hunk=1;33:diff_ctx=35:diff_cctx=33"
    if ! [ -d $d/debian/patches ]; then mkdir $d/debian/patches; fi
fi
```
---
## NeutrinoRDP
### buildに必要なpkgを追加
```bash
sudo apt-get -y install build-essential git-core cmake libssl-dev libx11-dev libxext-dev libxinerama-dev \
libxcursor-dev libxdamage-dev libxv-dev libxkbfile-dev libasound2-dev libcups2-dev libxml2 libxml2-dev \
libxrandr-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libavutil-dev  libavcodec-dev dh-make devscripts lintian git-buildpackage quilt pbuilder \
dput debhelper debmake fakeroot equivs cdbs
```
### srcpkg を取得
```bash
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/debian/sources/neutrinordp-836b738.tar.gz
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/debian/ubuntu2204/srcpkg/neutrinordp_1.0.1%2B836b738-1.debian.tar.xz
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/debian/ubuntu2204/srcpkg/neutrinordp_1.0.1%2B836b738-1.dsc
ln -s ./neutrinordp-836b738.tar.gz neutrinordp_1.0.1+836b738.orig.tar.gz
```
### Source 展開
```bash
dpkg-source -x neutrinordp_1.0.1+836b738-1.dsc
cd neutrinodrpd-836b738
```
### patch 適用
```bash
while dquilt push; do dquilt refresh; done
```
### build
```bash
dpkg-buildpackage -us -uc
```
  親ディレクトリに、debファイルとソースpkgが展開される。

---
## xrdp
### 前段で作成したNutrinoRDPをインストール
```bash
sudo apt install -y \
./libneutrinordp_1.0.1+836b738-1_amd64.deb \ 
./libneutrinordp-dev_1.0.1+836b738-1_amd64.deb
```
### buildに必要なpkgを追加
```bash
sudo apt install -y \
dh-make devscripts lintian git-buildpackage quilt pbuilder \
dput debhelper debmake fakeroot equivs cdbs check libfuse-dev libopus-dev \
libpam0g-dev libssl-dev nasm systemd libfuse2 libsubunit-dev libsubunit0
```

### srcpkg を取得
```bash
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/debian/sources/xrdp-0.9.20.tar.gz
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/debian/ubuntu2204/srcpkg/xrdp_0.9.20-1.debian.tar.xz
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/debian/ubuntu2204/srcpkg/xrdp_0.9.20-1.dsc
ln -s ./xrdp-0.9.20.tar.gz xrdp_0.9.20.orig.tar.gz
```
### Source 展開
```bash
dpkg-source -x xrdp_0.9.20-1.dsc
cd xrdp-0.9.20
```
### patch 適用
```bash
while dquilt push; do dquilt refresh; done
```
### build
```bash
dpkg-buildpackage -us -uc
```
  親ディレクトリに、debファイルとソースpkgが展開される。

---
## xorgxrdp
### 前段で作成したxrdpをインストール
```bash
sudo apt install -y ./xrdp_0.9.20-1_amd64.deb
```
### buildに必要なpkgを追加
```bash
sudo apt install -y \
 libepoxy-dev  libgbm-dev   x11-utils  xrdp  xserver-xorg-core xserver-xorg-dev
 ```
### srcpkg を取得
```bash
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/debian/sources/xorgxrdp-0.9.19.tar.gz
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/debian/ubuntu2204/srcpkg/xrdp_0.9.20-1.debian.tar.xz
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/debian/ubuntu2204/srcpkg/xrdp_0.9.20-1.dsc
ln -s xorgxrdp-0.9.19.tar.gz xorgxrdp_0.9.19.orig.tar.gz
```

### Source 展開
```bash
dpkg-source -x xorgxrdp_0.9.19-1.dsc
cd xorgxrdp-0.9.19
```
### patch 適用
```bash
while dquilt push; do dquilt refresh; done
```

### build
```bash
dpkg-buildpackage -us -uc
```

親ディレクトリに、debファイルとソースpkgが展開される。

---




## 補足：Source Rev 変更する場合

quilt コマンドをインストールする。
```bash
sudo apt install quilt -y
```

上位バージョンのソースアーカイブファイルを置いておく。
現在のversion の sourceを dpkg-source -x で 展開し、ディレクトリに移動する。
```bash
uupdate -v XXXXXXX ../neutrinordp-XXXXXX.tar.gz
```
新しいRevのディレクトリが作成される。
```bash
cd ../neutrinordp-XXXXXXX
dch -v 1:1.0.1+XXXXXX-1 -b
```
`dch --bpo` とすると ~bp1 などというバックポートパッチ番号になる。

### Patch追加する場合
patch は dbian/patch 以下に置き、debian/patch/series にファイル名を追記する。
```bash
alias dquilt="quilt --quiltrc=${HOME}/.quiltrc-dpkg"
. /usr/share/bash-completion/completions/quilt
complete -F _longopt -o filenames dquilt
```
`while dquilt push; do dquilt refresh; done`

 削除する場合 ` dquilt delete debian/patches/shutup-daemon.diff`

うまくパッチが当たらない場合以下ファイルを作成してみる。

`$HOME/.quiltrc-dpkg`
```bash
d=. ; while [ ! -d $d/debian -a `readlink -e $d` != / ]; do d=$d/..; done
if [ -d $d/debian ] && [ -z $QUILT_PATCHES ]; then
    # if in Debian packaging tree with unset $QUILT_PATCHES
    QUILT_PATCHES="debian/patches"
    QUILT_PATCH_OPTS="--reject-format=unified"
    QUILT_DIFF_ARGS="-p ab --no-timestamps --no-index --color=auto"
    QUILT_REFRESH_ARGS="-p ab --no-timestamps --no-index"
    QUILT_COLORS="diff_hdr=1;32:diff_add=1;34:diff_rem=1;31:diff_hunk=1;33:diff_ctx=35:diff_cctx=33"
    if ! [ -d $d/debian/patches ]; then mkdir $d/debian/patches; fi
fi
```
---
## 参考URL
https://www.debian.org/doc/manuals/maint-guide/update.ja.html#newupstream 

https://wiki.debian.org/SimpleBackportCreation

  https://qiita.com/miyase256/items/4eeab35a9e69195d1a66 