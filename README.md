# Custom Tkinter Tools
## CustomTkinterを使用したツール
CustomTkinterを使用したシンプルなツール達をまとめたリポジトリ  
Tkinterのみで作成したツールは別リポジトリでの管理としています。  

## 使用技術/環境/起動及び使用手順
- それぞれのディレクトリ下にそれぞれ記載  

## Tools
 - contdown  
 時間を設定し、0になるまで時間を計測するツール    

- counter  
 数をカウントするシンプルなツール  

 - csv_viewer  
 csvファイルを開き、その内容を表示する(編集不可)    

- extension_sort  
 ディレクトリを選択し、その直下にあるファイルの拡張子ごとにフォルダに振り分けるツール   

 - memo  
 テキストエリアに記述した内容を保存する/テキストファイルを開きその内容を表示、  
 変更内容を上書き保存できるツール    

 - pomodoro_timer  
 ポモドーロのサイクル(25分作業5分休憩を4回繰り返す)を計ることができるツール    

 - rename_files  
 ディレクトリを選択し、その直下にあるファイル名を一括で変更することができるツール    

- serial_number_files  
 ディレクトリを選択し、その直下にあるフォルダ及びファイルに連番を付与することができるツール   

- stopwatch  
 start/stop/resetができるストップウォッチ  

- text_extract  
 選択したファイル内から任意の文字列を含む行を検索し、抽出するツール  


## Custom tkinterのインストール
以下コマンドを実行  
pip install customtkinter  

## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

custom_tkinter_tools/  
├contdown  
├counter  
├csv_viewer  
├extension_sort  
├memo  
└pomodoro_timer  
└rename_files  
└serial_number_files  
└stopwatch  
└text_extract  
├ .gitignore  
├ 環境構築  
│		∟環境構築時のコマンドラインのテキスト、スクリーンショットを格納  
└ README.md  

</details>

# exe化方法(各フォルダ直下で実行)
■pyinstallerのインストール  
以下コマンドを実行  
pip install pyinstaller   

exe化の方法  
1.以下コマンドを実行  
pyinstaller main.py --onefile  --noconsole --icon=icon_01.ico

使用しそうなオプション  
--onefileは1つのファイルにまとめる  
--noconsoleはコンソールを表示しない  
--icon=test.icoはアイコンを変更(*.iconファイルを同一ディレクトリに配置する)  

2.作業ディレクトリ内にbuildディレクトリ/distディレクトリが作成される  
distディレクトリ内にあるmain.exeをダブルクリックで実行出来るようになっている(筈)  

3.エラーになった場合は  
コンソールからmain.exeを実行し、エラーを確認する(--noconsoleを設定していると出ない可能性あるので注意)  

# icon作成参考
https://qiita.com/Kosen-amai/items/4700100342c76f9fda78  
https://ao-system.net/alphaicon/  

icon作成時の画像  
ぼやける理由⇒.icoは複数サイズを持つ必要がある(16*16, 32*32, 48*48,128*128, '256*256'←最重要)
256*256で作成  
その他の無料ツール候補
icoFX(軽い)
favicon generator系(複数サイズ同時生成)

## version履歴(書き方の方針)
- X:大きな変更
- Y:機能追加
- V:バグ修正
例
- vX.Y.Z  
	初回リリース  
- v1.0.0  
	初回リリース  


## 備考
このリポジトリに含むプログラムは個人開発したものです。  