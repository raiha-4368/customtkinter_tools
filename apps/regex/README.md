# Regexツール
## CUstomTkinterを使用した正規表現を行うRegexツール
記述した文字に対して、正規表現を行うツールです

## 実行イメージ
### 実行画面
![実行画面](docs/01_regex(初期画面).png)
![実行画面](docs/02_regex(正規表現、対象の入力).png)


## できること
- 入力値で正規表現を行った結果を表示します  

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
python -m apps.regex.main  

※python -m はPythonモジュールをスクリプト(実行用ファイル)として実行するためのコマンドラインオプション  

1. 入力データおよび正規表現を入力  
2. 検索結果欄に正規表現後が表示

## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

apps  
├regex 
│		├─build(build及びdistはexeファイル作成時に自動生成)  
│   ├── dist  
│   │   └── main.exe  
│   ├── doc  
│   │   ├── 01_regex(初期画面).png  (実行時のスクリーンショット各種)   
│   │   ├── 02_regex(正規表現、対象の入力).png  
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
	∟ regex_exe(keyのバインドで正規表現の実行)  
	∟ error_mang(正規表現、入力データの未入力チェック)  

</details>

## 簡易テスト
### ■正常系
- 入力データ及び正規表現(一致あり)を入力 → 検索結果欄に一致した文字が表示

### ■異常系
- 入力データ及び正規表現(一致無し)を入力 → 検索結果欄に一致はありませんと表示

## version履歴
- v1.0.0(2026-05-11)  
	初回リリース  

## 備考
本ツールは個人開発アプリです。  

## 今後の改善
ファイルを選択し、正規表現を行えるようにする  
一致箇所の置換処理    