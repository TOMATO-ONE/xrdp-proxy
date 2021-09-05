# 既知の不具合
##  日本語キーボードを使っているにも関わらず、ログイン後に接続先が英語キー配列になってしまう。
   v0.9.16 以前のNeutrinoRDPモジュール(libneutrinordp.so)がRDP clientのキーレイアウト情報を送信していないことが原因でした

### xrdp.ini への設定追加での対応方法 (v0.9.17～)
   v0.9.17 以降では xrdp.ini の neutrinordp-any セクションに以下の記述を入れてください。
   xrdp側で認識しているキーレイアウト情報をリモートWindowsに送信するようになります。
   ```
   neutrinordp.allow_client_keyboardLayout=true
   ```
   
### xrdp.ini への設定追加での対応方法 macOSの場合 (v0.9.17～)
   JISキーボードのmacOSでMicrosoft Remotedesktop client を使っている場合は以下の記述をすると正常に使えるようになります。
   ```
   neutrinordp.allow_client_keyboardLayout=true
   neutrinordp.override_kbd_type=0x07
   neutrinordp.override_kbd_subtype=0x02
   neutrinordp.override_kbd_fn_keys=12
   neutrinordp.override_kbd_layout=0x00000411
   ```
   
### リモートWindows側でレジストリエディタでレジストリを変更する方法
 v0.9.16 以前のワークアラウンドとして、接続先Windows側のレジストリを変更し、KBDJPN.DLLの代わりに kbd106.dll を定義する方法があります。
レジストリエディタを使って以下のエントリーを探し、  
`HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Keyboard Layouts\00000411`  
`Layout File` キーの値を `KBDJPN.DLL` から `kbd106.DLL` に変更  

### リモートWindows側でコマンドプロンプトでレジストリを変更する方法
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
  NeutrinoRDPモジュールの不具合が原因でした。
   ワークアラウンドとして、接続先Windows側で影を無効にするようにマウスカーソルの設定を変更してください。

### xrdp.ini への追加設定での対応方法(v0.9.17～)
　v0.9.17以降はxrdp.ini でマウスカーソルの影を無効にできるようになりました。
  xrdo.ini の neutrinordp-any セクションに以下の記述を追加してください。
  ```
  perf.cursor_shadow=false
  ```

### リモートWindows側での対応
```
	[設定]-[デバイス]-[マウス]-[その他のマウスオプション]-[ポインター]を選択して
	（「ファイル名を指定して実行」またはコマンドプロンプトから  main.cpl ,1  でも可）
	「ポインターの影を有効にする」のチェックボックスを OFFにする
```
 
## RDP proxy接続先で背景が真っ黒なまま変更できない
NeutrinoRDPモジュールが壁紙を無効にしていることが原因でした。
Windows10ではユーザー側は背景を変更することはできませんでした。

v0.9.17以降はxrdp.ini で MSTSC.exe のエクスペリエンスタブにあるパフォーマンスの各オプションの設定を反映できるようになりました。
xrdp.ini の  neutrinordp-any セクションに以下の記述を追加してください。
```
perf.allow_client_experiencesettings=true
```

管理者側で強制もできます。
```
perf.wallpaper=(true | false)
perf.font_smoothing=(true | false)
perf.desktop_composition=(true | false)
perf.full_window_drag=(true | false)
perf.menu_anims=(true | false)
perf.themes=(true | false)
perf.cursor_blink=(true | false)
```

