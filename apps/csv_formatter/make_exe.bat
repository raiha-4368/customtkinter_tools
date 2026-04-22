@echo off
rem pyinstallerでexeファイルを作成するためのバッチファイル
rem 2つ上の階層のプロジェクトルートに移動 %~dp0はバッチファイルのあるディレクトリを指す
cd /d %~dp0\..\..
echo "directory: %cd%"
rem pyinstallerコマンドを実行
pyinstaller apps/csv_formatter/main.py --onefile  --noconsole --icon=apps/csv_formatter/icon_01.ico --paths . --distpath apps/csv_formatter/dist
rem exeファイルが生成された後、再びバッチファイルのあるディレクトリに移動
cd apps\csv_formatter
pause
