# RockyLinux8/Almalinux8/CentOS8 用 RDP Proxy対応 xrdp 

- xrdp-0.9.xx-x.el8.x86_64.rpm             Proxyモード専用時には不要なXvnc や Desktop 環境がインストールされないように依存関係を削除した xrdp  
- xrdp-rdpproxy-0.9.xx-x.el8.x86_64.rpm     RDP-Proxy module ( neutrinordp-any )  
- neutrinordp-libs-devel-x.el8.x86_64.rpm  RDP-Proxy module の動作に必要なlibrary  
- neutrinordp-devel-devel-2.el8.x86_64.rpm RDP-Proxy module のbuildに必要なdevel  

   
    
# インストール方法   
 - CLIのみのlinuxにRDP-Proxyを実装する場合   
  　GUI関連の依存関係を外しているのでvncやX-Window 関連がインストールされません
```
   yum localinstall xrdp-0.9.xx-x.el8.x86_64.rpm　xrdp-rdpproxy-0.9.xx-x.el8.x86_64.rpm neutrinordp-libs-devel-x.el8.x86_64.rpm
```