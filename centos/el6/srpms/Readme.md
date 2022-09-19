CentOS 6.8上でX11RDP-rh-matic を利用して作成した xrdp 0.9.2x と NeutrinoRDPの SRPMです。  
自分のために作ったので無保証です。

build方法

1. NeutrionoRDP を build  
buildに必要packageは以下を参照  
https://github.com/neutrinolabs/NeutrinoRDP/wiki/Compilation  

rpm -Uvh NeutrinoRDP-gitf7832d6-1.el6.src.rpm  
QA_RPATHS=0x0001 rpmbuild -ba --clean rpmbuild/SPECS/neutrinordp.spec  

2.xrdp を build  
buildに必要packageは以下を参照  
https://github.com/neutrinolabs/xrdp/wiki/Building-on-CentOS-(or-Red-Hat-based-distributions)  

SCL3をインストール  
sudo yum install scl-utils devtoolset-3-toolchain devtoolset-3-perftools   
  
先にNeutrinoRDPのlibとdevelをインストール  
sudo yum localinstall NeutrinoRDP-devel-git836b738-1.el6.x86_64.rpm NeutrinoRDP-libs-git836b738-1.el6.x86_64.rpm  
rpm -Uvh xrdp-0.9.2X.xxxxxxx.el6.src.rpm  
  
Software colection で gcc 4.9を有効にする  
scl enable devtoolset-3 bash  
  
rpmbuild -ba --clean ~/rpmbuild/SPECS/xrdp.spec  
  
  
rpm -Uvh xorgxrdp-0.9.2X-1.el6.src.rpm  
rpmbuild -ba --clean ~/rpmbuild/SPECS/xorgxrdp.spec  
  
