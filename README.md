# xrdp-proxy
xrdp 0.9.13 with NeutrinoRDP proxy module

NeutrinoRDP-any モジュールを有効にした、xrdp 0.9.13 です。  
Apache GUACAMOLE のように Microsoft Windows の RDP プロトコルのProxy として動作します。  
  
xrdpはRDPプロトコルでLinux GUIに接続するソリューションとして多くのディストリビューションで採用されています。  
xrdpはRDP Proxyとして動作する NeutrinoRDP-any モードを持っていますが、ほとんどのディストリビューションで無効化されています。  
RDP Proxy有効化に必要な NeutrinoRDP が FreeRDPと共存できないためと思われます。  
(FreeRDP 1.0.1 からforkしたNeutrinoRDPは、FreeRDP 1.0.2以降とlibファイル名が同じながらAPIが非互換です。)
  
  
そこで、主にdockerでのコンテナ化を目的として、Alpine Linuxのパッケージとdockerfileを作成しました。
  
Alpine Linux 3.11 用  apk / srcpkg パッケージ
docker 用 dockerfile と image アーカイブを置いています。

xrdp  
http://xrdp.org/
