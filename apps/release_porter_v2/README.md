# リリース用まとめツール
## CustomTkinterを使用したリリース用まとめるツール
custom_tkinter_toolsリポジトリ内のツールを展開用にまとめるツール  
release_porterからUIを大きく変えた為、v2とし、新ツールとした

## 実行イメージ
### 実行画面
![実行画面](docs/01_release_porter_v2(初期画面).png)

## できること
- 選択したフォルダ・ファイルを一つのファイルにまとめてコピーする  

## 使用技術
- Python
- Custom Tkinter
- Tkinter

## 環境
- Python 3.10 以上(pyファイル)

## 起動及び使用手順
コマンドプロンプト(プロジェクトルート)で以下コマンドを実行  
python -m apps.release_porter_v2.main  

※1. python -m はPythonモジュールをスクリプト(実行用ファイル)として実行するためのコマンドラインオプション  
※2. 当プログラムはconfig実装によるフォルダ構成の影響でexe化したものの動作が出来ていません。

1. 選択フォルダ内リストから対象を選択   
2. フォルダ保存ダイアログが開くので保存先を選択
3. 2.の選択フォルダにconfig設定したファイル・フォルダが保存される   

#### config.iniの設定
- 以下フォルダ(プロジェクトルートからみたパスを設定)内のリストを表示
path = apps

- 以下のリストでコピー元を設定。> がある場合右辺に記述することでコピー元からフォルダ構成を変更する。
release_list = 
    apps/{target_src}/main.py
    apps/{target_src}/icon_01.ico
    common
    apps/{target_src}/dist/main.exe > main.exe

## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

apps  
├release_porter_v2  
│		├─build(build及びdistはexeファイル作成時に自動生成)  
│   ├── dist  
│   │   └── main.exe(動作不可)  
│   ├── doc  
│   │   ├── 01_release_porter_v2(初期画面).png  (実行時のスクリーンショット各種)   
│   │   ├── icon_01.clip(変換前iconファイル)  
│   │   └── icon_01.png(同上)  
│   ├── config.ini  
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
	∟get_base_path(実行ディレクトリを取得する。現在未使用)  
	∟********** class ReleasePorterApp **********   
		∟__init__(初期化、frame生成)  
		∟ create_main_frame(フレーム内の要素を生成)  
		∟show_release_list(config設定箇所のリストを取得し、表示)  
		∟folder_porter(フォルダ名が押下されたとき、フォルダ保存ダイアログ、保存処理を行う)  

</details>

## 簡易テスト
### ■正常系
- apps以下のすべてのフォルダがボタン表示されている
- フォルダ名のボタンを押下 → フォルダ保存ダイアログ → config.iniで設定されているファイル・フォルダが保存されている

## version履歴
- v1.0.0(2026-05-15)  
	初回リリース  

## 備考
本ツールは個人開発アプリです。  

## 今後の改善
exe化についての対応  
 ∟実行ディレクトリが変わることでフォルダ構成がプログラム内と異なってしまうのでexe化できていない

追加したい機能  
- 自動zip化  
- pyinstallerの実行  