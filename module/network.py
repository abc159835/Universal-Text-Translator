from module.env import WEB_PATH
# import eel
# import threading

def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def get_available_port() -> int:
    import random
    while True:
        port = random.randint(20000, 60000)
        if not is_port_in_use(port):
            break
    return port

"""
This plan has been abandoned because the initialization time of the website is too long
"""
# # Even if the system sleeps, it will not shutdown
# SHUTDOWN_DELAY = 3600*24*30

# PORT = get_available_port()
# URL = f'http://localhost:{PORT}/'

# def eel_start():
#     eel.start(mode=None,port=PORT,shutdown_delay=SHUTDOWN_DELAY)

# # If the website is large, the loading time will be long.
# eel.init(WEB_PATH)


# # Exit as the main thread exits
# eel_thread = threading.Thread(target=eel_start)
# eel_thread.daemon = True
# eel_thread.start()

"""
Short loading time due to no need to read files
"""
from bottle import Bottle,static_file

app = Bottle()

@app.route('/<filename:path>')
def serve_file(filename):
    return static_file(filename, root=WEB_PATH)

@app.route('/')
def index():
    return static_file('index.html', root=WEB_PATH)