# 既知の不具合
##  日本語キーボードを使っているにも関わらず、ログイン後に接続先が英語キー配列になってしまう。
   NeutrinoRDPモジュールの不具合が原因と思われます。  
   ワークアラウンドとして、接続先Windows側のレジストリを変更し、KBDJPN.DLLの代わりに kbd106.dll を定義・再起動してください。  

### レジストリエディタで変更する方法
レジストリエディタを使って以下のエントリーを探し、  
`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\00000411`  
`Layout File` キーの値を `KBDJPN.DLL` から `kbd106.DLL` に変更  

### コマンドプロンプトで変更する方法
接続先Windowsの管理者権限でコマンドプロンプトを起動し、以下のコマンドを実行してください。
```
# 変更前確認
reg query  "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\00000411" /v "Layout File" 

# レジストリ変更
reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\00000411" /v "Layout File" /d "kbd106.DLL

# 変更後確認
reg query  "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\00000411" /v "Layout File" 

# 再起動実施
shutdown /r 
```

## 接続先にログイン後、マウスカーソルが黒い四角になってしまう
  NeutrinoRDPモジュールの不具合が原因と思われます。
   ワークアラウンドとして、接続先Windows側で影を無効にするようにマウスカーソルの設定を変更してください。
```
	[設定]-[デバイス]-[マウス]-[その他のマウスオプション]-[ポインター]を選択して
	（「ファイル名を指定して実行」またはコマンドプロンプトから  main.cpl ,1  でも可）
	「ポインターの影を有効にする」のチェックボックスを OFFにする
```
 
