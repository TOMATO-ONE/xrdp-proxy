CentOS 6.8上でX11RDP-rh-matic を利用して作成した NeutrinoRDP-any(RDP-Proxy)を有効にしたxrdp 0.9.13 と 前提となるNeutrinoRDPの RPMです。  
NeutrinoRDPとファイル名が衝突するためにFreeRDPとは共存できません。  
  
X11RDP-rh-matic を使いつつもエラーとなったために無理やりbuildした、darty buildです。  
自分のために作ったのもので無保証です。  
  
  
- 作成方法のメモ
-- xrdp側
CentOS6に対応した最終版のX11RDP-rh-matic v2.0.7を利用  
xrdp.spec.in の内のconfigure オプションを変更し、neutorinordp を有効化  
他patchを追加  
普通に X11RDP-RH-Matic.sh でbuildをすると、xrdp 0.9.13 では FUSEに関するエラーで止まってしまう。  
C11 コンパイラで突破できるが Software Collections(scl) でGCC 4.9 に切替えて実行しても X11RDP-rh-matic が認識しない。
--cleanup オプションは付けずにでエラー後にもソースファイルが残るようにして実行。  
エラー停止後に/tmp以下に残された xrdp.spec , xorgxrdp.spec を回収  
scl enable devtoolset-3 bash を実行後に rpmbuild -ba ./SPEC/xrdp.spec でrpmbを生成。
  
-- NeutrinoRDP側
オリジナルソースに含まれる`freerdp.spec`に手を入れて作成
