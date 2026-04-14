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
├common						※共通処理  
└apps							※ツール  
│├contdown  
│├counter  
│├csv_viewer  
│├extension_sort  
│├memo  
│├pomodoro_timer  
│├rename_files  
│├serial_number_files  
│├stopwatch  
│├text_extract  
├ .gitignore  
├ 環境構築  
│		∟環境構築時のコマンドラインのテキスト、スクリーンショットを格納  
└ README.md  

</details>

# 各ツールの実行方法
プロジェクトルート(customtkinter_tools直下)で以下コマンドを実行
 python -m apps.{対象のツール}.main

# exe化について
## pyinstallerのインストール  
以下コマンドを実行  
pip install pyinstaller   

## exe化  
1. 各ツールのディレクトリ下にあるmake_exe.batを実行  
2. 作業ディレクトリ内にbuildディレクトリ/distディレクトリが作成  
		dist以下にexeファイルが格納されている
3. エラーになった場合  
exeファイルが実行されない、処理が正常に実行されない等コンソール上のエラーを確認する際は  
bat内ので実行されているコマンドpyinstallerのオプション--noconsoleの設定を外して実行  
その後コンソールからmain.exeを実行すると、コンソールが表示されているのでエラーを確認できます  

## batの中身  
各ツールのディレクトリからプロジェクトルートに移動、pyinstallerコマンドを実行後、元のディレクトリに戻る処理   
cd /d %~dp0\..\..  
pyinstaller apps/{対象のツール}/main.py --onefile  --noconsole --icon=apps/{対象のツール}/icon_01.ico --paths .  
cd /d %~dp0\apps\{対象のツール}  

## 使用しそうなオプション  
--onefileは1つのファイルにまとめる  
--noconsoleはコンソールを表示しない  
--icon=test.icoはアイコンを変更(*.iconファイルを同一ディレクトリに配置する)  
--distpath C:path 任意のパスにexeを出力 or specファイルの編集  
--hidden-import=customtkinter hidden-import問題が出た場合は使用するかもしれないオプション  

※コマンドの補足  
以下をプログラム上に記述することでプロジェクトルートでのexe化処理がやりやすくなるかも？(未実施)  
"import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))"

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