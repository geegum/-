import cv2
import numpy as np

# 색상 범위 지정
lower_red = np.array([0, 50, 50])  # 빨강 범위 (H: 0-10)
upper_red = np.array([10, 255, 255])
lower_blue = np.array([110, 50, 50])  # 파랑 범위 (H: 110-130)
upper_blue = np.array([130, 255, 255])
lower_green = np.array([50, 50, 50])  # 초록 범위 (H: 50-70)
upper_green = np.array([70, 255, 255])

def get_color_name(hsv_value):
    # 색상 값에 따라 색상 이름 반환
    hue = hsv_value[0]
    if 0 <= hue <= 10 or 170 <= hue <= 180:
        return 'red'
    elif 110 <= hue <= 130:
        return 'blue'
    elif 50 <= hue <= 70:
        return 'green'
    else:
        return '알 수 없음'

# 웹캠 불러오기
cap = cv2.VideoCapture(0)

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    # 프레임 크기 조정 (선택사항)
    # frame = cv2.resize(frame, (800, 600))
    
    # 프레임을 HSV 색 공간으로 변환
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 색상에 따라 이진 이미지 생성
    red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    green_mask = cv2.inRange(hsv_frame, lower_green, upper_green)
    
    # 컬러 이미지에서 색상 영역 추출
    red_result = cv2.bitwise_and(frame, frame, mask=red_mask)
    blue_result = cv2.bitwise_and(frame, frame, mask=blue_mask)
    green_result = cv2.bitwise_and(frame, frame, mask=green_mask)
    
    # 컨투어 찾기
    contours, _ = cv2.findContours(red_mask + blue_mask + green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            # 컨투어의 중심 좌표 찾기
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # 중심 좌표에 텍스트 표시
                hsv_value = hsv_frame[cy, cx]
                color_name = get_color_name(hsv_value)
                cv2.putText(frame, color_name, (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # 결과 이미지 출력
    cv2.imshow('Webcam', frame)
    
    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 해제
cap.release()
cv2.destroyAllWindows()
