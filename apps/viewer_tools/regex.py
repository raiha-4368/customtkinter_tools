import customtkinter as ctk
import re

class RegexApp(ctk.CTkFrame):
    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        label = ctk.CTkLabel(self, text="regex")
        label.pack()

        #変数宣言(エラーにならないように宣言)
        self.filepath = ""
        self.exact_match_flag = False
        self.result = []

        # -------------------------
        # menu_frame
        # -------------------------
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack()
        # -------------------------
        # menu_frame内の要素
        # -------------------------
        # 説明ラベル
        self.label = ctk.CTkLabel(self.menu_frame, text="正規表現を行います")
        self.label.pack(pady=(20,20))
        # エラー用ラベル
        self.error_label = ctk.CTkLabel(self.menu_frame, text="",text_color="red")
        self.error_label.pack(pady=(10,10))

        # ***************************************************************************************************
        # search_frame
        # 検索文字列入力フレーム
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
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
        self.textbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.textbox_frame.pack(fill="both", expand=True)

        # --- 左側：入力エリア用のコンテナ ---
        self.left_container = ctk.CTkFrame(self.textbox_frame, fg_color="transparent")
        self.left_container.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)

        self.label_target = ctk.CTkLabel(self.left_container, text="入力データ")
        self.label_target.pack(side="top", anchor="w") # anchor="w"で左寄せ

        self.textbox_target = ctk.CTkTextbox(self.left_container)
        self.textbox_target.pack(side="top", fill="both", expand=True)
        self.textbox_target.bind("<KeyRelease>", self.regex_exe)


        # --- 中央：矢印 ---
        self.arrow_label = ctk.CTkLabel(self.textbox_frame, text="⇒")
        self.arrow_label.pack(side="left", padx=(10, 10))


        # --- 右側：結果エリア用のコンテナ ---
        self.right_container = ctk.CTkFrame(self.textbox_frame, fg_color="transparent")
        self.right_container.pack(side="left", fill="both", expand=True, padx=(0, 20), pady=20)

        self.label_result = ctk.CTkLabel(self.right_container, text="検索結果")
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
