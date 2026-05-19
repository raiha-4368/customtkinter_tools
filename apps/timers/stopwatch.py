import customtkinter as ctk
import time

# ======================================================================================================================
class Stopwatch(ctk.CTkFrame):
    """ストップウォッチ"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        label = ctk.CTkLabel(self, text="ストップウォッチ")
        label.pack()
        # タイマーの初期化処理
        self.start_time = 0
        self.elapsed_time = 0
        self.runningflag = False
        self.after_id = None    #予約したアフター管理用ID

        # -------------------------
        # タイム表示
        # -------------------------        
        self.stopwatch_label = ctk.CTkLabel(self, text="00:00.00", font=("Courier", 50, "bold")) # 等幅フォント
        self.stopwatch_label.pack(pady=(50.50))

        # -------------------------
        # ボタン用フレーム
        # -------------------------        
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)

        # start stop押下時は無効
        self.start_button = ctk.CTkButton(self.button_frame, text="START", command=self.start,
                                            width=80,
                                            height=40,
                                            cursor="hand2", # 指カーソル
                                            fg_color="#00FF00",
                                            hover_color="#006400",
                                            text_color="#FFFFFF",
                                            border_width=0)
        self.start_button.pack(side="left", padx=(20,0),expand=True)
        # stop start押下時のみ有効
        self.stop_button = ctk.CTkButton(self.button_frame, text="STOP",command=self.stop,
                                            width=80, 
                                            height=40,
                                            cursor="hand2", # 指カーソル
                                            fg_color="#20B2AA",
                                            hover_color="#00008B",
                                            text_color="#FFFFFF",
                                            border_width=0,
                                            state="disabled")
        self.stop_button.pack(side="left", padx=(20,0),expand=True)
        # reset
        self.reset_button = ctk.CTkButton(self.button_frame, text="RESET", command=self.reset,
                                            width=80,
                                            height=40,
                                            cursor="hand2", # 指カーソル
                                            fg_color="#B22222",
                                            hover_color="#8B0000",
                                            text_color="#FFFFFF",
                                            border_width=0)
        self.reset_button.pack(side="left", padx=(20,0),expand=True)

    def update_time(self):
        # runningフラグが真なら実行
        if self.runningflag:
            #経過時刻を計算(現在時刻-startを押下した時刻+stopを押下するまでに経過していた時間)
            # 例: 現在時刻(120) - startを押下した時刻(80) + stopを押下するまでに経過していた時間(30)
            now = time.time() - self.start_time + self.elapsed_time

            #分ミリ秒整形
            # divmod は、「割り算の商」と「余り」を同時に出してくれる関数。
            mins, secs = divmod(now, 60)                                #今の時間を60で割って分と秒に分ける
            milli = int((secs - int(secs)) * 100)                       #ミリ秒を取り出す secs(小数点以下あり) - int(secs(小数点以下無し)で計算し、小数点以下のみの値を算出し下2桁を*100でint型とする
            time_str = f"{int(mins):02d}:{int(secs):02d}.{milli:02d}"   #02d ⇒2桁（2 digits）で表示して、足りない所は 0 で埋める。 分と秒とミリ秒の2桁の数字が1桁の数字だった場合、0で埋めた文字列とする
            self.stopwatch_label.configure(text = time_str)

            #10ミリ秒後に自分を呼び出す(このidを持っている限り、after処理を行う)
            self.after_id = self.after(10, self.update_time)

    #startを押下してからの時刻を取得
    def start(self):
        if not self.runningflag:
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
        self.stopwatch_label.configure(text="00:00.00")
        self.toggle_buttons("reset")

    def toggle_buttons(self, state):
        #ボタンの切り替え
        if state == "running":
            self.start_button.configure(state= "disabled")
            self.stop_button.configure(state="normal")
        elif state == "stopped" or state == "reset":
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
# ======================================================================================================================