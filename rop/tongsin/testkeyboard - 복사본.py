
import socket
from _thread import *
import tensorflow.keras
import tensorflow.keras as keras
import numpy as np
import cv2

HOST = '127.0.0.1'
PORT = 8005
data = None
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

store = set()

# 모델 위치
model_filename = 'c:\\Users\\PC\\Downloads\\converted_keras (1)\\keras_model.h5'


# 케라스 모델 가져오기
model = tensorflow.keras.models.load_model(model_filename, compile=False)

# 모델 컴파일
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# 카메라를 제어할 수 있는 객체
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
HOT_KEYS = {
    'up': {Key.up},
    'down': {Key.down},
    'right': {Key.right},
    'left': {Key.left},
}

# 이미지 처리하기
def preprocessing(frame):
    #frame_fliped = cv2.flip(frame, 1)
    # 사이즈 조정 티쳐블 머신에서 사용한 이미지 사이즈로 변경해준다.
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    
    # 이미지 정규화
    # astype : 속성
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1

    # 이미지 차원 재조정 - 예측을 위해 reshape 해줍니다.
    # keras 모델에 공급할 올바른 모양의 배열 생성
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    #print(frame_reshaped)
    return frame_reshaped

# 예측용 함수
def predict(frame):
    prediction = model.predict(frame)
    return prediction

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

    # 종료
    if key == Key.esc:
        client_socket.send('f'.encode())
    if key == Key.space:
        client_socket.send('p'.encode())
        
flag = 1
while True:
    try :
        ret, frame = capture.read(0)
        cv2.imshow("VideoFrame", frame)
        if flag == 1:
            preprocessed = preprocessing(frame)
            prediction = predict(preprocessed)
            if (prediction[0,0] < prediction[0,1]):
                cv2.putText(frame, 'on', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
                flag = 2
            else:
                cv2.putText(frame, 'off', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        if flag == 2:
            with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
                listener.join()
            
    except:
        print("none")
