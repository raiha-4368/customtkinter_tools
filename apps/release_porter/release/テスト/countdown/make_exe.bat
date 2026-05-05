@echo off
rem pyinstallerでexeファイルを作成するためのバッチファイル
rem 2つ上の階層のプロジェクトルートに移動 %~dp0はバッチファイルのあるディレクトリを指す
cd /d %~dp0\..\..
echo "directory: %cd%"
rem pyinstallerコマンドを実行
pyinstaller apps/countdown/main.py --onefile  --noconsole --icon=apps/countdown/icon_01.ico --paths . --distpath apps/countdown/dist
rem exeファイルが生成された後、再びバッチファイルのあるディレクトリに移動
cd /d %~dp0\apps\countdown
pause
