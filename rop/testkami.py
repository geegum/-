import random
from pyKamipi.pibot import *
import time
from math import sin

# 카미봇 연결
kamibot = KamibotPi('COM9', 57600)

t_period = 330
tmp_time = 0
delt_time  = 0
dt = 0.01

# 솔솔 라라 솔솔 미 // 솔솔 미미 레
melody = [52,50,52,53,52,48,52,47,50,47,48,50,52,52,50,52,53,52,48,50,47,50,47,48,45,47,48,47,40,45,47,48,48,53,53,52,50,48,47,48,48,50]

cnt_note = 0
for note in melody:
    # 소리 재생q
    cnt_note = cnt_note + 1;
    if (cnt_note%2 == 0):
        
        kamibot.melody(note,0.3)
    else:
        kamibot.melody(note,0.3)

# 카미봇 연결 해제
kamibot.close()
