@echo off
rem pyinstallerでexeファイルを作成するためのバッチファイル
rem 2つ上の階層のプロジェクトルートに移動 %~dp0はバッチファイルのあるディレクトリを指す
cd /d %~dp0\..\..
echo "directory: %cd%"
rem pyinstallerコマンドを実行
pyinstaller apps/text_extract/main.py --onefile  --noconsole --icon=apps/text_extract/icon_01.ico --paths . --distpath apps/text_extract/dist
rem exeファイルが生成された後、再びバッチファイルのあるディレクトリに移動
cd /d %~dp0\apps\text_extract
pause
