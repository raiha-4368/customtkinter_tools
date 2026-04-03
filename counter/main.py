import tkinter as tk # メニュー用
import customtkinter as ctk

# 外観モード（"System", "Dark", "Light"）とテーマカラー（"blue", "green", "dark-blue"）の設定
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# CTKを継承
class CounterApp(ctk.CTk):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):
        super().__init__()

        self.configure(fg_color="#fffacd")
        self.title("Counter App")
        self.geometry("400x300")
        # -------------------------
        # フレーム生成
        # ctkでは親要素(master)は最初の引数に書くのが一般的
        # -------------------------
        self.main_frame = ctk.CTkFrame(master=self, width=200,height=200, fg_color="#fffacd")
        self.main_frame.pack()

        #初期表示
        self.create_widgets()

    # -------------------------
    # メイン画面表示UI
    # -------------------------
    def create_widgets(self):
        # -------------------------
        # menuの生成
        # custom tkinterにメニューは存在しないため、tkinterを使用
        # -------------------------
        menu_bar = tk.Menu(self)

        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="メニュー",menu=file_menu)
        file_menu.add_command(label="終了", command=self.quit)
        #区切り線を出すための記述
        # file_menu.add_separator()

        # -------------------------
        # 変数初期化
        # -------------------------
        self.count = 0

        # -------------------------
        # mainフレーム内の要素
        # -------------------------
        # カウント表示用ラベル
        self.display_count = ctk.CTkLabel(self.main_frame, text='0', font=('Arial', 40),text_color="#333")
        self.display_count.pack(pady=20)

        #加算用ボタン
        btn_plus = ctk.CTkButton(self.main_frame, text="+1", width=60, command=self.plus, font=('Arial', 20), fg_color="#fa8072", text_color="#696969")
        btn_plus.pack(side="left", padx=(10,10))

        #減算用ボタン
        btn_minus = ctk.CTkButton(self.main_frame, text="-1", width=60,command=self.minus, font=('Arial', 20), fg_color="#add8e6", text_color="#696969")
        btn_minus.pack(side="left", padx=(10,10))

        #reset用ボタン
        btn_reset = ctk.CTkButton(self.main_frame, text="Reset", width=60, command=self.reset, font=('Arial', 20), fg_color="#98fb98", text_color="#696969")
        btn_reset.pack(side="left", padx=(10,10))

    def plus(self):
        self.count +=1
        self.display_count.configure(text=str(self.count))
    
    def minus(self):
        self.count -= 1
        self.display_count.configure(text=str(self.count))
    
    def reset(self):
        self.count = 0
        self.display_count.configure(text=str(self.count))

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    # インスタンス化
    app = CounterApp()
    #イベント待ちループ開始
    app.mainloop()

