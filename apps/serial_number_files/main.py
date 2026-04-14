import os
import unicodedata
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from common import dialogs

# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class SerialNumberFilesApp(ctk.CTk):
    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):
        super().__init__()        
        
        self.configure(fg_color="#233B6C")
        self.title("Serial Number Files Files App")
        self.geometry("1200x800")

        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = ctk.CTkFrame(self, fg_color="#233B6C")
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
        self.number = 1
        self.digit = 2
        self.folder = None
        self.files = None
        self.preview_result = []
        self.clear_flag = True

        # フォルダ選択を促すラベル
        self.folder_label = ctk.CTkLabel(self.main_frame, text="対象フォルダ以下のフォルダ/ファイル名の先頭に連番を付与します。(000～999)",fg_color="#233B6C",text_color="#ffffff")
        self.folder_label.pack()

        # リストボックス用のラベルとリストボックス自体の表示用フレーム
        self.about_frame = ctk.CTkFrame(self.main_frame,fg_color="#233B6C")
        self.about_frame.pack()

        # フォルダ選択を行うボタン
        self.folder_button = ctk.CTkButton(self.about_frame, text="フォルダを選択", command=self.select_folder)
        self.folder_button.pack(side="left",pady=(10,10),padx=(0,10))

        # ディレクトリのパス表示
        self.dir_path = ctk.CTkLabel(self.about_frame, text="path:",fg_color="#233B6C",text_color="#ffffff")
        self.dir_path.pack(side="left",pady=(10,10))

        # 連番開始時の数値の入力フレーム
        self.number_digits_label_frame = ctk.CTkFrame(self.main_frame,fg_color="#233B6C")
        self.number_digits_label_frame.pack()

        # 連番開始数の入力
        self.serial_number_label = ctk.CTkLabel(self.number_digits_label_frame, text="連番開始数(数値のみ)",fg_color="#233B6C",text_color="#ffffff")
        self.serial_number_label.pack(side="left", pady=(10,10),padx=(0,0))
        self.serial_number_entry = ctk.CTkEntry(self.number_digits_label_frame)
        self.serial_number_entry.pack(side="left", pady=(10,10), padx=(20,50))
        self.serial_number_entry.insert(0,1)

        # ラジオボタンの桁数ラベル
        self.radio_label = ctk.CTkLabel(self.number_digits_label_frame, text="桁数設定", fg_color="#233B6C",text_color="#ffffff")
        self.radio_label.pack(side="left")
        # ラジオボタン用
        self.select_digits = (1,2,3)
        # ラジオボタンの共通変数(この変数で1つのラジオボタンと認識させ、デフォルトのセット値を2とする)
        # self.selected_value.get()でラジオボタンの入力値を取得する
        self.selected_value = ctk.IntVar(value=2)

        # ラジオボタンの〇の中の色は背景色より少し明るめとしている
        for d in self.select_digits:
            self.serial_radio = ctk.CTkRadioButton(self.number_digits_label_frame,
                                                   text=f"{d}桁",
                                                   value=d,
                                                   variable=self.selected_value,
                                                   border_color="#000000",
                                                   fg_color="#ffffff",
                                                   hover_color="#ddfd4f",
                                                   text_color="#ffffff")
            self.serial_radio.pack(anchor=tk.W) #radio1ウィジットを配置
        
        # radio_var = tk.IntVar(value=0)
        # radiobutton_1 = ctk.CTkRadioButton(self.number_digits_label_frame, text="CTkRadioButton 1",
        #                                      command=None, variable= radio_var, value=1)
        # radiobutton_1.pack()
        # radiobutton_2 = ctk.CTkRadioButton(self.number_digits_label_frame, text="CTkRadioButton 2",
        #                                      command=None, variable= radio_var, value=2)
        # radiobutton_2.pack()

        # リストボックス用のフレーム
        self.list_frame = ctk.CTkFrame(self.main_frame,fg_color="#233B6C")
        self.list_frame.pack(fill="both", expand=True)
        #履歴表示用リストボックス
        # ビフォー
        # self.before_listbox = tk.Listbox(self.list_frame, width=50)
        # self.before_listbox.pack(side="left",fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.listbox_before_frame = ctk.CTkScrollableFrame(self.list_frame, label_text="選択フォルダ内のリスト")
        self.listbox_before_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # ⇒
        self.arrow_label = ctk.CTkLabel(self.list_frame, text="⇒",fg_color="#233B6C",text_color="#ffffff")
        self.arrow_label.pack(side="left", padx=(5,5))
        # アフター
        # self.after_listbox = tk.Listbox(self.list_frame, width=50)
        # self.after_listbox.pack(side="left",fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.listbox_after_frame = ctk.CTkScrollableFrame(self.list_frame, label_text="選択フォルダ内のリスト")
        self.listbox_after_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # ボタン用のフレーム
        self.button_frame = ctk.CTkFrame(self.main_frame,fg_color="#233B6C")
        self.button_frame.pack()

        # 対象件数表示ラベル
        self.target_len_label = ctk.CTkLabel(self.button_frame, text="連番対象はありません",fg_color="#233B6C",text_color="#ffffff")
        self.target_len_label.pack(pady=(20,20))

        # プレビューボタン
        self.preview_button = ctk.CTkButton(self.button_frame, text="連番プレビュー",command=self.preview)
        self.preview_button.pack(side="left",pady=20,padx=(20,20))

        # 実行ボタン
        self.execute_serial_button = ctk.CTkButton(self.button_frame, text="連番付与実行",command=self.execute_serial)
        self.execute_serial_button.pack(side="left",pady=20,padx=(20,20))

        # クリアボタン
        self.clear_button = ctk.CTkButton(self.button_frame, text="フォルダ選択のクリア",command=self.clear_data)
        self.clear_button.pack(side="left",pady=20,padx=(20,20))


    # フォルダを選択
    def select_folder(self):
        # フォルダを選択しなおしたとき等、画面上を一旦クリアする
        self.clear_flag = False
        self.clear_data()
        # フォルダ選択時以外はTrueとなるようにしておく
        self.clear_flag = True

        # フォルダを開くダイアログ
        self.folder = dialogs.select_folder()

        print(self.folder)

        if not self.folder:
          messagebox.showerror("エラー","フォルダが選択されていません。")
          return

        # 画面にパスを表示 pathが長い時用に,anchor="w"の設定を追加
        self.dir_path.configure(text=f"path:{self.folder}",anchor="w")

        self.files = os.listdir(self.folder)
        # self.before_listbox.delete(0,tk.END)
        # リスト用のボタン削除
        for child in self.listbox_before_frame.winfo_children():          
            child.destroy()

        for f in self.files:
        #   self.before_listbox.insert(tk.END,f)
            # スクロールラベルバーにボタンを追加
            btn = ctk.CTkButton(self.listbox_before_frame, text=f,  fg_color="#FFFFFF",text_color="#000000", anchor="w", command=None)
            btn.pack(fill="x")


        #プレビュー押下を促す表示
        self.target_len_label.configure(text="プレビューを実行してください")

    # プレビュー
    # フォルダが選択されている時、プレビューボタンを押下することで変更後を表示する
    def preview(self):
        if not self.folder:
            messagebox.showerror("エラー","フォルダが選択されていません。")
            return

        # 型変換でのエラーを取得するためtry使用
        try:
            # 連番開始数を取得(全角/半角対応)
            self.number = int(unicodedata.normalize("NFKC",self.serial_number_entry.get()))
            # ラジオボタンの値を取得(1~3の想定)
            self.digit = int(self.selected_value.get())

        except Exception as e:
            messagebox.showerror("エラー","連番開始数または桁数が不正です")

        # リネーム後、プレビューを押下されたとき用にもう一度、フォルダからファイルの状態を読み込む
        self.files = os.listdir(self.folder)
        # self.before_listbox.delete(0,tk.END)
        # リスト用のボタン削除
        for child in self.listbox_before_frame.winfo_children():          
            child.destroy()

        for f in self.files:
            # self.before_listbox.insert(tk.END,f)
            # スクロールラベルバーにボタンを追加
            btn = ctk.CTkButton(self.listbox_before_frame, text=f,  fg_color="#FFFFFF",text_color="#000000", anchor="w", command=None)
            btn.pack(fill="x")

        # listboxとプレビュー結果格納変数の初期化
        # self.after_listbox.delete(0,tk.END)
        # リスト用のボタン削除
        for child in self.listbox_after_frame.winfo_children():          
            child.destroy()
        self.preview_result = []
        for f in self.files:
            self.preview_result.append((f,self.serial_number_preview(f)))
            # self.after_listbox.insert(tk.END,self.serial_number_preview(f))
            # スクロールラベルバーにボタンを追加
            btn = ctk.CTkButton(self.listbox_after_frame, text=self.serial_number_preview(f),  fg_color="#FFFFFF",text_color="#000000", anchor="w", command=None)
            btn.pack(fill="x")
            self.number +=1
        
        # 変更対象が存在しない時、エラーメッセージを表示し、プレビューの結果を削除する
        preview_count = 0
        for old, new in self.preview_result:
            # 一つでもoldとnewの相違があれば、flagをTureとする
            if old != new:
                preview_count += 1

        # 上記で変更対象が見つからず、flagがfalseだった時、エラーメッセージを表示する
        if preview_count == 0:
            messagebox.showerror("エラー","変更対象が存在しません")
            # self.after_listbox.delete(0,tk.END)
            # リスト用のボタン削除
            for child in self.listbox_after_frame.winfo_children():          
                child.destroy()
            self.preview_result = []

        # 対象件数を表示
        self.target_len_label.configure(text=f"連番対象は{preview_count} 件です")

    # 連番付与
    def serial_number_preview(self,filename):
        return f"{self.number:0{self.digit}d}_{filename}"
    
    # ファイル名変換処理
    def execute_serial(self):
        try:
            # プレビューを実行していない場合、処理しない
            if not self.preview_result:
                messagebox.showwarning("エラー","プレビューを実行してください。")
                return

            exe_flag = False
            error = ""
            for old,new in self.preview_result:
                #確認用
                #print(f"変換前:{old} ⇒変換後:,{new}")
                old_path = os.path.join(self.folder, old)
                new_path = os.path.join(self.folder, new)
               
               # 変換対象(old)が無くなっていた場合のエラーを設定
                if not os.path.exists(old_path):
                    error += f"{old}\n"
                    continue

                #一致していたら変換処理をする意味がないので処理対象外とする
                if old != new:
                    
                    # ファイル名をnew_pathに変える
                    os.rename(old_path, new_path)
                    exe_flag = True
            if exe_flag:
                messagebox.showinfo("Successful","対象フォルダ下にあるフォルダ/ファイルへの連番付与に成功しました。")
            elif error != "":
                messagebox.showerror("エラー",f"以下対象ファイルが存在しません。\n{error}")
            else:
                messagebox.showerror("エラー","フォルダ下に対象が存在しません")

        except Exception as e:
            messagebox.showerror("エラー",e)

    #クリア処理
    def clear_data(self):
        #変数の初期化
        self.folder = None
        self.files = None
        self.preview_result = []

        # 画面に表示したパスをクリア
        self.dir_path.configure(text="path:")

        #件数ラベルを初期化
        self.target_len_label.configure(text="連番対象はありません")

        # ファイル選択時にはリセットしない
        if self.clear_flag:
            #連番開始数をリセット
            self.serial_number_entry.delete(0,tk.END)
            self.serial_number_entry.insert(0,1)

            #ラジオボタンのリセット
            self.selected_value.set(2)

        # リスト用のボタン削除
        for child in self.listbox_before_frame.winfo_children():          
            child.destroy()

        # リスト用のボタン削除
        for child in self.listbox_after_frame.winfo_children():          
            child.destroy()
       
# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #インスタンス化
    app = SerialNumberFilesApp()
    #イベント待ちループ開始
    app.mainloop()
