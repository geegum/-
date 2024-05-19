from pyKamipi.pibot import KamibotPi
from pynput.keyboard import Listener, Key

kamibot = KamibotPi('COM9', 57600)
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
    kamibot.go_forward_speed(0, 20)

def left():
    kamibot.go_forward_speed(20, 0)

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

with Listener(on_press=handleKeyPress, on_release=handleKeyRelease) as listener:
    listener.join()
