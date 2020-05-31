# xrdp-proxy
これはNeutrinoRDP-any (RDP Proxy)モジュールを有効にしたxrdpをbuildするためのAlpine Linux用source pakage です。  
libneutrinordp.so に依存するためNeutrinoRDP のbuildも必要です。  
NeutrinoRDPはFreeRDP 1.0.1からforkしたRDP client ですがファイル名の関係でFreeRDPと共存できません。  

インストール直後のAlpine Linux 3.11 から以下の手順でbinary package をbuild できます。

```
# Alpine Linux community リポジトリを有効化
sed -i'.bak' -e "s/^#\(http:\/\/mirror.xtom.com.hk\/alpine\/v3.11\/community\)/\1/1" /etc/apk/repositories

# build用ユーザの作成と準備
apk add --update --no-cache alpine-sdk
adduser -D builduser
addgroup builduser abuild
echo "ALL ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/builduser
su builduser
cd ~
abuild-keygen -a -i -n -q

# NeutrinoRDP のbuild
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/srcpkg/neutrinordp-1.0.1-0.src.tar.gz
tar zxvf ./neutrinordp-1.0.1-0.src.tar.gz
cd NeutrinoRDP/
sudo apk update
abuild -r

# xrdp に必要なneutrinordp-libs,neutrinordp-dev のインストール
sudo apk add --update --no-cache ~/packages/builduser/x86_64/neutrinordp-dev-1.0.1-r0.apk ~/packages/builduser/x86_64/neutrinordp-libs-1.0.1-r0.apk

# xrdp のbuild
cd ~
wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/srcpkg/xrdp-0.9.13-1.src.tar.gz
tar zxf ./xrdp-0.9.13-1.src.tar.gz
cd xrdp/
abuild -r
# /home/builduser/package 以下に apk binary package が生成されます。
```


 通常のAlpine Linuxにインストールして起動する手順  
 ( 別ホストでapk add　するときには --allow-untrusted を付加してください。)
```
sudo apk add --update --no-cache ~/packages/builduser/x86_64/xrdp-0.9.13-r1.apk ~/packages/builduser/x86_64/xrdp-openrc-0.9.13-r1.apk 
exit

apk add --update --no-cache openrc 
rc-update add xrdp-sesman
rc-update add xrdp
rc-service xrdp-sesman start
rc-service xrdp start
```

Alpine Linux のdocker コンテナ内で起動するにはホストOS側の /sys/fs/cgroup をvolumeマウント`(-v /sys/fs/cgroup)`してコンテナ起動した上で以下の追加設定を行ってください。
```
sed -i 's/#rc_sys=""/rc_sys="lxc"/g' /etc/rc.conf
sed -i 's/^#rc_provide="!net"/rc_provide="loopback net"/' /etc/rc.conf
sed -i'.bak' '/getty/d' /etc/inittab
sed -i'.bak' 's/mount -t tmpfs/# mount -t tmpfs/' /lib/rc/sh/init.sh
sed -i'.bak' 's/hostname $opts/# hostname $opts/' /etc/init.d/hostname
mkdir -p /run/openrc
touch /run/openrc/softlevel
rc-status
rc-update add xrdp-sesman
rc-update add xrdp
rc-service xrdp-sesman start
rc-service xrdp start
```

/etc/xrdp/xrdp.ini を編集し、RDP/VNC 接続時の Linux PAM認証をする場合には
接続許可ユーザを tsusers グループに所属させてください。
```
apk add --update --no-cache linux-pam
addgroup tsusers
adduser -G tsusers -D -H -h /dev/null -s /sbin/nologin -g "xrdp user" <username>
passwd <username>
# ※グループ名をtsusersから変更するには /etc/xrdp/sesman.ini を編集してください。
```

build後のクリーンアップ
```
deluser --remove-home builduser
rm -f /etc/sudoers.d/builduser
apk del --purge neutrinordp-dev alpine-sdk
# ※ abuild -r 最中にインストールされたpkg はbuild終了時に削除されます。 
```

# 既知の不具合
##  ログイン後、日本語キーボードを使っているにも関わらず、英語のキー配列になってしまう。
   NeutrinoRDPモジュールの不具合が原因です。
   ワークアラウンドとして、接続先Windows側のレジストリを変更し、KBDJPN.DLLの代わりに kbd106.dll を定義し、再起動してください。

接続先Windowsの管理者権限でコマンドプロンプトを起動し、以下のコマンドを実行してください。
```
# 変更前確認
reg query  "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\00000411" /v "Layout File" 

# レジストリ変更
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\00000411" /v "Layout File" /d "kbd106.DLL

# 変更後確認
reg query  "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\00000411" /v "Layout File" 

# 再起動実施
shutdown /r 
```

## 接続後、マウスカーソルが黒い四角になってしまう
  NeutrinoRDPモジュールの不具合が原因です。
   ワークアラウンドとして、接続先Windows側で影を無効にするようにマウスカーソルの設定を変更してください。
```
	[設定]-[デバイス]-[マウス]-[その他のマウスオプション]-[ポインター]
	「ポインターの影を有効にする」のチェックボックスを OFFにする
```

-
