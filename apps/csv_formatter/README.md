# csvファイル整形ツール
## CustomTkinterを使用したcsvファイル整形ツール
csvファイルの整形(空白、改行、タブの削除)を行うツール

## 実行イメージ
### 実行画面
![実行画面01](docs/01_csv_formatter(初期画面).png)
![実行画面02](docs/02_csv_formatter(1つ目のファイルを選択).png)
![実行画面03](docs/03_csv_formatter(2つ目のファイルを選択).png)
![実行画面04](docs/04_csv_formatter(逆転).png)
![実行画面04](docs/05_csv_formatter(ファイルへ出力).png)

## できること
- csvファイルの選択、改行及びタブコードを可視化した状態でのプレビュー
- プレビュー結果から空白、改行、タブから任意のものを削除する
- 出力結果のファイル出力

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
python -m apps.csv_formatter.main  

※python -m はPythonモジュールをスクリプト(実行用ファイル)として実行するためのコマンドラインオプション  

1. "ファイルを選択"ボタンを押下でファイルを開くダイアログが開きファイルを選択。
テキストボックス欄に選択したファイル内容が表示される。  
2. 以下任意のチェックボックスにチェックを入れ、プレビューを押下し、整形済みのcsv結果をテキストボックスに出力
・空白(全半角どちらも)を削除する場合はチェックを入れてください
・改行(\n)及びタブ(\t)を削除する場合はチェックを入れてください
3. "ファイルへ出力"ボタンを押下することでファイル保存ダイアログが開き、任意の場所に保存できます。

## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

apps  
├─csv_formatter/  
｜		├─build(build及びdistはexeファイル作成時に自動生成)  
｜		├─dist  
｜		│  └─main.exe  
｜		├─test_dir(テスト実行時に使用するファイル。)  
｜		│  └─改行_タブ入り.csv    
｜		│  └─空白入り.csv    
｜		├─docs  
｜		│  └01_csv_formatter(初期画面).png (実行時のスクリーンショット各種)  
｜		│  └02_ ...  
｜		│  └icon_01.clip(変換前iconファイル)  
｜		│  └icon_01.png(同上)  
｜		├ main.py  
｜		└ icon_01.ico  
｜		└ make_exe.bat  (windows用。実行するとdist以下にexeファイル作成)    
｜		└ README.md  
common
└─共通処理用ディレクトリ  

</details>

## 簡易設計
<details>
<summary>簡易設計(折り畳み)  </summary>

main.py  
	∟init(初期化)  
	∟create_main_frame(初期画面)  
	∟get_filepath(ファイル選択時の処理)  
	∟select_file(ファイルを開き、ファイル情報をget_filepath_1もしくはget_filepath_2に返却)  
	∟csv_preview(オプション設定を適用しながら、csvのpreviewを行う)    
	∟format_for_display(csvを画面表示する際、\nや\t等を表示するためエスケープする処理)  
	∟subject_replace(受け取ったlistの文字列を消すreplace処理)  
	∟apply_and_refresh(どのreplace処理を行うかの判定)  
	∟along_csv_columns(scvの列ごとに要素の最長文字列に合わせて空白を入れる。全角半角や文字列によって空白を入れる意味がないようなので作成してみたが未使用)  
	∟output_file(ファイルへの出力)  
	∟fileselect_clear(テキストボックスをクリアする処理)  
	∟clear_data(全ての入力状況をクリア)  

</details>

## 簡易テスト
### ■正常系
- csvファイルを選択 → テキストボックスに表示 → 空白削除にチェック → プレビュー → ファイル出力 
- csvファイルを選択 → テキストボックスに表示 → 改行/タブ削除にチェック → プレビュー → ファイル出力 
- csvファイルを選択 → テキストボックスに表示 → 空白、改行/タブ削除にチェック → プレビュー → ファイル出力 

### ■異常系
- ファイルを選択せずにプレビュー → エラーメッセージが表示
- ファイルを選択せずにファイルへ出力 → エラーメッセージが表示

## version履歴
- v1.0.0(2026-04-22)  
	初回リリース  
	
## 備考
本ツールは個人開発アプリです。  

## 今後の改善案(実装未定)
replace処理の汎用化  
差分プレビュー  