from pyKamipi.pibot import KamibotPi
from pynput.keyboard import Listener, Key
import socket
from _thread import *

HOST = '127.0.0.1'
PORT = 8005
data = None
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

kamibot = KamibotPi('COM9', 57600)
store = set()

HOT_KEYS = {
    'up': {Key.up},
    'down': {Key.down},
    'right': {Key.right},
    'left': {Key.left}
}

def up():
    client_socket.send('w'.encode())

def down():
    client_socket.send('s'.encode())

def right():
    client_socket.send('d'.encode())
def left():
    client_socket.send('a'.encode())

def handleKeyPress(key):
    store.add(key)
    for action, trigger in HOT_KEYS.items():
        CHECK = all(triggerKey in store for triggerKey in trigger)
        if CHECK:
            try:
                func = eval(action)
                if callable(func):
                    func()
            except NameError as err:
                print(err)

def handleKeyRelease(key):
    if key in store:
        store.remove(key)
        kamibot.go_forward_speed(0, 0)

    # 종료
    if key == Key.esc:
        kamibot.go_forward_speed(0, 0)
        kamibot.close()
        return False

with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
    listener.join()
