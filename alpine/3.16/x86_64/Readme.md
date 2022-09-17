# xrdp-proxy
NeutrinoRDP-any(RDP Proxy)モジュールを有効にした、Alpine Linux 3.16 用 xrdp binary packageです。  
xrdpはAlpine Linuxに標準のxrdp から configure optionを変更して生成しています。  
NeutrinoRDPは FreeRDPのABUILDファイルを流用して生成しています。

- xrdp  
  - xrdp-0.9.20-r1.apk  
        - NeutrinoRDP-anyモジュールを有効にしたxrdp本体  
  - xrdp-openrc-0.9.20-r1.apk  
        - openrc 用 initスクリプト  
  - xrdp-doc-0.9.20-r1.apk  
  - xrdp-dev-0.9.20-r1.apk  

* NeutrinoRDP  
   - neutrinordp-libs-836b738-r1.apk      
   - neutrinordp-plugins-836b738-r1.apk     
   - neutrinordp-836b738-r1.apk  
          - RDP client "xfreerdp" xrdp-proxyには不要  
   - neutrinordp-dev-836b738-r1.apk  
          - xrdp build 時に利用  

インストール方法  
```APKBUILD:title
apk add --update --no-cache ./neutrinordp-libs-836b738-r1.apk ./xrdp-0.9.20-r1.apk ./xrdp-openrc-0.9.20-r1.apk --allow-untrusted

apk add --update --no-cache openrc 
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
- グループ名を`tsusers`から変更するには /etc/xrdp/sesman.ini を編集してください。

```

