# Docker コンテナへのインストールと実行

## RDP/VNC Proxyとしての基本的な実行方法 

### alpine 3.11 コンテナの起動
```
docker run -itd -p 3389:3389 --name xrdp-proxy alpine:3.11 sh
```
### コンテナへのapkインストール
```
docker exec -t xrdp-proxy wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.11/x86_64/neutrinordp-libs-1.0.1-r0.apk -P /tmp/
docker exec -it xrdp-proxy wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.11/x86_64/xrdp-0.9.13-r1.apk -P /tmp/
docker exec -it xrdp-proxy apk add --update --no-cache /tmp/neutrinordp-libs-1.0.1-r0.apk /tmp/xrdp-0.9.13-r1.apk --allow-untrusted 
docker exec -it xrdp-proxy rm -i /tmp/neutrinordp-libs-1.0.1-r0.apk /tmp/xrdp-0.9.13-r1.apk
```
### xrdp を実行
```
docker exec -itd xrdp-proxy /usr/sbin/xrdp -n
```
Windowsの「リモートデスクトップ接続」`mstsc.exe `でホストOSのIPアドレスに接続するとxrdpのダイアログが表示されます。  
  
### xrdp.iniを編集する場合
```
docker exec -it xrdp-proxy sh
(コンテナ内)
vi /etc/xrdp/xrdp.ini
exit
```
xrdpではクライアントの接続ごとにxrdp.iniが読みこまれる仕様のためxrdpの再起動は不要です。  
  

## Linux PAM認証を併用する場合　　
Proxy先のOS側の認証に加えて xrdp側でLinux PAMを用いたユーザ認証を行う場合には`xrdp-sesman`を起動させる必要があります。 
xrdp-sesmanだけが起動するコンテナを起動し、連携させるのがdocker本来のあり方ですが、  
単一コンテナ内で二つのサービスを起動させるためには以下のようにします。  
  
### alpine 3.11 コンテナの起動 (ホストOS側のcgroupをマウント)
```
docker run -itd -p 3389:3389 -v /sys/fs/cgroup:/sys/fs/cgroup --name xrdp-proxy alpine:3.11 sh
```
### apkインストール
```
docker exec -it xrdp-proxy apk add --update --no-cache openrc linux-pam
docker exec -it xrdp-proxy wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.11/x86_64/neutrinordp-libs-1.0.1-r0.apk -P /tmp/
docker exec -it xrdp-proxy wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.11/x86_64/xrdp-0.9.13-r1.apk -P /tmp/
docker exec -it xrdp-proxy wget https://github.com/TOMATO-ONE/xrdp-proxy/raw/devel/alpine/3.11/x86_64/xrdp-openrc-0.9.13-r1.apk -P /tmp/
docker exec -it xrdp-proxy apk add --update --no-cache /tmp/neutrinordp-libs-1.0.1-r0.apk /tmp/xrdp-0.9.13-r1.apk /tmp/xrdp-openrc-0.9.13-r1.apk --allow-untrusted 
docker exec -it xrdp-proxy rm -i /tmp/neutrinordp-libs-1.0.1-r0.apk /tmp/xrdp-0.9.13-r1.apk /tmp/xrdp-openrc-0.9.13-r1.apk
```
### OpenRCを起動できるようにするための修正とxrdp-sesmanの起動登録
```
docker exec -it xrdp-proxy sed -i 's/#rc_sys=""/rc_sys="lxc"/g' /etc/rc.conf
docker exec -it xrdp-proxy sed -i 's/^#rc_provide="!net"/rc_provide="loopback net"/' /etc/rc.conf
docker exec -it xrdp-proxy sed -i '/getty/d' /etc/inittab
docker exec -it xrdp-proxy sed -i 's/mount -t tmpfs/# mount -t tmpfs/' /lib/rc/sh/init.sh
docker exec -it xrdp-proxy sed -i 's/hostname $opts/# hostname $opts/' /etc/init.d/hostname
docker exec -it xrdp-proxy mkdir -p /run/openrc
docker exec -it xrdp-proxy touch /run/openrc/softlevel
docker exec -it xrdp-proxy rc-status
docker exec -it xrdp-proxy rc-update add xrdp-sesman
```
### xrdp.ini の編集  
```
docker exec -it xrdp-proxy sh
```
コンテナ内で`vi /etc/xrdp/xrdp.ini`で編集します。  
[RDP-Proxy-PAM]と[VNC-Proxy-PAM]のエントリをコメントアウトするとLinuxコンテナ側でのユーザ認証を行えるようになります。  
  
全てのパラメータ値を`ask`にするとダイアログボックス表示が破綻します。  
一部を固定値にしてダイアログに表示させないようにするか、`xrdp.ini` 117行目～のGUIパラメータを適宜編集してください。  
編集後、`exit`でコンテナ内から抜けます。

### xrdp-sesmanと xrdp の起動
```
docker exec -it xrdp-proxy rc-service xrdp-sesman start
docker exec -itd xrdp-proxy /usr/sbin/xrdp -n
```
### RDP接続を許可するグループ`tsusers`とユーザの作成
```
docker exec -it xrdp-proxy addgroup tsusers
docker exec -it xrdp-proxy adduser -G tsusers -D -H -h /dev/null -s /sbin/nologin -g "xrdp user" <username>
docker exec -it xrdp-proxy passwd <username>
```
グループ名をtsusersから変更するには `/etc/xrdp/sesman.ini` を編集してください。


## ログファイルについての考慮
ログファイルはコンテナ内に蓄積されてしまいます。  
以下のようにvolumeを指定してホストOS側のディレクトリにログを書き出すようにコンテナを起動します。
```
mkdir ./log/
docker run -itd -p 3389:3389 -v /sys/fs/cgroup:/sys/fs/cgroup -v ${PWD}/log:/var/log --name xrdp-proxy alpine:3.11 sh
```

### ホストOS側に置いたxrdp.ini を参照させたい  
コンテナ起動のたびにコンテナ内の`xrdp.ini`を修正するのが面倒な場合には、ホストOS側に`xrdp.ini`を置き、以下のようにして参照させてください。
```
docker run -itd -p 3389:3389 -v /sys/fs/cgroup:/sys/fs/cgroup -v ${PWD}/log:/var/log -v ${PWD}/xrdp.ini:/etc/xrdp/xrdp.ini --name xrdp-proxy alpine:3.11 sh
```
※なお、コンテナ起動後にホストOS側の`xrdp.ini`を編集しても反映されません。
