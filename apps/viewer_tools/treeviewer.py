import customtkinter as ctk
from common import dialogs
from pathlib import Path

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TreeCommandApp(ctk.CTkFrame):
    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        label = ctk.CTkLabel(self, text="TreeVirere")
        label.pack()

        # -------------------------
        # menu_frame
        # -------------------------
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack()
        # -------------------------
        # menu_frame内の要素
        # -------------------------
        self.dir_select = ctk.CTkButton(self.menu_frame, text="対象ディレクトリを選択",command=self.select_dir)
        self.dir_select.pack(side="left", pady=(10,10), padx=(10,10))

        self.clear_button = ctk.CTkButton(self.menu_frame, text="クリア",command=self.clear)
        self.clear_button.pack(side="left", pady=(10,10), padx=(10,10))


        # -------------------------
        # content_frame
        # -------------------------
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(expand=True,fill="both")
        # -------------------------
        # content_frame内の要素
        # -------------------------
        self.content_label = ctk.CTkLabel(self.content_frame,text="対象のディレクトリ以下をTreeコマンド風に表示します")
        self.content_label.pack(pady=(30,10))

        self.path_label = ctk.CTkLabel(self.content_frame,text="path : ")
        self.path_label.pack(pady=(10,20))


        self.textbox_area = ctk.CTkTextbox(self.content_frame, state="disabled")
        self.textbox_area.pack(expand=True,fill="both",pady=(0,20),padx=(20,20))


    #ディレクトリ選択
    def select_dir(self):
        dirpath = dialogs.select_folder(title="ディレクトリを選択")

        if dirpath:
            
            p = Path(dirpath)
            # パス表示のラベルを更新
            self.path_label.configure(text=f"path : {dirpath}")
            
            self.textbox_area.configure(state="normal")
            self.textbox_area.delete("1.0", "end")
            self.textbox_area.insert("1.0", f"{p.name}\n")

            self.display_tree(p, "")

            self.textbox_area.configure(state="disabled")

    def display_tree(self, dirpath, prefix):
        """
        dirpath: 探索するPathオブジェクト
        prefix:  行の先頭に付ける枝記号の文字列
        """
        # フォルダ内の中身をリスト化
        contents = list(dirpath.iterdir())
        # 表示を見やすくするため、フォルダを先に、ファイルを後に並べ替える（任意）
        contents.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

        # 受け取ったフォルダ内要素のカウント
        count = len(contents)

        for i, path in enumerate(contents):
            # 最後の要素かどうかを判定
            # max値に対して最後かどうかを判定し、True,Falseを返却
            is_last = (i == count - 1)
            
            # 枝の記号を決定 三項演算子の書き方
            # is_lastがTreuの時、└── 
            # Falseの時├── 
            connector = "└── " if is_last else "├── "
            
            # テキストエリアに挿入
            self.textbox_area.insert("end", f"{prefix}{connector}{path.name}\n")

            # フォルダであれば再帰
            if path.is_dir():
                # 次の階層へのプレフィックス（接頭辞）を計算
                # 自分が最後なら空白を、まだ続くなら縦線を引く
                new_prefix = prefix + ("    " if is_last else "│   ")
                self.display_tree(path, new_prefix)

# クリア処理
    def clear(self):
        self.path_label.configure(text=f"path : ")
        self.textbox_area.configure(state="normal")
        self.textbox_area.delete("1.0", "end")
        self.textbox_area.configure(state="disabled")

