chcp 65001
pyinstaller "main.py" --name "Application" --add-data "./vue/dist;static/" --icon "./vue/dist/toolbox.ico" --noconfirm
pause