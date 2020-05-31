### Dockerfileの使い方(imagebuild方法)
```
docker build -t junkertomato/xrdp-proxy:latest https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/docker/dockerfile
```
`entrypoint.sh`はdockerfileからダウンロードして使われる。

### docker image のsave方法
ファイルURLリンク切れでbuildできなくなった時の為にdocker saveでimageを保存しておく。
```
docker save junkertomato/xrdp-proxy:0.9.13 | xz -c > xrdp-proxy.0.9.13.tar.xz
```
### 保存した docker image の利用方法
```
cat xrdp-proxy.0.9.13.tar.xz | xz -d | docker load
```
