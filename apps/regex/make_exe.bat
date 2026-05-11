@echo off
rem pyinstallerでexeファイルを作成するためのバッチファイル
rem 2つ上の階層のプロジェクトルートに移動 %~dp0はバッチファイルのあるディレクトリを指す
cd /d %~dp0\..\..
echo "directory: %cd%"
rem pyinstallerコマンドを実行
pyinstaller apps/regex/main.py --onefile  --noconsole --icon=apps/regex/icon_01.ico --paths . --distpath apps/regex/dist
rem exeファイルが生成された後、再びバッチファイルのあるディレクトリに移動
cd apps\regex
pause
