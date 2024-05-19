import socket
from _thread import *
from pyKamipi.pibot import KamibotPi
from pynput.keyboard import Listener, Key

HOST = '127.0.0.1'
PORT = 8005
data = None
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
kamibot = KamibotPi('COM12', 57600)


# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def recv_data(client_socket) :
    while True :
        global data
        global kamisig
        data = client_socket.recv(1024)
        kamisig = data.decode()
        print("recive : ",repr(data.decode()))

while True:
    try :
        global kamisig
        
        if kamisig == 'w':
            kamibot.go_forward_speed(20, 20)
        elif kamisig == 'a':
            kamibot.go_forward_speed(0, 20)
        elif kamisig == 's':
            kamibot.go_backward_speed(20, 20)
        elif kamisig == 'd':
            kamibot.go_forward_speed(20, 0)
        elif kamisig == 'f':
            kamibot.turn_led(255, 0, 255)
            
        elif kamisig == 'f':
            kamibot.turn_led(0, 0, 255)

                
        cv2.imshow("VideoFrame", frame)
    except:
        print("none")

client_socket.close()