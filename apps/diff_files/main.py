import tkinter as tk
from tkinter import ttk,messagebox
import customtkinter as ctk
from common import dialogs, files
from itertools import zip_longest

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class DifffilesApp(ctk.CTk):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):

        super().__init__()   
        self.title("差分表示ツール")
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
        self.filepath = ""
        self.content = []
        self.diff_filepath1 = ""
        self.diff_filepath2 = ""
        self.diff_content1 = []
        self.diff_content2 = []

        # 比較したコンテンツ
        self.diff_content = []

        # 差分のみ表示フラグ
        self.diff_only = False

        # -------------------------
        # side_frame内の要素
        # -------------------------
        self.diff_file_select = ctk.CTkButton(self.side_frame, text="1つ目のファイル選択",command=self.get_diff_file1)
        self.diff_file_select.pack(pady=(10,10), padx=(10,10))

        self.diff_file_select2 = ctk.CTkButton(self.side_frame, text="2つ目のファイル選択",command=self.get_diff_file2)
        self.diff_file_select2.pack(pady=(10,10), padx=(10,10))
        
        self.diff_only_button = ctk.CTkButton(self.side_frame, text="差分のみを表示",command=self.diff_only_preview)
        self.diff_only_button.pack(pady=(10,10), padx=(10,10))


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
        self.content_label = ctk.CTkLabel(self.content_frame,text="ファイル差分を表示します。")
        self.content_label.pack(pady=(30,10))

        self.content_label = ctk.CTkLabel(self.content_frame,text="1つ目のファイル")
        self.content_label.pack(pady=(10,20))

        self.diff_path_label = ctk.CTkLabel(self.content_frame,text="path : ")
        self.diff_path_label.pack(pady=(10,20))

        # セグメントボタンでコンテンツの切り替え
        self.text_change_button = ctk.CTkSegmentedButton(self.content_frame, values=["1つ目のファイル", "2つ目のファイル"],
                                                         command=self.change_content,
                                                         selected_color=("orange", "purple"),
                                                         selected_hover_color=("darkorange","indigo"))
        self.text_change_button.set("1つ目のファイル")
        self.text_change_button.pack()


        self.text_view_area = ttk.Treeview(self.content_frame)
        self.text_view_area.pack(expand=True,fill="both",pady=(0,20),padx=(20,20))

        # タグ設定
        self.text_view_area.tag_configure("red_row", background="#ffcccc")


        # 1つ目のファイルパスを取得
    def get_diff_file1(self):
        # 以下でファイルを開き、pathとcontentを取得し、1つ目のファイル情報として記録
        self.select_file()

        # 1つ目のファイルの情報を保持
        if self.filepath:
            self.diff_filepath1 = self.filepath
            self.diff_content1 = self.content

            self.text_change_button.set("1つ目のファイル")
            self.diff_path_label.configure(text=f"path : {self.diff_filepath1}")

            self.diff_content = []

            #textboxに表示
            self.check_diff()
            if self.diff_content:
                self.diff_preview(1, self.diff_content)
            else:
                self.preview(self.diff_filepath1, self.diff_content1)
    
    # 2つ目のファイルパスを取得
    def get_diff_file2(self):
        # 以下でファイルを開き、pathとcontentを取得し、2つ目のファイル情報として記録
        self.select_file()

        # 2つ目のファイルの情報を保持
        if self.filepath:
            self.diff_filepath2 = self.filepath
            self.diff_content2 = self.content

            self.text_change_button.set("2つ目のファイル")
            self.diff_path_label.configure(text=f"path : {self.diff_filepath2}")

            self.diff_content = []

            #textboxに表示
            self.check_diff()
 
            if self.diff_content:
                self.diff_preview(2, self.diff_content)
            else:
                self.preview(self.diff_filepath2, self.diff_content2)

    # ファイルを開く
    def select_file(self):
        #変数の初期化
        self.filepath = ""
        self.content = []

        # ファイルを選択
        self.filepath = dialogs.select_file()

        if self.filepath:
            try:
                self.content, error = files.read_line_file(self.filepath)
                # *****************************************************************************
                # print(f"全体:{self.content}\n")
                # print(f"1行ずつ:")
                # for row in self.content:
                #     print(row)
                # *****************************************************************************

                if error:
                    messagebox.showerror("エラー", error)

            except Exception as e:
                  messagebox.showerror("エラー",e)

    # treeviewに表示
    def preview(self, path, content):
        if content:
            # 既存データをすべて削除
            for item in self.text_view_area.get_children():
                self.text_view_area.delete(item)
            
            # 見出し設定
            self.text_view_area.heading("#0", text=f"path : {path}")

            # データの挿入
            # ヘッダー行を指定していないのでtextで挿入
            for i, row in enumerate(content, start=1):
                self.text_view_area.insert("", "end", text=f"{i}. {row}")
            
    def diff_preview(self, set_content, content):
        # 既存データをすべて削除
        for item in self.text_view_area.get_children():
            self.text_view_area.delete(item)
        if content:
            for i, (row1, row2, flag) in enumerate(content, start=1):
                if set_content == 1:
                    # 見出し設定
                    self.text_view_area.heading("#0", text=f"path : {self.diff_filepath1}")
                    if flag:
                        if not self.diff_only:
                            self.text_view_area.insert("", "end", text=f"{i}. {row1}")
                    else:
                        self.text_view_area.insert("", "end", text=f"{i}. {row1}", tags=("red_row"))
                else:
                    # 見出し設定
                    self.text_view_area.heading("#0", text=f"path : {self.diff_filepath2}")
                    if flag:
                        if not self.diff_only:
                            self.text_view_area.insert("", "end", text=f"{i}. {row2}")
                    else:
                        self.text_view_area.insert("", "end", text=f"{i}. {row2}", tags=("red_row"))


    def check_diff(self):
        if self.diff_content1 and self.diff_content2:
            # 初期化
            self.diff_contetn = []

            # zip_longestは、長い方のリストに合わせてループを固定する
            # 足りない部分はfillvalueで指定した値を入れる
            for row1, row2 in zip_longest(self.diff_content1, self.diff_content2, fillvalue=""):
                if row1 == row2:
                    self.diff_content.append((row1, row2, True))
                else:
                    self.diff_content.append((row1, row2, False))


            # zip_longestを使わなかった時の処理はコメントアウト
            # for i1, row1 in enumerate(self.diff_content1, start=1):
            #     for i2, row2 in enumerate(self.diff_content2, start=1):
            #         #1つ目と2つ目のコンテンツの行数の一致する行に対して処理
            #         if i1 == i2:
            #             # 行のコンテンツが一致していればTrue、一致していなければFalseをlistに格納していく
            #             if row1 == row2:
            #                 self.diff_content.append((row1, row2, True))
            #             else:
            #                 self.diff_content.append((row1, row2, False))
            #             break

    def diff_only_preview(self):

        if not self.diff_content:
            messagebox.showerror("エラー", "差分のみ表示するファイルが存在しません")
            return
        
        # ボタン表示とフラグの切り替え
        if self.diff_only:
            self.diff_only = False
            self.diff_only_button.configure(text="すべて表示")
        else:
            self.diff_only = True
            self.diff_only_button.configure(text="差分のみ表示")

        set_content = self.text_change_button.get()
        if set_content == "1つ目のファイル":
            self.diff_preview(1,self.diff_content)
        else:
            self.diff_preview(2,self.diff_content)
            

    # 表示ファイルを切り替えるセグメントボタンが押されたときの処理
    def change_content(self, value):
        if value == "1つ目のファイル":
            self.diff_path_label.configure(text=f"path : {self.diff_filepath1}")
            self.diff_preview(1, self.diff_content)

        elif value == "2つ目のファイル":
            self.diff_path_label.configure(text=f"path : {self.diff_filepath2}")
            self.diff_preview(2, self.diff_content)


    # モードチェンジ
    def change_mode(self, new_appearance_mode):
        print(new_appearance_mode)
        ctk.set_appearance_mode(new_appearance_mode)

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #インスタンス化
    app = DifffilesApp()
    #イベント待ちループ開始
    app.mainloop()

