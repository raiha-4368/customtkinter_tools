# グラフツール_v1
## CustomTkinter及び、 matplotlibを使用したツール
GUI画面でcsvファイルを選択し、matplotlibを使用しグラフ描画を行います

## 実行イメージ
### 実行画面
![実行画面](docs/01_graph_tool(初期画面_グラフ).png)
![実行画面](docs/02_graph_tool(初期画面_データ).png)
![実行画面](docs/03_graph_tool(ファイル選択後_グラフ).png)
![実行画面](docs/04_graph_tool(ファイル選択後_データ).png)


## できること
- csvファイルを選択し、そのデータを使いグラフ表示を行う  

## 使用技術
- Python
- Custom Tkinter
- Tkinter
- matplotlib

## 環境
- Python 3.10 以上(pyファイル)
- Windows(exeファイル)

## 起動及び使用手順
main.exeファイルの実行
もしくはコマンドプロンプト(プロジェクトルート)で以下コマンドを実行  
python -m apps.graph_tool.main  

※python -m はPythonモジュールをスクリプト(実行用ファイル)として実行するためのコマンドラインオプション  


1. ファイルを選択ボタンを押下し、ダイアログでcsvファイルを選択  
2. グラフタブでグラフが、データタブでcsvデータがツリービューに表示されます

## csvファイルの例
以下のようなcsvファイルを想定
>1回目,2回目,3回目  
25,20,15

## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

apps  
├─graph_tool/  
│		├─build(build及びdistはexeファイル作成時に自動生成)  
│		├─dist  
│		│  └─main.exe  
│		├─docs  
│		│  └─01_graph_tool(初期画面_グラフ).png (実行時のスクリーンショット各種)  
│		│  └─  ...  
│		│  └icon_01.clip(変換前iconファイル)  
│		│  └icon_01.png(同上)  
│		├ main.py  
│		├ main_pandas.py(未完成)  
│		└ icon_01.ico  
│		└ README.md  
common  
└─共通処理用ディレクトリ  

</details>

## 簡易設計
<details>
<summary>簡易設計(折り畳み)  </summary>

main.py  
	∟init(初期化)  
	∟create_main_frame(初期画面)	
	∟import_file(csvファイルの読み込み/グラフ及びツリービューの表示処理)  
	∟on_closing(×ボタンでの終了時、グラフ描画処理が残ってしまわないように終了させる処理)  
	∟change_mode(外観モードチェンジ処理)  

</details>

## 簡易テスト
### ■正常系
csvファイル選択→グラフタブでのグラフ描画及びデータタブでのtreeview表示

## version履歴
- v1.0.0(2026-06-01)  
	初回リリース  

## 備考
本ツールは個人開発アプリです。  

## 今後の改善
軸の変更(x軸↔y軸等)   
pandasモジュールの使用verの作成  
