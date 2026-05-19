import customtkinter as ctk
import winsound

# ======================================================================================================================
class Pomodoro(ctk.CTkFrame):
    """ポモドーロタイマー"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        label = ctk.CTkLabel(self, text="ポモドーロタイマー")
        label.pack()
        # タイマーの初期化処理
        self.runningflag = False    #起動中or停止中の判定フラグ

        self.mode = "work"              # or break
        self.remaining_work_seconds = 1500   # 25分(1500)固定値
        self.remaining_break_seconds = 300   # 5分(300)固定値
        self.remaining_seconds = 1500   # 初期値は25分(1500)にあわせる
        self.set_count = 0              # 今何回目か
        self.max_sets = 4               # ループ回数

        # ポモドーロカウント(デフォルト 1/4回)
        self.pomodoro_label = ctk.CTkLabel(self,
                                           text="ポモドーロタイマー",
                                           font=("Arial", 30),
                                           text_color=("#000000","#FFFFFF"))
        self.pomodoro_label.pack(pady=10)
        self.pomodoro_count_label = ctk.CTkLabel(self,
                                                 text=f"{self.set_count + 1}/{self.max_sets}回",
                                                 font=("Arial", 20),
                                                 text_color=("#000000","#FFFFFF"))
        self.pomodoro_count_label.pack(pady=(0,20))

        # タイム表示(デフォルト25分表示)
        self.worktime_label = ctk.CTkLabel(self,
                                           text="作業時間",
                                           font=("Arial",30),
                                           text_color=("#000000","#FFFFFF"))
        self.worktime_label.pack(pady=10)
        self.countdown_label = ctk.CTkLabel(self,
                                            text=f"{self.remaining_work_seconds//60:02}:00",
                                            font=("Arial", 40),
                                            text_color=("#000000","#FFFFFF"))
        self.countdown_label.pack(pady=(0,20))

        # タイム表示(デフォルト5分表示)
        self.breaktime_label = ctk.CTkLabel(self,
                                            text="休憩時間",
                                            font=("Arial",30),
                                            text_color=("#000000","#FFFFFF"))
        self.breaktime_label.pack()
        self.breaktime_time = ctk.CTkLabel(self,
                                           text=f"{self.remaining_break_seconds//60:02}:00",
                                           font=("Arial", 40),
                                           text_color=("#000000","#FFFFFF"))
        self.breaktime_time.pack(pady=(0,20))

        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack()

        # start
        self.start_button = ctk.CTkButton(self.button_frame,
                                            width=80,
                                            height=40,
                                            text="START",
                                            command=self.start,
                                            cursor="hand2", # 指カーソル
                                            fg_color="#00FF00",
                                            hover_color="#006400",
                                            text_color="#FFFFFF",
                                            border_width=0)
        self.start_button.pack(side="left", padx=(20,20))

        # reset
        self.reset_button = ctk.CTkButton(self.button_frame,
                                            width=80,
                                            height=40,
                                            text="RESET",
                                            command=self.reset,
                                            cursor="hand2", # 指カーソル
                                            fg_color="#B22222",
                                            hover_color="#8B0000",
                                            text_color="#FFFFFF",
                                            border_width=0)
        self.reset_button.pack(side="left", padx=(20,20))

        # resetボタンを無効にしておく
        self.toggle_buttons(False)


    def start(self):
        #起動フラグをTrueへ
        self.runningflag = True
        # 起動フラグがTureなら実行(念のためif)
        if self.runningflag:
            self.toggle_buttons(True)
            self.tick()
        return
    
    def reset(self):
        #起動フラグをFalseへ
        self.runningflag = False
        # 起動フラグがFalseなら実行(念のためif)
        if not self.runningflag:        # タイマーの初期化処理
            self.runningflag = False    #起動中or停止中の判定フラグ

            self.mode = "work"              # or break
            self.remaining_seconds = 1500   # 25分(1500)固定値(残り時間)
            self.set_count = 0              # 今何回目か
            self.max_sets = 4               # ループ回数
            self.pomodoro_count_label.configure(text=f"{self.set_count + 1}/{self.max_sets}回")
            self.countdown_label.configure(text=f"{self.remaining_work_seconds//60:02}:00")
            self.breaktime_time.configure(text=f"{self.remaining_break_seconds//60:02}:00")
            # startボタンを有効化
            self.toggle_buttons(False)

            return

    def update_display(self):
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        if self.mode == "work":
            self.countdown_label.configure(text=f"{minutes:02}:{seconds:02}")
        elif self.mode == "break":
            self.breaktime_time.configure(text=f"{minutes:02}:{seconds:02}")
        return        

    def tick(self):
        # runningフラグが真なら実行
        if self.runningflag:
            self.remaining_seconds -= 1
        else:
            #フラグはFalseなら処理しない
            return

        if self.remaining_seconds <= 0:
            
            # システムアスタリスク音（ポーン）
            winsound.MessageBeep(winsound.MB_ICONASTERISK)

            if self.mode == "work":
                self.mode = "break"
                self.remaining_seconds = 300 # 5分(300)
                # mode切り替わりでラベルの初期化を行う
                self.countdown_label.config(text=f"{self.remaining_work_seconds//60:02}:00")

            else:
                # set_countを1つ進める
                self.set_count += 1

                # set_countがmax_setsと同数以上なら処理を終える
                if self.set_count >= self.max_sets:
                    self.runningflag = False
                    # ラベルの初期化
                    self.countdown_label.config(text=f"{self.remaining_work_seconds//60:02}:00")
                    self.breaktime_time.config(text=f"{self.remaining_break_seconds//60:02}:00")
                    return
                
                #ポモドーロの回数ラベルを更新
                self.pomodoro_count_label.config(text=f"{self.set_count + 1}/{self.max_sets}回")
                self.mode = "work"
                self.remaining_seconds = 1500 # 25分(1500)
                # mode切り替わりでラベルの初期化を行う
                self.breaktime_time.config(text=f"{self.remaining_break_seconds//60:02}:00")

        print(self.mode, self.remaining_seconds, self.set_count)
        self.update_display()

        self.after(1000, self.tick)
    
    def toggle_buttons(self, flag):
        if flag:
            self.start_button.configure(state="disabled")
            self.reset_button.configure(state="normal")
        else:
            self.start_button.configure(state="normal")
            self.reset_button.configure(state="disabled")

# ======================================================================================================================