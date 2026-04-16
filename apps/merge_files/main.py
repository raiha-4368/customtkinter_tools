from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from common import files, path_utils, dialogs

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class FileMergeApp(ctk.CTk):
    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):
        super().__init__()

        self.configure(fg_color="#191919")
        self.title("Text Extract App")
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
        # それぞれ1つ目のファイルの中身と2つ目のファイルの中身
        self.filepath = ""
        self.filepath1 = ""
        self.filepath2 = ""
        self.content = ""
        self.content1 = ""
        self.content2 = ""
        self.edit_flag = False  # 編集可否フラグ。デフォルトはFalse

        # ***************************************************************************************************
        # about_frame
        self.about_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
        self.about_frame.pack()
        
        # ファイル選択を促すラベル
        self.folder_label = ctk.CTkLabel(self.about_frame,text="■2つのファイルを結合します。")
        self.folder_label.pack()
        # 開始位置を揃える設定 →中身を左に寄せる:anchor="w" ,横幅いっぱいに広げる:fill="x"
        self.folder_label2 = ctk.CTkLabel(self.about_frame,text="・1つ目のファイル末尾に改行がない場合、改行コード(\\n)が挿入されます",anchor="w")
        self.folder_label2.pack(fill="x")
        self.folder_label3 = ctk.CTkLabel(self.about_frame,text="・2つ目のファイルは開始に改行コードがある場合、改行コード(\\n)を削除します",anchor="w")
        self.folder_label3.pack(fill="x")

        # ***************************************************************************************************
        # select_frame frameを左寄せにする
        self.select_frame1 = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.select_frame1.pack()

        # 1つ目のファイル選択を行うボタン ボタンの幅(width=160)と固定することでselect_frameのボタンと位置を合わせる
        self.file_button1 = ctk.CTkButton(self.select_frame1, text="1つ目のファイルを選択", command=self.get_filepath_1, anchor="w")
        self.file_button1.pack(side="left", pady=(10,10),padx=(0,10), fill="x")

        # ディレクトリのパス表示
        self.dir_path1 = ctk.CTkLabel(self.select_frame1, text="path:", width=500, anchor="w")
        self.dir_path1.pack(side="left",pady=(10,10),fill="x")

        # ***************************************************************************************************

        # ***************************************************************************************************
        # select_frame2
        self.select_frame2 = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.select_frame2.pack()

        # ファイルを行うボタン2
        self.file_button2 = ctk.CTkButton(self.select_frame2, text="2つ目ファイルを選択", command=self.get_filepath_2, anchor="w")
        self.file_button2.pack(side="left", pady=(10,10),padx=(0,10), fill="x")

        # ディレクトリのパス表示
        self.dir_path2 = ctk.CTkLabel(self.select_frame2, text="path:", width=500, anchor="w")
        self.dir_path2.pack(side="left",pady=(10,10),fill="x")

        # ***************************************************************************************************

        # ***************************************************************************************************
        # chk_frame
        # ファイル操作チェックframe
        self.chk_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
        self.chk_frame.pack()

        # チェックボックスの状態を保持する変数(初期値がTureだと最初からチェックが入る)
        self.chk_delete_state = ctk.BooleanVar(value=False)
        # ファイル削除チェック
        self.chk_delete = ctk.CTkCheckBox(self.chk_frame,
                                                    text="ファイル出力時に元ファイルを削除する場合はチェックを入れてください",
                                                    variable=self.chk_delete_state,
                                                    # selectcolor="#313131",
                                                    fg_color="#191919",
                                                    text_color="#ffffff")
        self.chk_delete.pack(pady=10)

        # 編集操作ボタン
        self.edit_button = ctk.CTkButton(self.chk_frame, text="編集不可",command=self.edit_toggle,fg_color="#8b0000",hover_color="#b22222")
        self.edit_button.pack(side="left",pady=20,padx=(20,20))

        self.edit_label = ctk.CTkLabel(self.chk_frame, text="※ファイル選択時やプレビュー、選択ファイル逆転ボタンを押下すると編集内容はクリアされます")
        self.edit_label.pack(side="left",pady=20,padx=(20,20))

        # ***************************************************************************************************

        # ***************************************************************************************************
        # text_area_frame
        # テキストエリア用フレーム
        self.textbox_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.textbox_frame.pack(fill="both", expand=True)

        # プレビュー結果
        self.merge_textbox = ctk.CTkTextbox(self.textbox_frame)
        self.merge_textbox.pack(side="left", pady=(20,20),padx=(20,20),fill="both", expand=True)
        # ***************************************************************************************************
        
        # ***************************************************************************************************
        # button_frame
        # ボタン用のフレーム
        self.button_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
        self.button_frame.pack()

        # リバースボタン
        self.merge_reverse_button = ctk.CTkButton(self.button_frame, text="選択ファイル順を逆転", command=self.merge_reverse)
        self.merge_reverse_button.pack(side="left",pady=(10,10),padx=(0,10))

        # ファイルへ出力
        self.execute_extension_button = ctk.CTkButton(self.button_frame, text="ファイルへ出力",command=self.output_file)
        self.execute_extension_button.pack(side="left",pady=20,padx=(20,20))

        # クリアボタン
        self.clear_button = ctk.CTkButton(self.button_frame, text="選択ファイル/テキストボックスのクリア",command=self.all_clear)
        self.clear_button.pack(side="left",pady=20,padx=(20,20))
        # ***************************************************************************************************

    # 1つ目のファイルパスを取得
    def get_filepath_1(self):
        # 以下でファイルを開き、pathとcontentを取得し、1つ目のファイル情報として記録
        self.select_file()

        # 1つ目のファイルの情報を保持
        if self.filepath:
            self.filepath1 = self.filepath
            self.content1 = self.content

            self.dir_path1.configure(text=self.filepath1)
            #textboxに表示
            if self.filepath2:
                self.merge_preview()
            else:
                self.preview(self.content)

    # 2つ目のファイルパスを取得
    def get_filepath_2(self):
        # 以下でファイルを開き、pathとcontentを取得し、2つ目のファイル情報として記録
        self.select_file()

        # 2つ目のファイルの情報を保持        
        if self.filepath:
            self.filepath2 = self.filepath
            self.content2 = self.content
            self.dir_path2.configure(text=self.filepath2)
            #textboxに表示
            if self.filepath1:
                self.merge_preview()
            else:
                self.preview(self.content)

    # ファイルを開く
    def select_file(self):
        #変数の初期化
        self.filepath = ""
        self.content = ""

        # ファイルを選択
        self.filepath = dialogs.select_file()

        if self.filepath:
            try:
                self.content, error = files.read_text_file(self.filepath)
                # fileとcontentを取得後textboxを初期化
                self.fileselect_clear()

                # 確認用
                # print(self.content)
            except Exception as e:
                  messagebox.showerror("エラー",e)
    
    # 2つのファイルが選択されている場合、結合し表示する
    def merge_preview(self):
        # ファイルの選択有無を確認。選択されていないならエラー
        if not self.filepath1 and not self.filepath2:
            messagebox.showerror("エラー","ファイルが選択されていません。")
            return
        #改行重複を避ける結合結果を生成
        # rstripで末尾の改行を削除する
        # lstripで開始の改行を削除する
        merged = self.content1.rstrip("\n") + "\n" + self.content2.lstrip("\n")
        self.preview(merged)
       
    # ファイル選択時に単体でも表示する
    def preview(self, content):
        # edit_flagに関わらずテキストエリアを書き込める状態にし、既存内容を削除
        self.merge_textbox.configure(state="normal")
        self.merge_textbox.delete("1.0", "end") #1行目から最後まで削除            
        self.merge_textbox.insert("1.0", content)
        # 処理が終わったらテキストボックスの編集可否を判定して状態を戻す
        self.edit_mgmt()

    # 選択ファイルの順序を入れ替える
    def merge_reverse(self):
        if self.content1 == "" and self.content2 == "":
            messagebox.showerror("エラー","逆順にするべきファイル内容がありません")
            return

        # content1とcontent2を入れ替える
        self.content1, self.content2 = self.content2, self.content1
        self.filepath1, self.filepath2 = self.filepath2, self.filepath1

        # 画面表示のpathを更新
        self.dir_path1.configure(text=self.filepath1)
        self.dir_path2.configure(text=self.filepath2)

        # previewを行う
        self.merge_preview()

    # merge結果をファイルへ書き込み
    def output_file(self):
        try:
            # text_boxの情報を取得
            # "end-1c"で余計な改行を削除
            content = self.merge_textbox.get("1.0", "end-1c")
            # print(f"コンテンツ:{content}")
            
            # contentがない場合処理しない処理はコメントアウト
            # if not content:
            #     messagebox.showwarning("エラー","結合後のファイル内に書き込む内容がありません")
            #     return

            # 時刻取得
            date = datetime.now().strftime("%Y%m%d_%H%M%S")            
            # ファイルを保存
            filepath = dialogs.save_txt_file(filename=f"merge_file_{date}.txt")

            if filepath:
                #txtファイルへの書き込み
                files.write_txt_file(filepath, content)

                # チェックボックスにチェックが入っており、1or2のどちらかのファイルがあるなら削除確認を行い、"はい"なら削除
                if self.chk_delete_state.get():
                    targets =[p for p in [self.filepath1, self.filepath2] if p]
                    if targets:
                        msg = f"以下のファイルを削除しますか？\n.{targets}を削除しますか?"
                        if messagebox.askyesno("削除の確認",msg):
                            for p in targets:
                                files.remove_file(p)
                    
        except Exception as e:
            messagebox.showerror("エラー",e)
    
    # テキストボックスをクリアする
    def fileselect_clear(self):
        # textareaの初期化
        self.merge_textbox.configure(state="normal")
        self.merge_textbox.delete("1.0", "end") #1行目から最後まで削除
        self.merge_textbox.configure(state="disabled")


    #クリア処理
    def all_clear(self):
        #変数の初期化
        self.filepath = ""
        self.filepath1 = ""
        self.filepath2 = ""
        self.content = ""
        self.content1 = ""
        self.content2 = ""

        # textareaの初期化
        self.merge_textbox.configure(state="normal")
        self.merge_textbox.delete("1.0", "end") #1行目から最後まで削除
        self.merge_textbox.configure(state="disabled")

        self.dir_path1.configure(text="path:")
        self.dir_path2.configure(text="path:")

        # チェックボックスを初期化
        self.chk_delete_state.set(False)

        # 編集可否のクリア
        self.edit_button.configure(text="編集不可",fg_color="#8b0000",hover_color="#b22222")
        self.edit_flag = False


    # 編集許可を行うボタン
    # ボタンはトグルボタンで管理し、edit_flagにより編集可否を判定させる
    def edit_toggle(self):
        if self.edit_flag:
            self.edit_button.configure(text="編集不可",fg_color="#8b0000",hover_color="#b22222")
            self.edit_flag = False
        else:
            self.edit_button.configure(text="編集可能",fg_color="#000080",hover_color="#4169e1")
            self.edit_flag = True
        
        # textboxの設定変更を行おう
        self.edit_mgmt()

    # 編集管理
    def edit_mgmt(self):
        if self.edit_flag:
            self.merge_textbox.configure(state="normal")
        else:
            self.merge_textbox.configure(state="disabled")

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    # インスタンス化
    app = FileMergeApp()
    #イベント待ちループ開始
    app.mainloop()
