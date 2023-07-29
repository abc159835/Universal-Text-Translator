chcp 65001
pyinstaller --windowed --name "Application" --add-data "./vue/dist;static/" --add-data "./hooks;./" --icon "./vue/dist/toolbox.ico" --noconfirm main.py
pause