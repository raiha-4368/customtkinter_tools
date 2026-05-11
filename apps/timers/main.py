import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import winsound
import time

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# ======================================================================================================================

class NavigationFrame(ctk.CTkFrame):
    """サイドメニュー用のクラス"""
    def __init__(self, master, select_page_callback, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)

        self.grid_rowconfigure(4, weight=1) # 下部に余白を作る設定

        # タイトルラベル
        self.label = ctk.CTkLabel(self, text="Timers App")
        self.label.grid(row=0, column=0, padx=20, pady=20)

        # 切り替えボタン
        self.btn_page1 = ctk.CTkButton(self, text="Countdown", command=lambda: select_page_callback("Countdown"))
        
        self.btn_page1.grid(row=1, column=0, padx=20, pady=20)

        self.btn_page2 = ctk.CTkButton(self, text="Stopwatch", command=lambda: select_page_callback("Stopwatch"))
        self.btn_page2.grid(row=2, column=0, padx=20, pady=20)

        self.btn_page3 = ctk.CTkButton(self, text="Pomodoro", command=lambda: select_page_callback("Pomodoro"))
        self.btn_page3.grid(row=3, column=0, padx=20, pady=20)
        
        # サイドメニューの下部にモードチェンジ用セグメントボタンを配置
        segemented_button = ctk.CTkSegmentedButton(self, values=["System", "Dark", "Light"],
                                                     command=self.change_mode,
                                                     selected_color=("orange", "purple"),
                                                     selected_hover_color=("darkorange","indigo"))
        segemented_button.set(ctk.get_appearance_mode())    # 初期値を現在のモードに設定
        segemented_button.grid(row=6, pady=(0,10))

    # TODO : 取り合えず実装見送り
    # def toggle_buttons(self, state):
    #     #ボタンの切り替え

    # モードチェンジ
    def change_mode(self, new_appearance_mode):
        print(new_appearance_mode)
        ctk.set_appearance_mode(new_appearance_mode)
# ======================================================================================================================

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

# ======================================================================================================================
class TimersApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Timers App")
        self.geometry("700x500")

        # -------------------------
        # menuの生成
        # -------------------------
        menu_bar = tk.Menu(self)

        self.configure(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="メニュー",menu=file_menu)
        file_menu.add_command(label="終了", command=self.quit)


        # レイアウト設定(左:サイドメニュー、右:メインコンテンツ)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0, weight=1)

        # サイドメニューの配置
        self.navigation_frame = NavigationFrame(self, self.select_frame, width=140)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")

        # 画面インスタンスの生成
        self.pages ={
            "Countdown" : Countdown(self, fg_color="transparent"),
            "Stopwatch" : Stopwatch(self, fg_color="transparent"),
            "Pomodoro"  : Pomodoro(self, fg_color="transparent")
        }

        # 初期表示
        self.select_frame("Countdown")

    def select_frame(self, name):
        """指定された名前のframeを表示し、他を隠す"""
        for page_name, page_instance in self.pages.items():
            if page_name == name:
                page_instance.grid(row=0, column=1, sticky="nsew")
            else:
                page_instance.grid_forget()

# ======================================================================================================================


# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    # インスタンス化
    app = TimersApp()
    #イベント待ちループ開始
    app.mainloop()
