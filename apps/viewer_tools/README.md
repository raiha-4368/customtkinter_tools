# ※途中!!!!


# viewerツールの集合ツール
## CustomTkinterを使用したビューア系ツールの集合
各種ファイルビューアのツール


## 実行イメージ
### 実行画面
![実行画面](docs/01_viewere_tools(初期画面).png)
![実行画面](docs/02_viewere_tools(Diff).png)
![実行画面](docs/03_viewere_tools(Regex).png)
![実行画面](docs/04_viewere_tools(Treeviewer).png)
![実行画面](docs/05_viewere_tools(Csv).png)
![実行画面](docs/06_viewere_tools(Json).png)
![実行画面](docs/07_viewere_tools(Xml).png)
![実行画面](docs/08_viewere_tools(DB).png)


## できること
-  以下Toolsを内包
### Tools
- Diff  
- Regex
- Tree Viewer
- Csv Viewer
- Json Viewer
- Xml Viewer
- DB Viewer


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
python -m apps.viewer_tools.main  

※python -m はPythonモジュールをスクリプト(実行用ファイル)として実行するためのコマンドラインオプション  

1. 対象ファイルを選択ボタンを押下  
2. ツリービューxmlファイルの内容が表示される

## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

apps  
├viewer_tools   
│		├─build(build及びdistはexeファイル作成時に自動生成)  
│   ├── dist  
│   │   └── main.exe  
│   ├── doc  
│   │   ├── 01_viewere_tools(初期画面).png  
│   │   ├── 02_viewere_tools(Diff).png  
│   │   ├── 03_viewere_tools(Regex).png  
│   │   ├── 04_viewere_tools(Treeviewer).png  
│   │   ├── 05_viewere_tools(Csv).png  
│   │   ├── 06_viewere_tools(Json).png  
│   │   ├── 07_viewere_tools(Xml).png  
│   │   ├── 08_viewere_tools(DB).png  
│   │   ├── icon_01.clip(変換前iconファイル)  
│   │   └── icon_01.png(同上)  
│		├── csv_viewer.py  
│		├── db_viewer.py  
│		├── diff.py  
│		├── icon_01.ico  
│		├── json_viewer.py  
│		├── main.py  
│		├── make_exe.bat  
│		├── README.md  
│		├── regex.py  
│		├── treeviewer.py  
│		└── xml_viewer.py  
common   
└─共通処理用ディレクトリ  

</details>

## 簡易設計
<details>
<summary>簡易設計(折り畳み)  </summary>

#### ※インスタンス関数に関しては記述中 

main.py  
	∟**********  class NavigationFrame  **********  
	∟__init__(初期化、frame生成)  
	∟ change_mode(サイドメニュー下部にあるモードチェンジ処理)  
	∟**********  class ViewerTools  **********
	∟__init__(初期化、frame生成)  
	∟select_frame  

diff.py  
	∟**********  class DifffilesApp  **********  
	∟__init__()  
	∟get_diff_file1()  
	∟get_diff_file2()  
	∟select_file()  
	∟preview()  
	∟diff_preview()  
	∟check_diff()  
	∟diff_only_preview()  
	∟change_content()  
	∟check_text_diff()  
	∟change_content_text()  
	∟clear()  

regex.py  
	∟**********  class RegexApp  **********  
	∟__init__()  
	∟regex_exe()  
	∟error_mang()  

treeviewer.py  
	∟**********  class TreeCommandApp  **********  
	∟__init__()  
	∟select_dir()  
	∟display_tree()  
	∟clear()  

csv_viewer.py  
	∟**********  class CsvViewerApp  **********  
	∟__init__()  
	∟import_file()  
	∟clear()  


json_viewer.py  
	∟**********  class JsonViewerApp  **********  
	∟__init__()  
	∟select_json()  
	∟explore_json()  
	∟clear()  

xml_viewer.py  
	∟**********  class XmlViewerApp  **********  
	∟__init__()  
	∟select_xml()  
	∟add_xml_to_tree()  
	∟clear()  

db_viewer.py  
	∟query_exe  
	∟**********  class DBViewerApp  **********  
	∟__init__()  
	∟show_frame()  
	∟**********  class SelectPage  **********  
	∟__init__()  
	∟select_file()  
	∟**********  class SqlPage  **********  
	∟__init__()  
	∟update_label()  
	∟textbox_sql()  
	∟update_listbox()  
	∟select_table()  
	∟**********  class ResultPage  **********  
	∟__init__()  
	∟update_label()  
	∟update_listbox()  
	∟show_structure()  
	∟show_data()  


</details>

## 簡易テスト
### ■正常系
- ツール選択ボタンを押下 → 対象ツールが使えること

## version履歴
- v1.0.0(2026-05-21)  
	初回リリース  

## 備考
本ツールは個人開発アプリです。  

## 今後の改善
その他、必要なツールの追加    
UIの改善等  