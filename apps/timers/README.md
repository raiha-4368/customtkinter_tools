# Timersツール
## CUstomTkinterを使用したTimerツール
Countdownツール、Stopwatchツール、PomodororTimerツールを複合したツール

## 実行イメージ
### 実行画面
![実行画面](docs/01_timers(Countdown).png)
![実行画面](docs/02_timers(Stopwatch).png)
![実行画面](docs/03_timers(Pomodoro).png)


## できること
- Countdownタイマーの使用
- Stopwatchの使用
- Pomodoroタイマーの使用  

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
python -m apps.timer.main  

※python -m はPythonモジュールをスクリプト(実行用ファイル)として実行するためのコマンドラインオプション  

1. 左側のメニューで使用するタイマーをボタンで選択(デフォルトはCoutdown)  
2. 右側に表示されている各タイマーを使用する

## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

apps  
├timers 
│		├─build(build及びdistはexeファイル作成時に自動生成)  
│   ├── dist  
│   │   └── main.exe  
│   ├── doc  
│   │   ├── 01_timers(Countdown).png  (実行時のスクリーンショット各種)   
│   │   ├── 02_timers(Stopwatch).png  
│   │   ├── 03_timers(Pomodoro).png  
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
	∟***** class NavigationFrame(サイドメニュー用) *****
	∟__init__(初期化、画面のウェジット生成)  
	∟ change_mode(サイドメニュー下部にあるモードチェンジ処理)  
 │ 	
	∟***** class Countdown(Countdownタイマー用) *****
	∟__init__(初期化、画面のウェジット生成)  
	∟add_countdown_minutes(ボタン押下時、タイマーに1分追加)	
	∟add_countdown_ten_seccond(ボタン押下時、タイマーに10秒追加)	
	∟add_countdown_one_seccond(ボタン押下時、タイマーに1秒追加)	
	∟countdown_time_view(上記追加したタイマーの時間を整形(00:00.000の形式))	
	∟update_time(タイムの更新処理。afterによりstartを押した間10ミリ秒毎に更新を行う)  
	∟start(開始時間を取得し、update_timeを実行)  
	∟stop(今までの経過時間を取得し、after_cancelでupdate_timeの処理を止める)  
	∟reset(タイマーの設定時刻及び、開始時間/経過時間を初期化)  
	∟toggle_buttons(1分/10秒/1秒ボタン及び、start/stopボタン押下時にボタンの有効化/無効化を切り替える)  
 │ 	
	∟***** class Stopwatch(Stopwatch用) *****
	∟__init__(初期化、画面のウェジット生成)  
 	∟create_widgets(初期画面)	
	∟update_time(タイムの更新処理。afterによりstartを押した間10ミリ秒毎に更新を行う)  
	∟start(開始時間を取得し、update_timeを実行)  
	∟stop(今までの経過時間を取得し、after_cancelでupdate_timeの処理を止める)  
	∟reset(開始時間及び、経過時間を初期化)  
	∟toggle_buttons(start及びstopボタン押下時にボタンの有効化/無効化を切り替える)  
 │ 	
	∟***** class Pomodoro(Pomodoroタイマー用) *****
	∟__init__(初期化、画面のウェジット生成)  
 	∟start(スタート)  
	∟reset(リセット)  
	∟update_display(画面更新処理)  
	∟tick(作業中/休憩判定及び切り替え処理)  
	∟toggle_buttons(スタート/リセットボタンの有効化/無効化処理)  
  ∟change_mode(セグメントボタンにより、モードチェンジを行う)  
 │ 	
	∟***** class TimersApp(起動用) *****
	∟__init__(各画面の生成を行う)  
	∟select_frame(指定された名前のframeを表示し、他を隠す)  

</details>

## 簡易テスト
### ■正常系
- 左側のメニューでCountdownを選択 → Countdownタイマーが正常に動作する
- 左側のメニューでStopwatchを選択 → Stopwatchが正常に動作する
- 左側のメニューでPomodoroを選択 → Pomodoroタイマーが正常に動作する

## version履歴
- v1.0.0(2026-05-11)  
	初回リリース  

## 備考
本ツールは個人開発アプリです。  

## 今後の改善
処理の見直し  
UIの改善等   