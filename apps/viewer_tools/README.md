# ※途中!!!!


# viewerツールの集合ツール
## CustomTkinterを使用したビューア系ツールの集合
各種ファイルビューアのツール


## 実行イメージ
### 実行画面
![実行画面](docs/01_viewere_tools(初期画面).png)


## できること
-  以下Toolsを内包
### Tools
- Regex Tool
- Json Viewer
- Xml Viewer
- Diff Files
- Tree Viewer


## 使用技術
- Python
- Custom Tkinter
- Tkinter

## 環境
- Python 3.10 以上(pyファイル)
- Windows(exeファイル)


## 起動及び使用手順
main.exeファイルの実行
もしくはコマンドプロンプト(プロジェクトルート)で以下コマンドを実行  
python -m apps.xmlviewer.main  

※python -m はPythonモジュールをスクリプト(実行用ファイル)として実行するためのコマンドラインオプション  

1. 対象ファイルを選択ボタンを押下  
2. ツリービューxmlファイルの内容が表示される

## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

apps  
├xmliewer   
│		├─build(build及びdistはexeファイル作成時に自動生成)  
│   ├── dist  
│   │   └── main.exe  
│   ├── doc  
│   │   ├── 01_xmlviewere(初期画面).png  (実行時のスクリーンショット各種)   
│   │   ├── 02_xmlviewere(フォルダ選択).png  
│   │   ├── icon_01.clip(変換前iconファイル)  
│   │   └── icon_01.png(同上)  
│   ├── icon_01.ico  
│   ├── main.py  
│   ├── make_exe.bat  
│   └── README.md  
common   
└─共通処理用ディレクトリ  

</details>

## 簡易設計
<details>
<summary>簡易設計(折り畳み)  </summary>

main.py  
	∟__init__(初期化、frame生成)  
	∟ create_main_frame(フレーム内の要素を生成)  
	∟ select_xml(xmlファイル選択時の処理)  
	∟ add_xml_to_tree(xmlを再帰的に見てtreeviewへの表示する処理)  
	∟ clear(選択状態・表示状態のクリア)  
	∟ change_mode(サイドメニュー下部にあるモードチェンジ処理)  

</details>

## 簡易テスト
### ■正常系
- 対象ファイルを選択でxmlファイルを選択 → ツリービューに表示される

### ■異常系
- 対象ファイルを選択でxmlファイル(構文エラー)を選択 → エラーダイアログが表示される
- 対象ファイルを選択でxmlファイル以外を選択 → エラーダイアログが表示される

## version履歴
- v1.0.0(2026-05-11)  
	初回リリース  

## 備考
本ツールは個人開発アプリです。  

## 今後の改善
階層表示の改善(key,value辺り)   
  