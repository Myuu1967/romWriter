# romWriter

今回製作したROMライターは趣味レベルの試作品です。
一応ROMの中身を読んだりデータを書き込んだりできましたが、品質は素人レベルです。  
実用に耐えるものではないことをご承知おきください。
  
このリポジトリの構成  
・README.md &emsp; このファイル  
romWriterというフォルダー  
ROMというフォルダー  
 romWriterの中  
   .gitignore &emsp; &emsp; 追跡しないファイルが書かれている  
   PCsideというフォルダー
   RomReader.py &emsp; ROMを読むためのソースコード。ラズベリーパイPico内のコード  
   RomWriter.py &emsp; &emsp; ROMにデータを書き込むためのソースコード。ラズベリーパイPico内のコード  
   RomWriter00.csv &emsp; ROMライターの回路を構成する部品の部品表（名称が分かりにくくてすみません。汗）  
   RomWriter00.pdf &emsp; ROMライターの回路の回路図。KiCAD8にて書かれている（同上）  
   RomWriter02.py &emsp; &emsp; RomWriter.pyのニューバージョン。RomWriter.pyで書き込んだところ、エラーが多数出たので前のに戻した。ラズベリーパイPico内のコード  
   checkFFRom.py &emsp; &emsp; Romのデータが0xFF（消去済み）かどうかをチェックするツール。（0~255の値が繰り返されているかもチェックできる）  

  フォルダーROMの中身  
  各種画像ファイル  
  
  PCsideの中身  
   RomUart.py &emsp; &emsp;  読み込んだデータをPC側でUARTにて受信するためのソースコード。PC側にて動く。受信したデータはフォルダーdataの中に保存される  
   detectErrordData.py &emsp; 書き込んだ値と実際のROMのデータを比べて、エラーをチェックするコード  
   hexDump.py &emsp; &emsp; 保存してあるデータのダンプリストを出力するコード。romDump.batと組み合わせて使用する  
   rom_dump.bat &emsp; &emsp; ダンプリストを表示させるときに使うバッチファイル。中を見れば使用法は理解できるかと思います。  
   sendRomDataToPico &emsp; 書き込むデータをPC側からラズベリーパイPico側に送信するのソースコード  
   dataの中身
     保存したバイナリーファイル。読み取ったROMのデータ。rom_dump.batを使って中身が見れる（直接何かのアプリケーションで開くのは危険かもしれないです）
