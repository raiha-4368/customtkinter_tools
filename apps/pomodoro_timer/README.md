# Timerアプリ
## CustomTkinterを使用したポモドーロタイマーアプリケーション
25分作業 + 5分休憩を繰り返すシンプルなポモドーロタイマーです。


## 実行イメージ
### 実行画面
![実行画面](docs/01_pomodoro.png)

## できること
- 作業 / 休憩の自動切り替え  
- ポモドーロ回数表示  
- スタート / リセット  
- 終了時に通知音  


## 使用技術
- Python
- Custom Tkinter
- Tkinter

## 環境
- Python 3.10 以上(pyファイル)
- Windows(exeファイル)

## 起動及び使用手順
main.exeファイルの実行  
もしくはコマンドプロンプト(対象ディレクトリ下)で以下コマンドを実行  
python main.py  

1. startボタンを押す  
2. 作業開始  
3. 自動で休憩に切り替わります  


## フォルダ構成
<details>
<summary>フォルダ構成(折り畳み)  </summary>

counter_tkinter/  
├─build(build及びdistはexeファイル作成時に自動生成)  
├─dist  
│  └─main.exe  
├─docs  
│  └─01_pomodoro.png (実行時のスクリーンショット各種)  
│	 └─icon_01.ico  
│  └─icon用.png  
├ main.py  
└ README.md  

</details>

## 簡易設計
<details>
<summary>簡易設計(折り畳み)  </summary>

main.py  
	∟init(初期化)  
	∟create_main_frame(初期画面)	
	∟start(スタート)  
	∟reset(リセット)  
	∟update_display(画面更新処理)  
	∟tick(作業中/休憩判定及び切り替え処理)  
	∟toggle_buttons(スタート/リセットボタンの有効化/無効化処理)  
  ∟change_mode(セグメントボタンにより、モードチェンジを行う)  

</details>

## 簡易テスト
### ■正常系
- STARTボタン押下 → タイマー開始 → 25分経過システム音が鳴り5分休憩のサイクルが4回繰り返される

## version履歴
- v1.0.0(2026-04-08)  
	初回リリース  

## 備考
本ツールは個人開発アプリです。  

## 今後の改善(出来ればやりたいと思っていること)
ポモドーロ周期の変更が出来るように改修(ループ回数/作業時間/休憩時間)  
作業及び休憩のタイマー動作時の一時停止と再開  