from tkinter import messagebox
import customtkinter as ctk
import winsound
import time

# ======================================================================================================================
class Countdown(ctk.CTkFrame):
    """カウントダウンタイマー"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        label = ctk.CTkLabel(self, text="カウントダウンタイマー")
        label.pack()
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
        self.countdown_label = ctk.CTkLabel(self, text="00:00.000", font=("Arial", 40), fg_color="transparent")
        self.countdown_label.pack(pady=(50.50))

        # カウントダウンを1分加算(タイマー開始前のみ有効)
        # 分秒設定ボタン横並べの為のフレーム
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack()

        self.one_minutes_button = ctk.CTkButton(self.button_frame, text="＋1分", command=self.add_countdown_minutes,
                                                width=80,
                                                height=40)
        self.one_minutes_button.pack(side="left", padx=(20,20), pady=(20,20))

        # カウントダウンを10秒加算(タイマー開始前のみ有効)
        self.ten_seccond_button = ctk.CTkButton(self.button_frame, text="＋10秒", command=self.add_countdown_ten_seccond,
                                                width=80,
                                                height=40)
        self.ten_seccond_button.pack(side="left", padx=(20,20), pady=(20,20))

        # カウントダウンを1秒加算(タイマー開始前のみ有効)
        self.one_seccond_button = ctk.CTkButton(self.button_frame, text="＋1秒", command=self.add_countdown_one_seccond,
                                                width=80,
                                                height=40)
        self.one_seccond_button.pack(side="left", padx=(20,20), pady=(20,20))

        self.button_frame2 = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame2.pack()

        # start
        self.start_button = ctk.CTkButton(self.button_frame2, text="START", command=self.start ,
                                            width=80,
                                            height=40,
                                            cursor="hand2", # 指カーソル
                                            fg_color="#00FF00",
                                            hover_color="#006400",
                                            text_color="#FFFFFF",
                                            border_width=0)
        self.start_button.pack(side="left", pady=(10,0), padx=(20,20))
        # stop
        self.stop_button = ctk.CTkButton(self.button_frame2, text="STOP",command=self.stop,
                                            width=80,
                                            height=40,
                                            cursor="hand2", # 指カーソル
                                            fg_color="#20B2AA",
                                            hover_color="#00008B",
                                            text_color="#FFFFFF",
                                            border_width=0,
                                            state="disabled")
        self.stop_button.pack(side="left", pady=(10,0), padx=(20,20))

        # reset
        self.reset_button = ctk.CTkButton(self.button_frame2, text="RESET", command=self.reset,
                                            width=80,
                                            height=40,
                                            cursor="hand2", # 指カーソル
                                            fg_color="#B22222",
                                            hover_color="#8B0000",
                                            text_color="#FFFFFF",
                                            border_width=0)
        self.reset_button.pack(side="left", pady=(10,0), padx=(20,20))

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
                    self.after_cancel(self.after_id)
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
                self.after_id = self.after(10, self.update_time)

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
                self.after_cancel(self.after_id)
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
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="disabled")
            self.one_minutes_button.configure(state="normal")
            self.ten_seccond_button.configure(state="normal")
            self.one_seccond_button.configure(state="normal")

        # 時間設定のボタンが押されたとき、スタンバイ状態としてstartボタンを有効化
        elif state == "standby":
            self.start_button.configure(state="normal")

        # カウントダン中はstartボタン及び、時間設定ボタンを無効化し、stopボタンを有効化
        elif state == "running":
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.one_minutes_button['state'] = "disabled"
            self.one_minutes_button.configure(state="disabled")
            self.ten_seccond_button.configure(state="disabled")
            self.one_seccond_button.configure(state="disabled")

        # 一時停止中はstopボタンを無効化し、startボンタンを有効化
        elif state == "stopped":
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")

# ======================================================================================================================