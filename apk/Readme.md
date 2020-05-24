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
$ sudo apk add --update --no-cache ./neutrinordp-libs-1.0.1-r0.apk ./xrdp-0.9.13-r1.apk ./xrdp-openrc-0.9.13-r1.apk --allow-untrusted
```
