# CountdoenTimerアプリ
## CustomTkinterを使用したカウントダウンタイマー
簡易タイマーツール  
1秒～59分(想定)設定し、時間を計測できます。    

## 実行イメージ
### 実行画面
![実行画面01](docs/01_countdown(未入力).png)
![実行画面02](docs/02_countdown(タイマーセット状態).png)
![実行画面03](docs/03_countdown(タイマー起動中).png)

## できること
- 1秒～59分間の経過時間を計測(任意でストップ/リセット可能)

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
python -m apps.countdown.main  

※python -m はPythonモジュールをスクリプト(実行用ファイル)として実行するためのコマンドラインオプション  


## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

apps/  
├─countdown/  
│		├─build(build及びdistはexeファイル作成時に自動生成)  
│		├─dist  
│		│  └─main.exe  
│		├─docs  
│		│  └01_countdown(未入力).png (実行時のスクリーンショット各種)  
│		│  └02_ ...  
│		│  └icon_01.clip(変換前iconファイル)  
│		│  └icon_01.png(同上)  
│		├ main.py  
│		└ icon_01.ico  
│		└ README.md  
common/  
└─共通処理用ディレクトリ  

</details>

## 簡易設計
<details>
<summary>簡易設計(折り畳み)  </summary>

main.py  
	∟init(初期化)  
	∟create_main_frame(初期画面)	
	∟add_countdown_minutes(ボタン押下時、タイマーに1分追加)	
	∟add_countdown_ten_seccond(ボタン押下時、タイマーに10秒追加)	
	∟add_countdown_one_seccond(ボタン押下時、タイマーに1秒追加)	
	∟countdown_time_view(上記追加したタイマーの時間を整形(00:00.000の形式))	
	∟update_time(タイムの更新処理。afterによりstartを押した間10ミリ秒毎に更新を行う)  
	∟start(開始時間を取得し、update_timeを実行)  
	∟stop(今までの経過時間を取得し、after_cancelでupdate_timeの処理を止める)  
	∟reset(タイマーの設定時刻及び、開始時間/経過時間を初期化)  
	∟toggle_buttons(1分/10秒/1秒ボタン及び、start/stopボタン押下時にボタンの有効化/無効化を切り替える)  

</details>

## 簡易テスト
### ■正常系
- +1分、+10秒、1秒ボタンでタイマーをセット → STARTボタン押下 → カウントダウン開始 → 終了時にシステム音
- タイマーセット状態 → resetボタンでタイマーがリセット

## version履歴
- v1.0.0(2026-04-08)  
	初回リリース  

## 備考
本ツールは個人開発アプリです。  

## 今後の改善
ラベルの数値の変数管理をStringVarを使う方法を試してみたい(ctk.StringVar)  
