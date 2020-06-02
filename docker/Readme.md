# What is this ?
xrdp with NeutrinoRDP.  RDP/VNC Proxy.

NeutrinoRDP-any(RDP Proxy)を有効にしたxrdpのコンテナです。
RDP-Proxy , VNC-Proxy として機能します。

# How to use. 
```
mkdir ./log
docker run -itd -v /sys/fs/cgroup -v $PWD/log -p 3389:3389 --name xrdp-proxy junkertomato/xrdp-proxy
```
リモートデスクトップ接続`mstsc.exe`などでdocker ホストの3389/tcpに接続してください。

# Known issue / 既知の問題
以下を参照
https://github.com/TOMATO-ONE/xrdp-proxy/blob/devel/known%20issue.md#既知の不具合
