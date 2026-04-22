import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from common import files, path_utils, dialogs

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class CsvFormatterApp(ctk.CTk):
    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):
        super().__init__()

        self.configure(fg_color="#191919")
        self.title("Csv Formatter App")
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
        self.file = ""
        self.csv_content = ""

        # ***************************************************************************************************
        # about_frame
        self.about_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
        self.about_frame.pack()
        
        # ファイル選択を促すラベル
        self.folder_label = ctk.CTkLabel(self.about_frame,text="■csvファイルの整形を行います")
        self.folder_label.pack()
        # # 開始位置を揃える設定 →中身を左に寄せる:anchor="w" ,横幅いっぱいに広げる:fill="x"
        self.folder_label2 = ctk.CTkLabel(self.about_frame,text="・改行(\\n)及びタブ(\\t)は表示時にエスケープし、画面上に表示させる",anchor="w")
        self.folder_label2.pack(fill="x")
        # self.folder_label3 = ctk.CTkLabel(self.about_frame,text="・",anchor="w")
        # self.folder_label3.pack(fill="x")

        # ***************************************************************************************************
        # select_frame frameを左寄せにする
        self.select_frame1 = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.select_frame1.pack()

        # ファイル選択を行うボタン
        self.file_button = ctk.CTkButton(self.select_frame1, text="ファイルを選択", command=self.get_filepath, anchor="w")
        self.file_button.pack(side="left", pady=(10,10),padx=(0,10), fill="x")

        # ディレクトリのパス表示
        self.dir_path = ctk.CTkLabel(self.select_frame1, text="path:", width=500, anchor="w")
        self.dir_path.pack(side="left",pady=(10,10),fill="x")

        # ***************************************************************************************************

        # ***************************************************************************************************
        # chk_frame
        # ファイル操作チェックframe
        self.chk_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
        self.chk_frame.pack()

        # チェックボックスの状態を保持する変数(初期値がTureだと最初からチェックが入る)
        # 空白削除チェック
        self.chk_balnk = ctk.BooleanVar(value=False)
        self.chk_balnk_box = ctk.CTkCheckBox(self.chk_frame,
                                                    text="空白(全半角どちらも)を削除する場合はチェックを入れてください",
                                                    variable=self.chk_balnk,
                                                    # selectcolor="#313131",
                                                    fg_color="#191919",
                                                    text_color="#ffffff")
        self.chk_balnk_box.pack(pady=10)
        # 改行,タブ削除チェック
        self.chk_lf = ctk.BooleanVar(value=False)
        self.chk_lf_box = ctk.CTkCheckBox(self.chk_frame,
                                                    text="改行(\\n)及びタブ(\\t)を削除する場合はチェックを入れてください",
                                                    variable=self.chk_lf,
                                                    # selectcolor="#313131",
                                                    fg_color="#191919",
                                                    text_color="#ffffff")
        self.chk_lf_box.pack(pady=10)
        # ***************************************************************************************************

        # ***************************************************************************************************
        # text_area_frame
        # テキストエリア用フレーム
        self.textbox_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.textbox_frame.pack(fill="both", expand=True)

        # プレビュー結果
        self.textbox = ctk.CTkTextbox(self.textbox_frame, state="disabled")
        self.textbox.pack(side="left", pady=(20,20),padx=(20,20),fill="both", expand=True)
        # ***************************************************************************************************
        
        # ***************************************************************************************************
        # button_frame
        # ボタン用のフレーム
        self.button_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
        self.button_frame.pack()

        # preview
        self.replace_button = ctk.CTkButton(self.button_frame, text="プレビュー",command=self.apply_and_refresh)
        self.replace_button.pack(side="left",pady=20,padx=(20,20))

        # 最長要素へカンマ合わせ削除
        # 没機能 フォントや、全角半角によってきれいにきれいに整形出来ない
        # self.longest_button = ctk.CTkButton(self.button_frame, text="最長要素に合わせる",command=self.along_csv_columns)
        # self.longest_button.pack(side="left",pady=20,padx=(20,20))

        # ファイルへ出力
        self.execute_extension_button = ctk.CTkButton(self.button_frame, text="ファイルへ出力",command=self.output_file)
        self.execute_extension_button.pack(side="left",pady=20,padx=(20,20))

        # クリアボタン
        self.clear_button = ctk.CTkButton(self.button_frame, text="選択ファイル/テキストボックスのクリア",command=self.all_clear)
        self.clear_button.pack(side="left",pady=20,padx=(20,20))
        # ***************************************************************************************************

    # ファイルパスを取得
    def get_filepath(self):

        # 既存情報を削除
        self.all_clear()

        # 以下でファイルを開き、pathとcontentを取得し、1つ目のファイル情報として記録
        self.select_file()

        # ファイルの情報を保持
        if self.filepath:
            self.dir_path.configure(text=self.filepath)
            self.csv_preview(self.csv_content)

    # ファイルを開く
    def select_file(self):
        # ファイルを選択
        self.filepath = dialogs.select_file()

        if self.filepath:
            try:
                # ファイル名だけ取得
                self.file = os.path.basename(self.filepath)
                # csvとして読み込む
                self.csv_content = files.read_csv_file(self.filepath)

            except Exception as e:
                  messagebox.showerror("エラー",e)
       
    # ファイル選択時表示する
    def csv_preview(self, content):

        #区切り文字の変更
        delimiter = "|"

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end") #1行目から最後まで削除

        # csvを読み込んでいる想定カラムの設定             
        # 以下でlist化する時、カラム行より多い要素があるとき、その列をNoneとして格納してしまう
        # columns = list(record[0].keys())
        # colがNoneの時はcolumnsに含めないよう以下とする
        columns = [col for col in content[0].keys() if col]
        self.textbox.insert("1.0", f"{delimiter}".join(columns))
        self.textbox.insert("end", "\n")

        # print("改行確認")

        for r in content:
            # print(f"{repr(r)}")
            values = [self.format_for_display(r.get(col)) for col in columns]

            # csvとUIを分ける為、区切りを変更
            self.textbox.insert("end", f"{delimiter}".join(values))
            self.textbox.insert("end", "\n")
        self.textbox.configure(state="disabled")

    # 表示用にエスケープする処理
    def format_for_display(self, value):
        if value is None:
            return ""
        return value.replace("\n", "\\n").replace("\t", "\\t")

    # csvの要素から対象を削除する
    def subject_replace(self, subject):

        # 空白削除した新しいlistを用意
        new_record = []
        # # 内部値確認用
        # for key in self.csv_content[0]:
        #     # カラム行のみ
        #     print("key :",key)
        #     for value in self.csv_content:
        #         # 値行のみ
        #         print("value :", value[key])

        # 1行ずつ取り出す
        for row in self.csv_content:
            new_row = {}
            for key, value in row.items():
                if value is not None:
                    new_value = value
                    for s in subject:
                        new_value = new_value.replace(s, "")     
                    new_row[key] = new_value
                else:
                    new_row[key] = value
            new_record.append(new_row)
        # 保持情報も削除後に入れ替え
        self.csv_content = new_record
        # print(self.csv_content)
    
    # プレビュー押下時に空白、改行、タブの削除確認を行う
    def apply_and_refresh(self):
        # 入力チェック
        if not self.csv_content:
            messagebox.showerror("エラー", "csvデータがありません")
            return
        # チェックボックス状態を見てすべて適用
        if self.chk_balnk.get():
            # csvの要素から空白を削除する
            # 空白はすべて削除
            self.subject_replace([" ", "　"])
        if self.chk_lf.get():
            # csvの要素から改行及びタブを削除する
            self.subject_replace(["\n", "\t"])
        
        self.csv_preview(self.csv_content)


    # csvの各行の最長要素を検索し、それにカンマ位置を合わせる
    # 没にするが一応残しておく
    def along_csv_columns(self):

        # 空白削除した新しいlistを用意
        new_record = []
        max_len = 0

        # 1行ずつ取り出す
        for row in self.csv_content:
            new_row = {}
            for key, value in row.items():
                # valueの要素の一番長いものを取得しておく
                if len(value) > max_len  :
                    max_len = len(value)
            if len(key) > max_len:
                max_len= len(key)

            # もう一度forを回して、max_lenに合わせる
            for key, value in row.items():
                if value is not None:
                    new_row[key] = value.ljust(max_len)
                else:
                    new_row[key] = value.ljust(max_len)
            new_record.append(new_row)
        self.csv_preview(new_record)

    # ファイルへ書き込み
    def output_file(self):
        try:
            # 入力チェック
            if not self.csv_content:
                messagebox.showerror("エラー","出力内容がありません")
                return

            # カラム行の作成
            columns = [col for col in self.csv_content[0].keys() if col]

            # ファイル名を作成
            # 既存ファイル名があるならそれを使用
            # 既存ファイル名がない場合csv_formatter_YYYYMMDD.csvとする
            if self.file:
                filepath = dialogs.save_csv_file(filename=f"{self.file}")
            else:
                # 時刻取得
                date = datetime.now().strftime("%Y%m%d_%H%M%S")            
                filepath = dialogs.save_csv_file(filename=f"csv_formatter_{date}.csv")

            if filepath:
                # print(f"カラム行:{columns}")
                # print(f"コンテンツ行:{self.csv_content}")
                # csvファイルへの書き込み
                files.write_csv_file_dict(filepath, columns, self.csv_content)
                
        except Exception as e:
            messagebox.showerror("エラー",e)

    #クリア処理
    def all_clear(self):
        #変数の初期化
        self.filepath = ""
        self.file = ""
        self.csv_content = ""

        # textareaの初期化
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end") #1行目から最後まで削除
        self.textbox.configure(state="disabled")

        self.dir_path.configure(text="path:")

        # チェックボックスを初期化
        self.chk_balnk.set(False)
        self.chk_lf.set(False)

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    # インスタンス化
    app = CsvFormatterApp()
    #イベント待ちループ開始
    app.mainloop()
