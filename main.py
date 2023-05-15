from module.network import app
from loguru import logger
import webview


window = webview.create_window('Universal Translator',url=app,width=2160,height=1200)

# MainThread blocked
webview.start()