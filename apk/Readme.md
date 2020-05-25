# xrdp-proxy
NeutrinoRDP-any(RDP Proxy)モジュールを有効にした、Alpine Linux 3.11 用 xrdp  0.9.13 binary packageです。  
xrdpはAlpine Linuxに標準のxrdp から configure optionを変更して生成しています。  
NeutrinoRDPは FreeRDPのABUILDファイルを流用して生成しています。

- xrdp  
  - xrdp-0.9.13-r1.apk  
        - NeutrinoRDP-anyモジュールを有効にしたxrdp本体  
  - xrdp-openrc-0.9.13-r1.apk  
        - openrc 用 initスクリプト  
  - xrdp-doc-0.9.13-r1.apk  
  - xrdp-dev-0.9.13-r1.apk  

* NeutrinoRDP  
   - neutrinordp-libs-1.0.1-r0.apk      
   - neutrinordp-plugins-1.0.1-r0.apk     
   - neutrinordp-1.0.1-r0.apk  
          - RDP client "xfreerdp" xrdp-proxyには不要  
   - neutrinordp-dev-1.0.1-r0.apk  
          - xrdp build 時に利用  

インストール方法  
```APKBUILD:title
apk add --update --no-cache ./neutrinordp-libs-1.0.1-r0.apk ./xrdp-0.9.13-r1.apk ./xrdp-openrc-0.9.13-r1.apk --allow-untrusted

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

dockerfileでimageをbuildし、コンテナ起動とともにxrdpを起動するようにしたい場合にはENTRYPOINTを工夫してみてください。
- Linux PAM 認証が不要な場合(sesmanの起動が不要)：
   `ENTRYPOINT ["/usr/sbin/xrdp","-n"] ` と記述  
    
- Linux PAM 認証も使いたい場合：
   `/sbin/rc-service xrdp-sesman start` 実行後、  
    最後に `/usr/sbin/xrdp -n` を実行するshellスクリプトを作成・COPYし、  
   `ENTRYPOINT ["/entriypoint.sh"] ` などと記述  


/etc/xrdp/xrdp.ini を編集し、RDP/VNC 接続時の Linux PAM認証をする場合には
接続許可ユーザを tsusers グループに所属させてください。
```
apk add --update --no-cache linux-pam
addgroup tsusers
adduser -G tsusers -D -H -h /dev/null -s /sbin/nologin -g "xrdp user" <username>
passwd <username>
```
- グループ名を`tsusers`から変更するには /etc/xrdp/sesman.ini を編集してください。

# 既知の不具合
##  日本語キーボードを使っているにも関わらず、ログイン後に接続先が英語キー配列になってしまう。
   NeutrinoRDPモジュールの不具合が原因です。
   ワークアラウンドとして、接続先Windows側のレジストリを変更し、KBDJPN.DLLの代わりに kbd106.dll を定義し、再起動してください。

レジストリエディタを使って以下を
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\00000411


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

## 接続先にログイン後、マウスカーソルが黒い四角になってしまう
  NeutrinoRDPモジュールの不具合が原因です。
   ワークアラウンドとして、接続先Windows側で影を無効にするようにマウスカーソルの設定を変更してください。
```
	[設定]-[デバイス]-[マウス]-[その他のマウスオプション]-[ポインター]
	「ポインターの影を有効にする」のチェックボックスを OFFにする
```

-
