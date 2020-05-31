### Dockerfileの使い方(imagebuild方法)
```
docker build -t junkertomato/xrdp-proxy:latest https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/docker/dockerfile
```


### docker save image の生成方法
```
docker save junkertomato/xrdp-proxy:0.9.13 | xz -c > xrdp-proxy.0.9.13.tar.xz
```

