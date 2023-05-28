from module.network import app
from module.env import env
from loguru import logger
import module.OShelper
import webview


"""文件夹选择"""
def open_folder():
    result = window.create_file_dialog(dialog_type=webview.FOLDER_DIALOG)
    if result is not None:
        return result[0]
    else:
        return None

if env():
    window = webview.create_window('Universal Translator',url='http://localhost:5173/',width=2160,height=1200)
else:
    window = webview.create_window('Universal Translator',url=app,width=2160,height=1200)

window.expose(module.OShelper.get_folder_all_file,open_folder,module.OShelper.get_file_content)

# MainThread blocked
webview.start(debug=True)