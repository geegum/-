from pyKamipi.pibot import KamibotPi
from pynput.keyboard import Listener, Key
import socket
from _thread import *

HOST = '127.0.0.1'
PORT = 8005
data = None
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
kamibot = KamibotPi('COM12', 57600)
store = set()

HOT_KEYS = {
    'up': {Key.up},
    'down': {Key.down},
    'right': {Key.right},
    'left': {Key.left}
}

def up():
    kamibot.go_forward_speed(20, 20)

def down():
    kamibot.go_backward_speed(20, 20)

def right():
    kamibot.go_forward_speed(20, 0)

def left():
    kamibot.go_forward_speed(0, 20)

def handleKeyPress(key):
    store.add(key)
    for action, trigger in HOT_KEYS.items():
        if all(triggerKey in store for triggerKey in trigger):
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

    if key == Key.esc:
        kamibot.go_forward_speed(0, 0)
        kamibot.close()
        return False

def recv_data(client_socket):
    while True:
        global data
        data = client_socket.recv(1024)
        print("수신: ", repr(data.decode()))

start_new_thread(recv_data, (client_socket,))
print(">> 서버에 연결됨")

with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
    listener.join()
client_socket.close()
