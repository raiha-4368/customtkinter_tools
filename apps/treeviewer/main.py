import tkinter as tk
import customtkinter as ctk
from common import dialogs
from pathlib import Path

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TreeCommandApp(ctk.CTk):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):

        super().__init__()   
        self.title("treeコマンドツール")
        self.geometry("1200x800")

        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        self.side_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFFFFF")
        self.side_frame.pack(side=ctk.LEFT, fill=ctk.Y)

        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(side=ctk.RIGHT, expand=True, fill=ctk.BOTH)

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

        # -------------------------
        # 変数宣言
        # -------------------------

        # -------------------------
        # side_frame内の要素
        # -------------------------
        self.dir_select = ctk.CTkButton(self.side_frame, text="対象ディレクトリを選択",command=self.select_dir)
        self.dir_select.pack(pady=(10,10), padx=(10,10))

        self.clear_button = ctk.CTkButton(self.side_frame, text="クリア",command=self.clear)
        self.clear_button.pack(pady=(10,10), padx=(10,10))

        # サイドメニューの下部にモードチェンジ用セグメントボタンを配置
        segemented_button = ctk.CTkSegmentedButton(self.side_frame, values=["System", "Dark", "Light"],
                                                     command=self.change_mode,
                                                     selected_color=("orange", "purple"),
                                                     selected_hover_color=("darkorange","indigo"))
        segemented_button.set(ctk.get_appearance_mode())    # 初期値を現在のモードに設定
        segemented_button.pack(side="bottom",pady=(10,10))


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





    # モードチェンジ
    def change_mode(self, new_appearance_mode):
        print(new_appearance_mode)
        ctk.set_appearance_mode(new_appearance_mode)

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #インスタンス化
    app = TreeCommandApp()
    #イベント待ちループ開始
    app.mainloop()

