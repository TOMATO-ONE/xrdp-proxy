# CentOS7用 xrdp

- xrdp-0.9.xx-x.el7.x86_64.rpm             Proxyモード専用時には不要なXvnc や Desktop 環境がインストールされないように依存関係を削除した xrdp  
- xrdp-neutrinordp-0.9.xx-x.x86_64.rpm     RDP-Proxy module ( neutrinordp-any )  
- NeutrinoRDP-libs-devel-x.el7.x86_64.rpm  RDP-Proxy module の動作に必要なlibrary  
- NeutrinoRDP-devel-devel-2.el7.x86_64.rpm RDP-Proxy module のbuildに必要なdevel  

   
    
# 主な利用シーン   
 - CLIのみのCentOS7にRDP-Proxyを実装する場合   
  　GUI関連の依存関係を外しているのでvncやX-Window 関連がインストールされません
```
   yum localinstall xrdp-0.9.xx-x.el7.x86_64.rpm　xrdp-neutrinordp-0.9.xx-x.x86_64.rpm NeutrinoRDP-libs-devel-x.el7.x86_64.rpm
```
 - 既存EPELのxrdpをインストール済みのLinux Desktop に RDP-Proxyを追加する場合   
    EPELのxrdpにadd onとしてインストールできます。 
```
    yum localinstall xrdp-rdpproxy-0.9.xx-x.x86_64.rpm neutrinordp-libs-gitxxxxx-1.el7.x86_64.rpm
```
