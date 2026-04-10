import os
import unicodedata
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

class ExtensionSortApp(ctk.CTk):
    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):
        super().__init__()

        self.configure(fg_color="#233B6C")
        self.title("Extension Sort App")
        self.geometry("1400x800")

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

        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="メニュー",menu=file_menu)
        file_menu.add_command(label="終了", command=self.quit)

        #変数宣言(エラーにならないように宣言)
        self.folder = None
        self.files = None
        self.preview_result = []
        self.error_result = []
        self.ext_count = {}
        self.ext_flag = False


        # フォルダ選択を促すラベル
        self.folder_label = ctk.CTkLabel(self.main_frame, text="対象フォルダ以下のファイルを拡張子毎のフォルダに振り分けます。",fg_color="#233B6C",text_color="#ffffff")
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
        
        # リストボックス用のフレーム
        self.list_frame = ctk.CTkFrame(self.main_frame,fg_color="#233B6C")
        self.list_frame.pack(fill="both", expand=True) # この設定でframeを広げている
        #履歴表示用リストボックス
        # ビフォー
        # ctkにlistboxはない為、listboxを使用する場合はtkinterを使用しなければならない
        # なのでlistboxではなくスクロールラベルバーにボタンを実装する形で再現する
        self.listbox_before_frame = ctk.CTkScrollableFrame(self.list_frame, label_text="選択フォルダ内のリスト")
        self.listbox_before_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # リストのアイテムをボタンとして追加
        # 初期状態はボタンがない状態なのでコメントアウト
        # 以下の処理のcommandはボタン押下時に選択対象をコンソールに表示するものとなっている
        # items = [”"""]
        # for item in items:
        #     self.btn = ctk.CTkButton(self.listbox_frame, text=item,  fg_color="transparent", anchor="w", command=lambda x=item: print(f"Selected: {x}"))
        #     self.btn.pack(fill="x")

        # ⇒
        self.arrow_label = ctk.CTkLabel(self.list_frame, text="⇒",fg_color="#233B6C",text_color="#ffffff")
        self.arrow_label.pack(side="left", padx=(5,5))

        # アフター
        self.listbox_after_frame = ctk.CTkScrollableFrame(self.list_frame, label_text="選択フォルダ内の変換後リスト")
        self.listbox_after_frame.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # ボタン用のフレーム
        self.button_frame = ctk.CTkFrame(self.main_frame,fg_color="#233B6C")
        self.button_frame.pack()

        # 対象件数表示ラベル
        self.target_len_label = ctk.CTkLabel(self.button_frame, text="対象はありません",fg_color="#233B6C",text_color="#ffffff")
        self.target_len_label.pack(pady=(20,20))

        # プレビューボタン
        self.preview_button = ctk.CTkButton(self.button_frame, text="振り分けプレビュー",command=self.preview)
        self.preview_button.pack(side="left",pady=20,padx=(20,20))

        # 実行ボタン
        self.execute_extension_button = ctk.CTkButton(self.button_frame, text="拡張子別振り分け実行",command=self.execute_extension)
        self.execute_extension_button.pack(side="left",pady=20,padx=(20,20))

        # クリアボタン
        self.clear_button = ctk.CTkButton(self.button_frame, text="フォルダ選択のクリア",command=self.clear_data)
        self.clear_button.pack(side="left",pady=20,padx=(20,20))


    # フォルダを選択
    def select_folder(self):
        # フォルダを選択しなおしたとき等、画面上を一旦クリアする
        self.clear_data()

        self.folder = filedialog.askdirectory()
        # 確認用
        # print(self.folder)
        if not self.folder:
          messagebox.showerror("エラー","フォルダが選択されていません。")
          return

        # 画面にパスを表示 pathが長い時用に,anchor="w"の設定を追加
        self.dir_path.configure(text=f"path:{self.folder}",anchor="w")

        # ファイルの一覧を取得
        self.files = os.listdir(self.folder)

        # リスト用のボタン削除
        for child in self.listbox_before_frame.winfo_children():          
            child.destroy()

        # スクロールラベルバーにボタンを追加
        for f in self.files:
            ext = self.extension_sort_preview(f)
            if ext != "":
                btn = ctk.CTkButton(self.listbox_before_frame, text=f,  fg_color="#FFFFFF",text_color="#000000", anchor="w", command=None)
                btn.pack(fill="x")
            else:
                btn = ctk.CTkButton(self.listbox_before_frame, text=f,  fg_color="#696969",text_color="#000000", anchor="w", command=None)
                btn.pack(fill="x")
                

        #プレビュー押下を促す表示
        self.target_len_label.configure(text="プレビューを実行してください")

    # プレビュー
    # フォルダが選択されている時、プレビューボタンを押下することで変更後を表示する
    def preview(self):
        # 実行フラグをfalseにしておく
        self.ext_flag = False

        if not self.folder:
            messagebox.showerror("エラー","フォルダが選択されていません。")
            return
        
        # カウント用変数の初期化
        self.ext_count = {}

        # リネーム後、プレビューを押下されたとき用にもう一度、フォルダからファイルの状態を読み込む
        self.files = os.listdir(self.folder)
        
        # ビフォーリスト用のボタン削除
        for child in self.listbox_before_frame.winfo_children():          
            child.destroy()
 
        # プレビュー押下時にファイル情報を再取得する
        for f in self.files:
            ext = self.extension_sort_preview(f)
            if ext != "":
                btn = ctk.CTkButton(self.listbox_before_frame, text=f,  fg_color="#FFFFFF",text_color="#000000", anchor="w", command=None)
                btn.pack(fill="x")
            else:
                btn = ctk.CTkButton(self.listbox_before_frame, text=f,  fg_color="#696969",text_color="#000000", anchor="w", command=None)
                btn.pack(fill="x")
 
        # ディレクトリ情報
        # print("test",self.folder)
        
        # プレビュー結果格納変数の初期化
        self.preview_result = []
        preview_flag = False
        # アフターリスト用のボタン削除
        for child in self.listbox_after_frame.winfo_children():          
            child.destroy()
        
        for f in self.files:
            # ファイル名とディレクトリ名(ファイルの場合は空)をresultに格納
            ext = self.extension_sort_preview(f)
            self.preview_result.append((f,ext))
            # ""じゃなければディレクトリ名と結合して表示
            if ext != "":
                # self.after_listbox.insert(tk.END,f"{f}/{ext}")
                btn = ctk.CTkButton(self.listbox_after_frame, text=f"{ext}/{f}",  fg_color="#FFFFFF",text_color="#000000", anchor="w", command=None)
                btn.pack(fill="x")
                preview_flag = True
            else:
                # self.after_listbox.insert(tk.END,f"{f}")
                btn = ctk.CTkButton(self.listbox_after_frame, text=f"{f}",  fg_color="#696969",text_color="#000000", anchor="w", command=None)
                btn.pack(fill="x")
        
        # 変更対象が存在しない時、エラーメッセージを表示し、プレビューの結果を削除する
        if not preview_flag:
            messagebox.showerror("エラー","変更対象が存在しません")
            # self.after_listbox.delete(0,tk.END)
            # リスト用のボタン削除
            for child in self.listbox_after_frame.winfo_children():          
                child.destroy()
            self.preview_result = []

        # 対象件数を表示
        # dict型にitems()を付け加えることでkeyとvalueのどちらも取得可能にする →self.ext_count.items()
        text = ""
        for ext, count in sorted(self.ext_count.items()):
            text += f"\n{ext}: {count}件"
        self.target_len_label.configure(text=f"以下振り分け対象です{text}")


    # 拡張子ごとに振り分け
    def extension_sort_preview(self,filename):
        # フォルダは対象外
        if not os.path.isfile(f"{self.folder}/{filename}"):
            return ""

        # 拡張子抜きの名前と拡張子を取り出す
        # name, ext = os.path.splitext(filename)

        # 拡張子だけ取り出す
        ext = os.path.splitext(filename)[1]

        # 上記取得の拡張子の小文字を消し(lower)、.を消す(replace)という処理
        ext = ext.lower().replace(".", "")

        # 拡張子がない場合、not_extとしフォルダを作らせる
        if ext == "":
            ext = "not_ext"

        # カウント処理
        # dict型の変数の中にext(拡張子)が含まれているかを確認
        if ext in self.ext_count:
           self.ext_count[ext] += 1
        else:
            self.ext_count[ext] = 1
        # 確認用
        # print("カウント処理:",self.ext_count) 

        # 新しいパスとディレクトリ名を返却
        return ext
       
    # 拡張子ごとに振り分け、振り分け先フォルダがない場合作成
    def execute_extension(self):
        try:
            # プレビューを実行していない場合、処理しない
            if not self.preview_result:
                messagebox.showwarning("エラー","プレビューを実行してください。")
                return

            # extフラグがTureなら処理実行済みの警告を表示し、処理しない
            if self.ext_flag:
                messagebox.showwarning("警告","処理実行済みフォルダです。")
                return

            # error_resultは空にしておく
            self.error_result = []

            self.ext_flag = False
            for filename, ext in self.preview_result:

                #ext(拡張子名)が""なら処理しない
                if ext != "":
                    # ディレクトリがなければ作成
                    if not os.path.exists(f"{self.folder}/{ext}"):
                        os.mkdir(f"{self.folder}/{ext}")

                    # 新旧のフルパスを作成
                    old_path = os.path.join(self.folder, filename)
                    new_path = os.path.join(self.folder, f"{ext}/{filename}")
                    # ファイル名をnew_pathに変える
                    # os.renameは対象ディレクトリに同じ名前のファイルがある場合エラーになる(windows限定、MacOS及びLinaxでは上書きされる)
                    # そのため既存ファイルがある場合処理せず、error_resultでエラー表示する
                    if not os.path.exists(new_path):
                        os.rename(old_path, new_path)
                        # 強制的に上書きする処理
                        # os.replace(old_path, new_path)
                        self.ext_flag = True
                    else:
                        self.error_result.append((filename, ext))

            # 振り分け先に同じ名前のファイルがあった時のエラーメッセージを生成
            text = ""
            if self.error_result:
                for error_path, ext in self.error_result:
                    text += f"\n{error_path}"
                    
            # 処理実行flag及び上記でエラー/警告用のtextが作られていないかをチェック
            if self.ext_flag and text == "":
                messagebox.showinfo("Successful","対象フォルダ下にあるファイルを拡張子毎のフォルダに格納しました。")
            elif self.ext_flag and text != "":
                messagebox.showwarning("Partial Successful", f"フォルダ内に同一名称のファイルがあるため一部処理が実行できませんでした。{text}")
            elif not self.ext_flag and text != "":
                messagebox.showerror("エラー", f"フォルダ内に同一名称のファイルがあるため処理が実行できませんでした。{text}")
            else:
                messagebox.showerror("エラー","フォルダ下に対象が存在しません")
        
        except Exception as e:
            messagebox.showerror("エラー",e)

    #クリア処理
    def clear_data(self):
        #変数の初期化
        self.folder = None
        self.files = None

        # プレビュー時に初期化されているが、一応こちらでも初期化
        self.preview_result = []
        self.error_result = []
        self.ext_count = {}
        self.ext_flag = False

        # 画面に表示したパスをクリア
        self.dir_path.configure(text="path:")

        #件数ラベルを初期化
        self.target_len_label.configure(text="対象はありません")

        # スクロールラベルバーを初期化
        for child in self.listbox_before_frame.winfo_children():          
            child.destroy()
        for child in self.listbox_after_frame.winfo_children():          
            child.destroy()

       
# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #インスタンス化
    app = ExtensionSortApp()
    #イベント待ちループ開始
    app.mainloop()
