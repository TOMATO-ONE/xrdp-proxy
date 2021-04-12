# xrdp-proxy
xrdp with NeutrinoRDP proxy module

RDP Proxy (NeutrinoRDP-any)モジュールを有効にした、xrdp  です。  
Apache GUACAMOLE のように Microsoft Windows の RDP プロトコルのProxy として動作します。  
  
xrdpはRDPプロトコルでLinux GUIに接続するソリューションとして多くのディストリビューションで採用されています。  
xrdpはRDP Proxyとして動作する NeutrinoRDP-any モードを持っていますが、ほとんどのディストリビューションでは利用できません。  
xrdp.ini の [NeutrinoRDP-Any] セクションを有効にしても、動作に必要な libxrdpneutrinordp.so が同梱されていないためです。   
   
FreeRDP 1.0.1 からforkしたNeutrinoRDPは、libファイル名が同じながらAPIが非互換なため、FreeRDP 1.0.2以降と共存できないこと、   
また、xrdpは主にWindowsクライアントからLinux Desktopへの GUIログインを目的として使われることが多く、RDP Proxyの使用頻度が少ないことが理由と思われます。   
   
ここにあるのは libxrdpneutrinordp.so を同梱しRDP Proxy として動作するようにした xrdp で、以下のものを置いています。  
   
- CentOS 7 用RPMバイナリパッケージ(x86_64)、SRPMソースパッケージ
- Alpine Linux 3.xx 用APKバイナリパッケージ(x86_64,arm,arch64)、srcパッケージ
- Dockerコンテナbuild用 dockerfile

docker imageは docker hub でも 公開しています。  
https://hub.docker.com/r/junkertomato/xrdp-proxy
  
xrdp  
http://xrdp.org/
