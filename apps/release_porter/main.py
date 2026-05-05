import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from common import dialogs
from pathlib import Path
import shutil

# 依存関係を洗い出すためのモジュール
# 正常に取れるか不明の為、使用は一旦保留
from modulefinder import ModuleFinder

# TODO プログレスバーの実装を検討




# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class ReleasePorterApp(ctk.CTk):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):

        super().__init__()   
        self.title("Release Porter")
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
        self.path_list = []

        # -------------------------
        # side_frame内の要素
        # -------------------------
        self.dir_select_button = ctk.CTkButton(self.side_frame, text="対象プログラムフォルダを選択",command=self.select_folder)
        self.dir_select_button.pack(pady=(10,10), padx=(10,10))

        self.file_select_button = ctk.CTkButton(self.side_frame, text="対象プログラムファイルを選択",command=self.select_file)
        self.file_select_button.pack(pady=(10,10), padx=(10,10))

        self.save_button = ctk.CTkButton(self.side_frame, text="プレビュー状況で保存する",command=self.folder_porter)
        self.save_button.pack(pady=(10,10), padx=(10,10))

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
        self.content_label = ctk.CTkLabel(self.content_frame,text="対象のプログラムを公開用に1つのフォルダにまとめます")
        self.content_label.pack(pady=(30,10))

        self.release_area = ttk.Treeview(self.content_frame, columns=()) # columnsを空にする
        self.release_area.column("#0", stretch=True) # ツリー列を横いっぱいに広げる
        self.release_area.pack(expand=True,fill="both",pady=(0,20),padx=(20,20))

        # 見出し設定
        self.release_area.heading("#0", text=f"以下のフォルダ/ファイルを1つのフォルダにまとめます")

    #フォルダを選択
    def select_folder(self):
        dirpath = dialogs.select_folder(title="ディレクトリを選択")

        if dirpath:
            path = Path(dirpath)
        
            # 重複チェック
            if dirpath not in self.path_list:
                # listに追加
                self.path_list.append(dirpath)

                self.recursively_search(path)
            else:
                messagebox.showerror("エラー","選択フォルダが重複しています")


    # フォルダ探索
    def recursively_search(self, folder, parent=""):

        # pathの中から最後の要素のみを抽出
        # last_item = folder.name
        # last_item = os.path.basename(dirpath)

        # データの挿入(引数に指定し親ノードの指定する)
        current_node = self.release_area.insert(parent, "end", text=f"{folder.name}", open=True)

        for item in folder.iterdir():
            if item.is_dir():
                self.recursively_search(item, parent=current_node)
            else:
                self.release_area.insert(current_node, "end", text=f"{item.name}")

    #ファイルを選択
    def select_file(self):
        filepath = dialogs.select_file(title="ファイルを選択")

        if filepath:
            # 重複チェック
            if filepath not in self.path_list:

                # listに追加
                self.path_list.append(filepath)

                # データの挿入
                self.release_area.insert("", "end", text=f"{Path(filepath).name}")
            else:
                messagebox.showerror("エラー","選択ファイルが重複しています")

    # 保存処理
    def folder_porter(self):

        # 移動除外リストの作成(未実装)
        ignore_list = []
        if self.path_list:

            save_path = dialogs.select_folder(title="保存先フォルダを選択してください")
            if save_path:
                for item in self.path_list:
                    if Path(item).is_dir():
                        # 保存先パスに元のフォルダ名をくっつける
                        dest = Path(save_path) / Path(item).name

                        # dirs_exist_ok=Trueで同一ファイルがあってもエラーにしない
                        shutil.copytree(item,
                                        dest,
                                        ignore=shutil.ignore_petterns(ignore_list),
                                        dirs_exist_ok=True)
                    else:
                        # デフォルトで上書きは許容される
                        shutil.copy(item, save_path)
            
                messagebox.showinfo("フォルダに保存しました", f"{save_path}\nに保存しました")
        else:
            messagebox.showerror("エラー", "フォルダ/ファイルが選択されていません。")



    # クリア処理
    def clear(self):
        # 既存データをすべて削除
        for item in self.release_area.get_children():
            self.release_area.delete(item)

        # path_listを空にする
        self.path_list = []



    # モードチェンジ
    def change_mode(self, new_appearance_mode):
        print(new_appearance_mode)
        ctk.set_appearance_mode(new_appearance_mode)

# -------------------------
# 起動処理
# -------------------------
if __name__ == "__main__":
    #インスタンス化
    app = ReleasePorterApp()
    #イベント待ちループ開始
    app.mainloop()

