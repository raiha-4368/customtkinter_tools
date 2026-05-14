import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from common import dialogs
from pathlib import Path
import shutil
import os
import sys

import configparser

# 依存関係を洗い出すためのモジュール
# 正常に取れるか不明の為、使用は一旦保留
from modulefinder import ModuleFinder

# TODO プログレスバーの実装を検討




# 外観モードの設定（"System", "Dark", "Light"）
# テーマカラーの設定（"blue", "green", "dark-blue"）
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# exe化時にconfig.iniの位置が問題
# =====================================
# 実行ディレクトリを取得
# =====================================
def get_base_path():
    if getattr(sys,'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))



class ReleasePorterApp(ctk.CTk):

    # -------------------------
    # init(引数の最初はself固定となる)
    # -------------------------
    def __init__(self):

        super().__init__()   
        self.title("Release Porter")
        self.geometry("1200x800")


        # 実行しているpyファイルがあるディレクトリを取得
        # pyファイルと同階層にあるconfig.iniのpathを取得しに行く
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # exe用に直下にする
        # config_path = 'config.ini'
        # py用にツールディレクトリに探しに行く
        config_path = os.path.join(base_dir,'config.ini')
        print(base_dir)
        print(config_path)

        # configファイルの読み込み
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding='utf-8')

        # -------------------------
        # フレーム生成
        # -------------------------
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

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
        # content_frame内の要素
        # -------------------------
        self.content_label = ctk.CTkLabel(self.content_frame,text="対象のプログラムを公開用に1つのフォルダにまとめます")
        self.content_label.pack(pady=(30,10))
        # release_area
        self.release_area = ctk.CTkScrollableFrame(self.content_frame, label_text="選択フォルダ内のリスト")
        self.release_area.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        self.show_release_list()

    # configからpathを受け取り、画面上にリリース対象を表示する
    def show_release_list(self):
        release_list_path = self.config["release_target"]["path"]

        # 取得したpathからリストを作成
        path = Path(release_list_path)

        dir_list = [f.name for f in path.iterdir() if f.is_dir()]

        # リスト用のボタン削除
        for child in self.release_area.winfo_children():          
            child.destroy()

        # スクロールラベルバーにボタンを追加
        for d in dir_list:
            btn = ctk.CTkButton(self.release_area, text=d,
                                anchor="w",
                                command=lambda dir=d: self.folder_porter(dir))
            btn.pack(fill="x")

    # 保存処理
    def folder_porter(self, target_name):
        try:
            # 移動除外リストの作成(未実装)
            ignore_list = []
            if not target_name:
                messagebox.showerror("エラー", "対象が指定されていません。")
                return

            # 1.保存先ベースフォルダ選択
            save_path = dialogs.select_folder(title="保存先フォルダを選択してください")
            if not save_path:
                return
            
            # 保存先にアプリ名フォルダを作成
            save_base = Path(save_path) / target_name

            # 2.リストの取得と置換
            raw_value = self.config.get('release_target','release_list')
            release_list = [line.strip().format(target_src=target_name)
                             for line in raw_value.splitlines() if line.strip()]
            
            src_str =  ""
            dest_sub_str = ""
            for item in release_list:
                # 「 > 」で分割して、元パスと先パスを取得
                if ">" in item:
                    src_str, dest_sub_str = item.split(">")
                else:
                # 今まで通り、構造を維持する場合
                    src_str, dest_sub_str = item, item
                src_path = Path(src_str.strip())

                if not src_path.exists():
                        print(src_path)
                        continue

                # 3.コピー先の計算
                # save_ base (選択先/アプリ名) + 元の相対パス構造を維持してコピー    
                dest_path = save_base / dest_sub_str.strip()
                
                # 親ディレクトリを作成(ないとエラーになるため)
                dest_path.parent.mkdir(parents=True, exist_ok=True)

                if src_path.is_dir():
                    # フォルダのコピー
                    shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                    print(f"Directory Copied: {src_path}")
                else:
                    # ファイルのコピー
                    shutil.copy2(src_path, dest_path) # copy2 は作成日時などの属性も維持します
                    print(f"File Copied: {src_path}")

            messagebox.showinfo("完了", f"リリース対象を以下に抽出しました:\n{save_base}")

        except Exception as e:
            messagebox.showerror("エラー", f"保存に失敗しました\n{e}")
                


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

