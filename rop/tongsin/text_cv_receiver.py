import cv2
import socket
import pickle
import struct

HOST = '127.0.0.1'  # 서버의 IP 주소
PORT = 8000  # 서버의 포트 번호
DISPLAY_WIDTH = 640  # 화면 출력 폭
DISPLAY_HEIGHT = 240  # 화면 출력 높이

# 서버로부터 메시지를 받는 메소드
def recv_data(client_socket):
    while True:
        try:
            data = b""
            payload_size = struct.calcsize("L")
            while len(data) < payload_size:
                data += client_socket.recv(4096)

            if not data:
                print("서버와의 연결이 끊어졌습니다.")
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += client_socket.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            # 받은 데이터를 웹캠 영상으로 디코딩
            frame = pickle.loads(frame_data)

            # 화면 크기 조절
            resized_frame = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

            # 조절한 화면 출력
            cv2.imshow("Received", resized_frame)
            cv2.waitKey(1)
        except:
            print(e)
            break

# 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 서버로부터 메시지를 받는 스레드 시작
recv_data(client_socket)

# 클라이언트 소켓 종료
client_socket.close()
