import os
import sys

def get_base_path():
  """ exe化対応のベースパス取得 """
  if getattr(sys, 'frozen', False):
    return sys._MEIPASS # PyInstaller用
  return os.path.abspath(".")

def resource_path(relative_path: str) -> str:
  """ リソースの絶対パス取得 """
  base_path = get_base_path()
  return os.path.join(base_path, relative_path)