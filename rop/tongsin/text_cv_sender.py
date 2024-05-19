import cv2
import socket
import pickle
import struct

HOST = '127.0.0.1'  # 서버의 IP 주소
PORT = 8000  # 서버의 포트 번호
WIDTH = 160  # 조절할 화상의 폭
HEIGHT = 120  # 조절할 화상의 높이

# OpenCV를 사용하여 웹캠 영상 캡처 및 크기 조절
def capture_and_resize():
    cap = cv2.VideoCapture(0)  # 웹캠 캡처를 위한 객체 생성
    while True:
        ret, frame = cap.read()  # 웹캠 영상 읽기
        if not ret:
            break

        # 화상 크기 조절
        resized_frame = cv2.resize(frame, (WIDTH, HEIGHT))

        # 조절한 영상 데이터를 직렬화하여 전송하기 위해 바이트로 변환
        data = pickle.dumps(resized_frame)
        message_size = struct.pack("L", len(data))

        # 서버에 데이터 전송
        client_socket.sendall(message_size + data)

    # 웹캠 캡처 종료
    cap.release()

# 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# 웹캠 영상 캡처 및 크기 조절 시작
capture_and_resize()

# 클라이언트 소켓 종료
client_socket.close()
