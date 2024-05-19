import random
from pyKamipi.pibot import *
kamibot= KamibotPi('COM9', 57600)
kamibot.go_dir_speed("f", 100, "f", 100)
kamibot.delay(1)
kamibot.go_dir_speed("b", 100, "f", 100)
kamibot.delay(1)
kamibot.go_dir_speed("f", 100, "f", 100)
kamibot.delay(1)
kamibot.go_dir_speed("f", 100, "b", 100)
kamibot.delay(1)

for i in range(5):
    kamibot.go_dir_speed("f", 100, "f", 100)
    kamibot.delay(1)
    kamibot.go_dir_speed("b", 100, "f", 100)
    kamibot.delay(1)
    kamibot.go_dir_speed("f", 100, "f", 100)
    kamibot.delay(1)
    kamibot.go_dir_speed("f", 100, "b", 100)
    kamibot.delay(1)
kamibot.stop()
kamibot.close()
