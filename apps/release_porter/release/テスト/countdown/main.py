import time
import tkinter as tk
from tkinter import messagebox
import winsound
import customtkinter as ctk

# 外観モードの設定（"System"(OSの設定), "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")


class CountdownApp(ctk.CTk):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):
        super().__init__()

        self.configure(fg_color="#fffacd")
        self.title("Countdown App")
        self.geometry("500x500")
        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = ctk.CTkFrame(self, fg_color="#fffacd")
        self.main_frame.pack()

        #初期表示
        self.create_main_frame()


    # -------------------------
    # メイン画面表示UI
    # -------------------------
    def create_main_frame(self):
        # -------------------------
        # menuの生成
        # -------------------------
        menu_bar = tk.Menu(self)

        self.configure(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="メニュー",menu=file_menu)
        file_menu.add_command(label="終了", command=self.quit)


        # タイマーの初期化処理
        self.start_time = 0
        self.elapsed_time = 0
        self.runningflag = False
        self.after_id = None    #予約したアフター管理用ID

        # カウントダウンタイマー設定時に使用する変数の初期化
        self.minutes_time =  0
        self.seccond_time =  0

        # -------------------------
        # mainフレーム内の要素
        # -------------------------        
        # タイム表示
        self.countdown_label = ctk.CTkLabel(self.main_frame, text="00:00.000", font=("Arial", 40), fg_color="#fffacd",text_color="#000000")
        self.countdown_label.pack(pady=(50.50))

        #コンボボックスで分数設定させる⇒没
        # self.countdown_conbobox = ttk.Combobox(self.main_frame, values=["1分","2分","3分","4分","5分"])
        # self.countdown_conbobox.pack(pady=(20,20))

        # カウントダウンを1分加算(タイマー開始前のみ有効)
        # 分秒設定ボタン横並べの為のフレーム
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="#fffacd")
        self.button_frame.pack()

        self.one_minutes_button = ctk.CTkButton(self.button_frame, text="＋1分", command=self.add_countdown_minutes ,fg_color="#f0ffff", text_color="#000000")
        self.one_minutes_button.pack(side="left", padx=(20,20), pady=(20,20))

        # カウントダウンを10秒加算(タイマー開始前のみ有効)
        self.ten_seccond_button = ctk.CTkButton(self.button_frame, text="＋10秒", command=self.add_countdown_ten_seccond ,fg_color="#f0ffff", text_color="#000000")
        self.ten_seccond_button.pack(side="left", padx=(20,20), pady=(20,20))

        # カウントダウンを1秒加算(タイマー開始前のみ有効)
        self.one_seccond_button = ctk.CTkButton(self.button_frame, text="＋1秒", command=self.add_countdown_one_seccond ,fg_color="#f0ffff", text_color="#000000")
        self.one_seccond_button.pack(side="left", padx=(20,20), pady=(20,20))

        # start
        self.start_button = ctk.CTkButton(self.main_frame, text="START", command=self.start ,fg_color="#fa8072", text_color="#696969")
        self.start_button.pack(side="left", padx=(20,20))
        # stop
        self.stop_button = ctk.CTkButton(self.main_frame, text="STOP",command=self.stop,fg_color="#add8e6", text_color="#696969")
        self.stop_button.pack(side="left", padx=(20,20))

        # reset
        self.reset_button = ctk.CTkButton(self.main_frame, text="RESET", command=self.reset, fg_color="#98fb98", text_color="#696969")
        self.reset_button.pack(side="left", padx=(20,20))

        self.toggle_buttons("default")


    # 1分追加
    def add_countdown_minutes(self):
        self.minutes_time += 1
        self.countdown_time_view()

    # 10秒追加
    def add_countdown_ten_seccond(self):
        self.seccond_time += 10        
        self.countdown_time_view()

    # 1秒追加
    def add_countdown_one_seccond(self):
        self.seccond_time += 1
        self.countdown_time_view()    

    def countdown_time_view(self):
        if 59 < self.seccond_time:
            self.seccond_time = self.seccond_time -60
            self.minutes_time += 1

        self.countdown_time = f"{self.minutes_time:02d}:{self.seccond_time:02d}.000"
        self.countdown_label.configure(text = self.countdown_time)

        self.toggle_buttons("standby")

    def update_time(self):

        # runningフラグが真なら実行
        if self.runningflag:
            # 残り時間 = 設定時間 - 経過時間になるように実装
            # 経過時間を計算= 今の時間 - 開始時の時間
            # 設定時間は60を掛けて秒単位にする
            self.setting_time = self.minutes_time*60 + self.seccond_time

            # 0秒設定なら開始しない
            if self.setting_time == 0:
                return
            
            # # 連打防止(後で必要かもしれないけどコメントアウト)
            # if self.after_id is not None:
            #     return

            # 残り時間を算出
            self.remaining_time = self.setting_time -( time.time() - self.start_time + self.elapsed_time ) 

            # 分ミリ秒整形
            # minutes = int(self.remaining_time // 60)
            # seconds = int(self.remaining_time % 60)
            # millis = int((self.remaining_time - int(self.remaining_time)) * 1000)

            # intは切り捨て roundは四捨五入⇒これでミリ秒のズレを消す
            # remaining_ms = max(0, int(self.remaining_time * 1000))
            remaining_ms = max(0, round(self.remaining_time * 1000))
            minutes = remaining_ms // 60000
            seconds = (remaining_ms % 60000) // 1000
            millis = remaining_ms % 1000

            self.countdown_label.configure(text = f"{minutes:02}:{seconds:02}.{millis:03}")

            if self.remaining_time <= 0:
                # reset処理でも00:00.000としているが、コンマ数秒ずれるようなので、こちらで表示を変える
                self.countdown_label.configure(text = "00:00.000")
                #初期化処理
                self.reset()

                if self.after_id:
                    self.main_frame.after_cancel(self.after_id)
                    self.after_id = None

                # システムアスタリスク音（ポーン）
                winsound.MessageBeep(winsound.MB_ICONASTERISK)

                # 以下、停止時のサウンド候補(残しておく)
                # ビープ音(音の高さ,音の長さ)
                # winsound.Beep(1000,500)

                # 「チャララ〜ン」と階段状に鳴らす
                # for freq in [262, 330, 392, 523]:
                #     winsound.Beep(freq, 200)

            else:
                #10ミリ秒後に自分を呼び出す(このidを持っている限り、after処理を行う)
                self.after_id = self.main_frame.after(10, self.update_time)

    #startを押下してからの時刻を取得
    def start(self):
        if not self.runningflag:
            #トグルボタンで無効にしているので以下の処理は実行されない筈(一応残しておく)
            if self.countdown_label.cget("text") == "00:00.000":
                messagebox.showerror("error", "残り時間が設定されていません。")
                return
            self.runningflag = True
            # 開始時刻を取得 > エポック（通常は1970年1月1日 00:00:00 UTC）からの経過時間を 浮動小数点数（float） で返却
            self.start_time = time.time()
            self.update_time()
            #トグルボタン(時刻を計測している間、ボタンを無効にする)
            self.toggle_buttons("running")

    #stopが押されるまでの時刻を取得、保持
    def stop(self):
        if self.runningflag:
            self.runningflag = False
            # stopを押下するまでの経過時間を取得
            # 今までの経過時間 + 現在の時間 - startボタン押下時間
            self.elapsed_time += time.time() - self.start_time

            #after_cancelで予約を取り消し、idを初期化(None)する
            if self.after_id:
                self.main_frame.after_cancel(self.after_id)
                self.after_id = None
            #トグルボタン(時刻を計測していない間、ボタンを無効にする)
            self.toggle_buttons("stopped")

    def reset(self):
        self.stop()
        self.elapsed_time = 0
        self.countdown_label.configure(text = "00:00.000")
        self.remaining_time = 0
        self.minutes_time = 0
        self.seccond_time = 0

        self.toggle_buttons("reset")

    def toggle_buttons(self, state):
        #ボタンの切り替え
        #カウントダウンラベルがデフォルト表示(00:00.00)であるとき、start/stopボタンを無効化
        if self.countdown_label.cget("text") == "00:00.000" or state == "default" or state == "reset":
            self.start_button.configure(state="disabled",fg_color="#b22222")
            self.stop_button.configure(state="disabled",fg_color="#5f9ea0")
            self.one_minutes_button.configure(state="normal",fg_color="#f0ffff")
            self.ten_seccond_button.configure(state="normal",fg_color="#f0ffff")
            self.one_seccond_button.configure(state="normal",fg_color="#f0ffff")

        # 時間設定のボタンが押されたとき、スタンバイ状態としてstartボタンを有効化
        elif state == "standby":
            self.start_button.configure(state="normal",fg_color="#fa8072")

        # カウントダン中はstartボタン及び、時間設定ボタンを無効化し、stopボタンを有効化
        elif state == "running":
            self.start_button.configure(state="disabled",fg_color="#b22222")
            self.stop_button.configure(state="normal",fg_color="#add8e6")
            self.one_minutes_button['state'] = "disabled"
            self.one_minutes_button.configure(state="disabled",fg_color="#808080")
            self.ten_seccond_button.configure(state="disabled",fg_color="#808080")
            self.one_seccond_button.configure(state="disabled",fg_color="#808080")

        # 一時停止中はstopボタンを無効化し、startボンタンを有効化
        elif state == "stopped":
            self.start_button.configure(state="normal",fg_color="#fa8072")
            self.stop_button.configure(state="normal",fg_color="#5f9ea0")


# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #インスタンス化
    app = CountdownApp()
    #イベント待ちループ開始
    app.mainloop()

