from module.network import app
import module.OShelper
import webview

    
def start(env = True):
    if env:
        window = webview.create_window('Universal Translator',url='http://localhost:5173/',width=2160,height=1200)
    else:
        window = webview.create_window('Universal Translator',url=app,width=2160,height=1200)
        
    def open_folder():
        """文件夹选择"""
        result = window.create_file_dialog(dialog_type=webview.FOLDER_DIALOG)
        if result is not None:
            return result[0]
        else:
            return None

    window.expose(module.OShelper.recursive_read_folder,open_folder,module.OShelper.get_file_content,module.OShelper.global_config,module.OShelper.set_global_config)

    # MainThread blocked
    webview.start(debug=True)


module.OShelper.init()
start()