# リリース用まとめツール
## CustomTkinterを使用したリリース用まとめるツール
custom_tkinter_toolsリポジトリ内のツールを展開用にまとめるツール  
release_porterからUIを大きく変えた為、v2とし、新ツールとした

#### ※README記述まだ途中!!!

## 実行イメージ
### 実行画面
![実行画面](docs/01_release_porterv1(初期画面).png)

## できること
- 選択したフォルダ・ファイルを一つのファイルにまとめてコピーする  

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
python -m apps.release_porter.main  

※python -m はPythonモジュールをスクリプト(実行用ファイル)として実行するためのコマンドラインオプション  

1. 対象プログラムフォルダを選択ボタンを押下  
2. 対象プログラムファイルを選択ボタンを押下
※フォルダ・ファイルは必要なものを選択。どちらかの実行は必須ですが、両方実行の必要はありません。  
3. ツリービューに選択したフォルダ・ファイルが表示されます。
フォルダの中は展開された状態で表示されます。  
4. プレビュー状況で保存するボタンを押下
フォルダ保存のダイアログが開き、選択したフォルダにツリービューのフォルダ・ファイルがまとめてコピー・保存されます  

## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

apps  
├release_porter_v2  
│		├─build(build及びdistはexeファイル作成時に自動生成)  
│   ├── dist  
│   │   └── main.exe  
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
	∟__init__(初期化、frame生成)  
	∟ create_main_frame(フレーム内の要素を生成)  

</details>

## 簡易テスト
### ■正常系


## version履歴
- v1.0.0(2026-05-14)  
	初回リリース  

## 備考
本ツールは個人開発アプリです。  

## 今後の改善
exe化についての対応  
 ∟実行ディレクトリが変わることでフォルダ構成がプログラム内と異なってしまうのでexe化できていない

追加したい機能  
- 自動zip化  
- pyinstallerの実行  