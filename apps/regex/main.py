import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from common import dialogs
from pathlib import Path
import re

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class RegexApp(ctk.CTk):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):
        super().__init__()

        self.configure(fg_color="#191919")
        self.title("Regex App")
        self.geometry("1500x800")

        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = ctk.CTkFrame(self, fg_color="#191919")
        self.main_frame.pack(fill="both", expand=True)

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

        #変数宣言(エラーにならないように宣言)
        self.filepath = ""
        self.exact_match_flag = False
        self.result = []

        # 説明ラベル
        self.label = ctk.CTkLabel(self.main_frame, text="正規表現を行います",fg_color="#191919",text_color="#ffffff")
        self.label.pack(pady=(20,20))
        # エラー用ラベル
        self.error_label = ctk.CTkLabel(self.main_frame, text="",text_color="red")
        self.error_label.pack(pady=(10,10))

        # ***************************************************************************************************
        # search_frame
        # 検索文字列入力フレーム
        self.search_frame = ctk.CTkFrame(self.main_frame, fg_color="#191919")
        self.search_frame.pack(fill="both", expand=True)

        # 正規表現の入力を促すラベル
        self.search_word_label = ctk.CTkLabel(self.search_frame, text="正規表現を入力")
        self.search_word_label.pack(side="left", pady=(0,0),padx=(20,20))
        # 正規表現の入力テキストボックス
        self.word = ctk.CTkTextbox(self.search_frame, height=100)
        self.word.pack(side="left", pady=(20,20),padx=(20,20), fill="x", expand=True)
        self.word.bind("<KeyRelease>", self.regex_exe)

        # ***************************************************************************************************

        # ***************************************************************************************************
        # textbox_frame
        # テキストエリア用フレーム
        self.textbox_frame = ctk.CTkFrame(self.main_frame, fg_color="#191919")
        self.textbox_frame.pack(fill="both", expand=True)

        # --- 左側：入力エリア用のコンテナ ---
        self.left_container = ctk.CTkFrame(self.textbox_frame, fg_color="transparent")
        self.left_container.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)

        self.label_target = ctk.CTkLabel(self.left_container, text="入力データ", text_color="#ffffff")
        self.label_target.pack(side="top", anchor="w") # anchor="w"で左寄せ

        self.textbox_target = ctk.CTkTextbox(self.left_container)
        self.textbox_target.pack(side="top", fill="both", expand=True)
        self.textbox_target.bind("<KeyRelease>", self.regex_exe)


        # --- 中央：矢印 ---
        self.arrow_label = ctk.CTkLabel(self.textbox_frame, text="⇒", fg_color="#191919", text_color="#ffffff")
        self.arrow_label.pack(side="left", padx=(10, 10))


        # --- 右側：結果エリア用のコンテナ ---
        self.right_container = ctk.CTkFrame(self.textbox_frame, fg_color="transparent")
        self.right_container.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=20)

        self.label_result = ctk.CTkLabel(self.right_container, text="検索結果", text_color="#ffffff")
        self.label_result.pack(side="top", anchor="w")

        self.textbox_result = ctk.CTkTextbox(self.right_container, state='disabled')
        self.textbox_result.pack(side="top", fill="both", expand=True)
        # ***************************************************************************************************

    # 正規表現を行う
    # 第二引数のeventはbindで渡すときに必要
    # class内のインスタンスメソッドの第一引数はselfとなる
    # bindは自動的にeventを引数に渡すので、指定していないとエラーになる
    def regex_exe(self, event=None):
        # textboxの情報を取得
        # "end-1c"で余計な改行を削除
        text = self.textbox_target.get("1.0", "end-1c")      
        pattern = self.word.get("1.0", "end-1c")
        self.error_mang(text, pattern)

        result = re.search(pattern, text)

        self.textbox_result.configure(state='normal')
        if result:
            self.textbox_result.delete("1.0", "end") #1行目から最後まで削除    
            self.textbox_result.insert("1.0", result.group())
        else:
            self.textbox_result.delete("1.0", "end") #1行目から最後まで削除    
            self.textbox_result.insert("1.0", "一致はありません")

        self.textbox_result.configure(state='disabled')

    def error_mang(self, text, pattern):
        new_text = ""
        if not text:
            new_text= new_text + "正規表現対象が入力されていません\n"
        
        if not pattern:
            new_text = new_text + "正規表現が入力されていません"
        
        self.error_label.configure(text=new_text)


    # モードチェンジ
    def change_mode(self, new_appearance_mode):
        print(new_appearance_mode)
        ctk.set_appearance_mode(new_appearance_mode)

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #インスタンス化
    app = RegexApp()
    #イベント待ちループ開始
    app.mainloop()

