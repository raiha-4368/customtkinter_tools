# CSVビューアアプリ
## tkinterを使用したCSVビューアアプリケーション
csvファイルのビューア用アプリです。
※csvファイルは見出し行と列が対応している前提です。

## 実行イメージ
### 実行画面
![実行画面_初期](docs/01_csv_viewer.png)
![実行画面_正常](docs/02_csv_viewer_success.png)
![実行画面_エラー](docs/03_csv_viewer_error.png)

## できること
- csvファイルを開き、その内容を表示する(編集不可)  

## 使用技術
- Python
- Custom Tkinter
- Tkinter

## 環境
- Python 3.10 以上(pyファイル)
- Windows(exeファイル)


## 起動及び使用手順
main.exeファイルの実行  
もしくはコマンドプロンプト(対象ディレクトリ下)で以下コマンドを実行  
python main.py  

1. ファイルを選択ボタンを押す  
2. ファイルを選択  
3. 表で表示されます
※見出し列(カラム)に対して要素となる行が多い時、その多い行は表示されません。  


## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

csv_viewer/  
├─build(build及びdistはexeファイル作成時に自動生成)  
├─dist  
│  └─main.exe  
├─docs  
│  └─01_csv_viewer.png (実行時のスクリーンショット各種)  
│  └─  ...  
│  └icon_01.clip(変換前iconファイル)  
│  └icon_01.png(同上)  
├ main.py  
└ icon_01.ico  
└ README.md  

</details>

## 簡易設計
<details>
<summary>簡易設計(折り畳み)  </summary>

main.py  
	∟init(初期化)  
	∟create_main_frame(初期画面)	
	∟import_file(csvファイルの読み込み/表示処理)  

</details>

## 簡易テスト
### ■正常系
csvファイル選択→テキストボックス欄にcsv内容が表示される

### ■異常系
行列が一致しないcsvファイル選択→テキストボックス欄にcsv内容が表示されるが、画面下部に警告文が表示される

## version履歴
- v1.0.0(2026-04-09)  
	初回リリース  

## 備考
本ツールは個人開発アプリです。  

## 今後の改善
customtkinterにTreeviewがない為、tkinterでの実装となっている  
UIを整理し、customtkinterらしい見た目にしたい      