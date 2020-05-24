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

/etc/xrdp/xrdp.ini を編集し、RDP/VNC 接続時の Linux PAM認証をする場合には
接続許可ユーザを tsusers グループに所属させてください。
```
apk add --update --no-cache linux-pam
addgroup tsusers
adduser -G tsusers -D -H -h /dev/null -s /sbin/nologin -g "xrdp user" <username>
passwd <username>
```
- グループ名をtsusersから変更するには /etc/xrdp/sesman.ini を編集してください。

