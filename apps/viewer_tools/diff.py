from tkinter import ttk,messagebox
import customtkinter as ctk
from common import dialogs, files
from itertools import zip_longest
import difflib

class DifffilesApp(ctk.CTkFrame):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        label = ctk.CTkLabel(self, text="Diff")
        label.pack()
        
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
        # タブ設定
        # -------------------------
        tabview = ctk.CTkTabview(self, fg_color="transparent")
        tabview.pack(expand=True,fill="both")

        tabview.add("file mode")  # add tab at the end
        tabview.add("text mode")  # add tab at the end
        tabview.set("text mode")  # set currently visible tab

        # -------------------------
        # menu_frame
        # -------------------------
        self.menu_frame_file = ctk.CTkFrame(tabview.tab("file mode"), fg_color="transparent")
        self.menu_frame_file.pack()

        self.menu_frame_text = ctk.CTkFrame(tabview.tab("text mode"), fg_color="transparent")
        self.menu_frame_text.pack()
        # -------------------------
        # menu_frame内の要素(file mode)
        # -------------------------
        self.diff_file_select = ctk.CTkButton(self.menu_frame_file, text="1つ目のファイル選択",command=self.get_diff_file1)
        self.diff_file_select.pack(side="left", pady=(10,10), padx=(10,10))

        self.diff_file_select2 = ctk.CTkButton(self.menu_frame_file, text="2つ目のファイル選択",command=self.get_diff_file2)
        self.diff_file_select2.pack(side="left", pady=(10,10), padx=(10,10))
        
        self.diff_only_button = ctk.CTkButton(self.menu_frame_file, text="差分のみを表示",command=self.diff_only_preview)
        self.diff_only_button.pack(side="left", pady=(10,10), padx=(10,10))

        # -------------------------
        # menu_frame内の要素(text mode)
        # -------------------------        
        self.clear_button = ctk.CTkButton(self.menu_frame_text, text="クリア",command=self.clear)
        self.clear_button.pack(side="left", pady=(10,10), padx=(10,10))

        # -------------------------
        # content_frame
        # -------------------------
        self.content_frame_file = ctk.CTkFrame(tabview.tab("file mode"), fg_color="transparent")
        self.content_frame_file.pack(expand=True,fill="both")

        self.content_frame_text = ctk.CTkFrame(tabview.tab("text mode"), fg_color="transparent")
        self.content_frame_text.pack(expand=True,fill="both")

        self.content_frame_text2 = ctk.CTkFrame(tabview.tab("text mode"), fg_color="transparent")
        self.content_frame_text2.pack(expand=True,fill="both")

        # -------------------------
        # content_frame内の要素(file mode)
        # -------------------------
        self.content_label = ctk.CTkLabel(self.content_frame_file,text="ファイル差分を表示します。")
        self.content_label.pack(pady=(30,10))

        self.diff_path_label = ctk.CTkLabel(self.content_frame_file,text="path : ")
        self.diff_path_label.pack(pady=(10,20))

        # セグメントボタンでコンテンツの切り替え
        self.text_change_button = ctk.CTkSegmentedButton(self.content_frame_file, values=["1つ目のファイル", "2つ目のファイル"],
                                                         command=self.change_content,
                                                         selected_color=("orange", "purple"),
                                                         selected_hover_color=("darkorange","indigo"))
        self.text_change_button.set("1つ目のファイル")
        self.text_change_button.pack(pady=(10,10))


        self.text_view_area = ttk.Treeview(self.content_frame_file)
        self.text_view_area.pack(expand=True,fill="both", pady=(0,20),padx=(20,20))

        # タグ設定
        self.text_view_area.tag_configure("red_row", background="#dc143c")
        
        # -------------------------
        # content_frame内の要素(text mode)
        # -------------------------
        self.content_label2 = ctk.CTkLabel(self.content_frame_text,text="テキスト差分を表示します。")
        self.content_label2.pack(pady=(30,10))

        self.textbox1 = ctk.CTkTextbox(self.content_frame_text)
        self.textbox1.pack(side="left", expand=True,fill="both", pady=(0,20),padx=(20,20))

        self.textbox2 = ctk.CTkTextbox(self.content_frame_text)
        self.textbox2.pack(side="left", expand=True,fill="both", pady=(0,20),padx=(20,20))

        # 初期セグメント設定
        self.segment_str = "diff_detail"

        # セグメントボタンでコンテンツの切り替え
        self.text_diff_button = ctk.CTkSegmentedButton(self.content_frame_text2, values=["左ボックス表示", "右ボックス表示", "差分詳細表示"],
                                                         command=self.change_content_text,
                                                         selected_color=("orange", "purple"),
                                                         selected_hover_color=("darkorange","indigo"))
        self.text_diff_button.set("差分詳細表示")
        self.text_diff_button.pack(pady=(10,10))


        self.diff_textbox = ctk.CTkTextbox(self.content_frame_text2)
        self.diff_textbox.pack(expand=True, fill="both", pady=(0,20),padx=(20,20))


        # 差分表示用Textboxの初期設定のイメージ
        self.diff_textbox.tag_config("added", background="#244a28", foreground="#e6edf3")    # 緑背景（追加）
        self.diff_textbox.tag_config("removed", background="#4c1e20", foreground="#e6edf3")  # 赤背景（削除）
        self.diff_textbox.tag_config("red_row", background="#dc143c")
        
        # バインド処理
        self.textbox1.bind("<KeyRelease>", self.check_text_diff)
        self.textbox2.bind("<KeyRelease>", self.check_text_diff)


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
            self.diff_only_button.configure(text="差分のみ表示")
        else:
            self.diff_only = True
            self.diff_only_button.configure(text="すべて表示")

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

    # bindは自動的にeventを引数に渡すので、指定していないとエラーになる
    def check_text_diff(self, event=None):

        self.diff_textbox.delete("1.0", "end")

        line1 = self.textbox1.get("1.0", "end-1c").splitlines()
        line2 = self.textbox2.get("1.0", "end-1c").splitlines()

        if self.segment_str == "diff_detail":
            # difflibで差分を生成
            diff = list(difflib.ndiff(line1, line2))
            for line in diff:
                # 先頭2文字のコード（"  ", "- ", "+ ", "? "）
                # ndiff が返す各行の先頭の記号は、以下のように「テキストA（左 / 修正前）」と「テキストB（右 / 修正後）」のどちらに対応しているかが決まっています。
                # 先頭の記号意味どちらのテキストにあるか
                #    (半角スペース2つ)両方で共通している行 両方にある
                # -  (マイナス＋スペース)テキストAにだけ存在する行 テキストA（左）側にある（＝Bで削除された）
                # +  (プラス＋スペース)テキストBにだけ存在する行テキストB（右）側にある（＝Bで追加された）
                # ?  (ハテナ＋スペース)直前の行の「文字単位」の変更箇所を示すガイド行どちらにも属さない（画面には表示しない裏の判定用）
                code = line[:2]
                # 本文
                content = line[2:] + "\n" 
                # 変更なし(スペース2つ)
                if code == "  ":
                    self.diff_textbox.insert("end", content)
                # 右にだけある
                elif code == "+ ":
                    #追加
                    self.diff_textbox.insert("end", content, "added")
                # 左にだけある
                elif code == "- ":
                    # 削除
                    self.diff_textbox.insert("end", content, "removed")
                elif code == "? ":
                    # 行内の細かい変化 (今回はスキップ、さらに細かく色分けする際に使用)
                    pass
        elif self.segment_str == "left" or self.segment_str == "right":
        # zip_longestは、長い方のリストに合わせてループを固定する
        # 足りない部分はfillvalueで指定した値を入れる
            for row1, row2 in zip_longest(line1, line2, fillvalue=""):
                if self.segment_str == "left":
                    if row1 == row2:
                        self.diff_textbox.insert("end", f"{row1}\n")
                    else:
                        self.diff_textbox.insert("end", f"{row1}\n", "red_row")

                elif self.segment_str == "right":
                    if row1 == row2:
                        self.diff_textbox.insert("end", f"{row2}\n")
                    else:
                        self.diff_textbox.insert("end", f"{row2}\n", "red_row")

    def change_content_text(self,value):
        if value == "左ボックス表示":
            self.segment_str = "left"
            self.check_text_diff()

        elif value == "右ボックス表示":
            self.segment_str = "right"
            self.check_text_diff()
        
        elif value == "差分詳細表示":
            self.segment_str = "diff_detail"
            self.check_text_diff()

    def clear(self):
        self.diff_textbox.delete("1.0", "end")
        self.textbox1.delete("1.0", "end")
        self.textbox2.delete("1.0", "end")
