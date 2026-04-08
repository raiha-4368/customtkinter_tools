import os
import unicodedata
import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class TextExtractApp(ctk.CTk):
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
        self.main_frame.pack()

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

        # フォルダ選択を促すラベル
        self.folder_label = ctk.CTkLabel(self.main_frame, text="選択されたファイル内から検索文字列を含む行を探します",fg_color="#191919",text_color="#ffffff")
        self.folder_label.pack()

        # ***************************************************************************************************
        # about_frame
        # リストボックス用のラベルとリストボックス自体の表示用フレーム
        self.about_frame = ctk.CTkFrame(self.main_frame,fg_color="#191919")
        self.about_frame.pack()

        # ファイルを行うボタン
        self.file_button = ctk.CTkButton(self.about_frame, text="ファイルを選択", command=self.select_file)
        self.file_button.pack(side="left",pady=(10,10),padx=(0,10))

        # ディレクトリのパス表示
        self.dir_path = ctk.CTkLabel(self.about_frame, text="path:",fg_color="#191919",text_color="#ffffff")
        self.dir_path.pack(side="left",pady=(10,10))
        # ***************************************************************************************************

        # ***************************************************************************************************
        # search_frame
        # 検索文字列入力フレーム
        self.search_frame = ctk.CTkFrame(self.main_frame, fg_color="#191919")
        self.search_frame.pack()

        # 検索文字列の入力ラベル
        self.search_word_label = ctk.CTkLabel(self.search_frame, text="検索文字列入力")
        self.search_word_label.pack(side="left", pady=(20,20),padx=(20,20))
        # 検索文字列入力欄
        self.search_word = ctk.CTkEntry(self.search_frame)
        self.search_word.pack(side="left", pady=(20,20),padx=(20,20))

        # チェックボックスの状態を保持する変数(初期値がTureだと最初からチェックが入る)
        self.chk_exact_match_state = ctk.BooleanVar(value=False)
        # 完全一致のチェック
        self.chk_exact_match = ctk.CTkCheckBox(self.search_frame,
                                                    text="完全一致で検索する場合はチェックを入れてください",
                                                    variable=self.chk_exact_match_state,
                                                    # selectcolor="#313131",
                                                    fg_color="#191919",
                                                    text_color="#ffffff")
        self.chk_exact_match.pack(pady=10)

        # 大文字小文字を区別するかのチェック
        self.chk_is_case_sensitive_state = ctk.BooleanVar()     
        self.chk_is_case_sensitive = ctk.CTkCheckBox(self.search_frame,
                                                    text="大文字小文字を区別しない場合はチェックを入れてください",
                                                    variable=self.chk_is_case_sensitive_state,
                                                    # selectcolor="#313131",
                                                    fg_color="#191919",
                                                    text_color="#ffffff")
        self.chk_is_case_sensitive.pack(pady=10)

        # ***************************************************************************************************

        # ***************************************************************************************************
        # text_area_frame
        # テキストエリア用フレーム
        self.text_area_frame = ctk.CTkFrame(self.main_frame, fg_color="#191919")
        self.text_area_frame.pack()

        # テキストエリア
        self.text_area_before = ctk.CTkTextbox(self.text_area_frame,state='disabled')
        self.text_area_before.pack(side="left", pady=(20,20),padx=(20,20))
        # テキストエリアの大きさ調整の為コメントアウト。後でpack(width=50, height=50,expand=True, fill="both")
        # ⇒
        self.arrow_label = ctk.CTkLabel(self.text_area_frame, text="⇒",fg_color="#191919",text_color="#ffffff")
        self.arrow_label.pack(side="left", padx=(5,5))
        # 検索結果
        self.text_area_after = ctk.CTkTextbox(self.text_area_frame)
        self.text_area_after.pack(side="left", pady=(20,20),padx=(20,20))
        # テキストエリアの大きさ調整の為コメントアウト。後でpack(width=50, height=50, expand=True, fill="both")
        # ***************************************************************************************************
        
        # ***************************************************************************************************
        # button_frame
        # ボタン用のフレーム
        self.button_frame = ctk.CTkFrame(self.main_frame,fg_color="#191919")
        self.button_frame.pack()

        # 対象ファイルから検索文字列を含む行を抜き出す
        self.preview_button = ctk.CTkButton(self.button_frame, text="検索開始",command=self.read_line_file)
        self.preview_button.pack(side="left",pady=20,padx=(20,20))

        # ファイルへ出力
        self.execute_extension_button = ctk.CTkButton(self.button_frame, text="ファイルへ出力",command=self.output_file)
        self.execute_extension_button.pack(side="left",pady=20,padx=(20,20))

        # クリアボタン
        self.clear_button = ctk.CTkButton(self.button_frame, text="ファイル/テキストエリアのクリア",command=self.clear_data)
        self.clear_button.pack(side="left",pady=20,padx=(20,20))
        # ***************************************************************************************************

    # ファイルを開く
    def select_file(self):

        # 今までの入力値をクリア
        self.clear_data()

        self.filepath = filedialog.askopenfilename(
          defaultextension=".txt",
          filetypes=[("All files", "*.*")],
          title="ファイルを開く"
      )
        if self.filepath:
            try:
                with open(self.filepath, mode='r', encoding="utf-8") as f:
                    content = f.read()
                    # print(content)
                    # テキストエリアを一度空にしてから読み込んだ内容を挿入
                    self.text_area_before.configure(state="normal")
                    self.text_area_before.delete("1.0", "end") #1行目から最後まで削除
                    self.text_area_before.insert("1.0", content) #1行目に挿入
                    self.text_area_before.configure(state="disabled")

                # オプション 今開いているファイル名をタイトルに表示
                self.title(f"Text Extract App - {self.filepath}")

                # selfにファイルパスを持たせておく
                self.dir_path.configure(text=self.filepath)

            except Exception as e:
                  messagebox.showerror("エラー",e)

    
    # ファイルを一行ずつ読み込み、検索文字列行を抜き出す
    def read_line_file(self):
        # resultを初期化
        self.result = []

        # ファイルの選択有無を確認。選択されていないならエラー
        if self.filepath == "":
            messagebox.showerror("エラー","ファイルが選択されていません。")
            return
        # 検索対象文字列の有無を確認。入力されていないならエラー
        self.get_word = self.search_word.get()
        if self.get_word == "":
            messagebox.showerror("エラー","検索対象文字が入力されていません。")
            return

        # 読み込みモードr
        with open(self.filepath, 'r',encoding='utf-8') as f:
            # 新しい処理
            for i, line in enumerate(f, start=1):
                self.line_search(i,line.strip())

        # ファイルの読み込み終了後
        # テキストエリアを書き込める状態にし、既存内容を削除
        self.text_area_after.configure(state="normal")
        self.text_area_after.delete("1.0", "end") #1行目から最後まで削除    
        # 検索結果があればテキストエリアにインサート
        if self.result:
            insert_num = 0
            for r in self.result:
                insert_num += 1
                self.text_area_after.insert(f"{insert_num}.0", f"{r[2]}\n")
        else:
            messagebox.showerror("エラー","検索文字との一致が見つけられませんでした。")
        # 処理が終わったらテキストエリアの書き込めない状態にする
        self.text_area_after.configure(state="disabled")


    # 一列受け取って、文字列を含むかどうかの判定
    def line_search(self, num, line):
        # TODO reモジュール(正規表現)の方が処理が書きやすいかもしれないですが現状はコレでいきます。
        # 大文字小文字を無視する場合
        if self.chk_is_case_sensitive_state.get():
            word_lower = self.get_word.lower()
            line_lower = line.lower()
            # 完全一致
            if self.chk_exact_match_state.get():
                if word_lower == line_lower:
                    # print(f"大文字小文字を無視&完全一致")
                    self.result.append((self.filepath, num, line))
            # 部分一致
            else:
                if word_lower in line_lower:
                    # print(f"大文字小文字を無視&部分一致")
                    self.result.append((self.filepath, num, line))
        # 大文字小文字を区別する場合
        else:
            # 完全一致
            if self.chk_exact_match_state.get():
                if self.get_word == line:
                    # print(f"大文字小文字を区別&完全一致")
                    self.result.append((self.filepath, num, line))
            # 部分一致
            else:
                if self.get_word in line:
                    # print(f"大文字小文字を区別&部分一致")
                    self.result.append((self.filepath, num, line))

    # 検索結果をファイルへ書き込み
    def output_file(self):
        try:
            # text_areaの情報を取得
            # "end-1c"で余計な改行を削除
            content = self.text_area_after.get("1.0", "end-1c")
            print(f"コンテンツ:{content}")
            
            # 検索を行っていない場合、処理しない
            if not content:
                messagebox.showwarning("エラー","検索を実行してください。")
                return

            # 時刻取得
            date = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            filepath = filedialog.asksaveasfilename(
                defaultextension = ".csc",
                initialfile=f"{self.get_word}_{date}.csv", 
                filetypes=[("csv files", "*.csv")],
                title="textファイルを保存"
                )
            if filepath:
                # カラム行作成
                column = ["filepath","line_num","content"]

            #新規書き込みw,追記モードaで使い分け
                with open(filepath, mode='w', newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    # ヘッダー書き込み
                    writer.writerow(column)
                    # resultの書き込み
                    for row in self.result:
                        writer.writerow(row)

        except Exception as e:
            messagebox.showerror("エラー",e)

       
    #クリア処理
    def clear_data(self):
        #変数の初期化
        self.filepath = ""
        self.exact_match_flag = False
        self.result = []

        # 画面に表示したパスをクリア
        self.dir_path.configure(text="path:")

        # 検索対象文字列をクリア
        self.search_word.delete(0, ctk.END)

        # チェックボックスを初期化
        self.chk_exact_match_state.set(False)
        self.chk_is_case_sensitive_state.set(False)

        # textareaの初期化
        self.text_area_before.configure(state="normal")
        self.text_area_before.delete("1.0", "end") #1行目から最後まで削除
        self.text_area_before.configure(state="disabled")
        self.text_area_after.configure(state="normal")
        self.text_area_after.delete("1.0", "end") #1行目から最後まで削除
        self.text_area_after.configure(state="disabled")

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    # インスタンス化
    app = TextExtractApp()
    #イベント待ちループ開始
    app.mainloop()
