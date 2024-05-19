import socket
from _thread import *
from pyKamipi.pibot import KamibotPi
from pynput.keyboard import Listener, Key

HOST = '192.168.209.231'
PORT = 8005
data = None
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
kamibot = KamibotPi('COM5', 57600)
store = set()

melody = [64, 60, 64, 60]
# 서버로부터 메세지를 받는 메소드
# 스레드로 구동 시켜, 메세지를 보내는 코드와 별개로 작동하도록 처리
def recv_data(client_socket) :
    while True :
        global data
        global sig
        data = client_socket.recv(1024)
        sig = data.decode()

        print("recive : ",repr(data.decode()))
start_new_thread(recv_data, (client_socket,))
print ('>> Connect Server')

while True:
    try :
        global sig
        print(data.decode())
        if sig == 'w':
            kamibot.go_forward_speed(20, 20)

        if sig == 'a':
            kamibot.go_forward_speed(0, 20)
        if sig == 's':
            kamibot.go_backward_speed(10, 10)
        if sig == 'd':
            kamibot.go_forward_speed(20, 0)
        if sig == 'p':
            kamibot.turn_led(0, 0, 255)
            kamibot.delay(1)
        if sig == 'f':
            kamibot.turn_led(255, 0, 0)
            kamibot.delay(1)
        if sig == 'z':
            kamibot.go_forward_speed(0, 0)
            kamibot.delay(1)
        if sig == 'q':
            kamibot.turn_led(0, 255, 255)
            kamibot.delay(0.5)
            kamibot.turn_led(255, 0, 0)
            kamibot.delay(0.5)
            kamibot.move_time("f", 10, "b", 10)
            for note in melody:
                kamibot.melody(note, 0.3)
        if sig == 'i':
            kamibot.turn_led(0, 255, 0)
            kamibot.delay(1)


        
        client_socket.send(message.encode())
    except:
        pass

client_socket.close()