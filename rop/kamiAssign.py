import tensorflow.keras
import numpy as np
import cv2
from pyKamipi.pibot import KamibotPi
from pynput.keyboard import Listener, Key
import time

kamibot = KamibotPi('COM9', 57600)
store = set()

melody = [48, 57, 55, 53, 48, 48, 57, 55, 53, 50, 52, 50, 59, 57, 55, 52, 48, 48, 59, 55, 57, 53, 48, 57, 55, 53, 57, 67,57, 48, 55, 53, 50, 52, 59, 57, 55, 48, 48, 48, 48, 50, 48, 59, 55, 53, 57, 57, 57]

HOT_KEYS = {
    'up': {Key.up},
    'down': {Key.down},
    'right': {Key.right},
    'left': {Key.left},
    'space': {Key.space}  # 스페이스바 키 추가
}

def up():
    kamibot.go_forward_speed(10, 10)

def down():
    kamibot.go_backward_speed(10, 10)

def right():
    kamibot.go_forward_speed(10, 0)

def left():
    kamibot.go_forward_speed(0, 10)

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

    # 스페이스바
    if key == Key.space:
        kamibot.draw_star(10)
        kamibot.delay(1) 

# 모델 위치
model_filename = r'C:\Users\PC\Desktop\converted_keras\keras_model.h5'

# 케라스 모델 가져오기
model = tensorflow.keras.models.load_model(model_filename)

# 카메라를 제어할 수 있는 객체
capture = cv2.VideoCapture(0)

# 카메라 길이 너비 조절
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# 이미지 처리하기
def preprocessing(frame):
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    return frame_reshaped

# 예측용 함수
def predict(frame):
    prediction = model.predict(frame)
    return prediction

while True:
    ret, frame = capture.read()

    if cv2.waitKey(100) > 0:
        break

    preprocessed = preprocessing(frame)
    prediction = predict(preprocessed)

    if prediction[0, 0] < prediction[0, 1]:
        print('mask off')
        cv2.putText(frame, 'mask off', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        
        kamibot.go_dir_speed("b", 100, "f", 100)
        kamibot.delay(5)
        kamibot.stop()
        for note in melody:
            kamibot.melody(note, 0.3)
        
        with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
            listener.join()
    else:
        cv2.putText(frame, 'mask on', (0, 25), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        print('mask on')

    cv2.imshow("VideoFrame", frame)

kamibot.close()