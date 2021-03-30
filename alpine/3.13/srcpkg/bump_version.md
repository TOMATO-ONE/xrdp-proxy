# apk バージョンアップ手順
```
1.srcpkg を展開しABUILDを編集。  
2.バージョン番号、source URLなどを書き換える  
3.新しいsource で patch を適用し可能か確認する。  
   patch -p1 < 各種patch  
   ./bootstrap  
   ./configure (オプションはABUILD記載のもの)  
   make  
4.ABUILDのhash追加  
   abuild checksum  
5.ABUILD  
   abuild -r  
6.SRCPKG作成  
   abuild srcpkg  
```
 ~/packages/src/ 以下に生成される。  

