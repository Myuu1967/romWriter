# romWriter
このリポジトリの構成
・README.md　　このファイル
romWriter    ソースコードなどが入っているフォルダー
 romWriterの中
   .gitignore    追跡しないファイルが書かれている
   RomReader.py    ROMを読むためのソースコード。ラズベリーパイPico内のコード
   RomUart.py      読み込んだデータをPC側でUARTにて受信するためのソースコード。PC側にて動く
   RomWriter.py    ROMにデータを書き込むためのソースコード。ラズベリーパイPico内のコード
   RomWriter00.csv    ROMライターの回路を構成する部品の部品表（名称が分かりにくくてすみません。汗）
   RomWriter00.pdf    ROMライターの回路の回路図。KiCAD8にて書かれている（同上）
