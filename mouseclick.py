# coding=utf-8

# Author: $￥
# @Time: 2020/3/27 16:56
# for auto fishing in minecraft

import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key

mouse = Controller()
start = False


def _click():

    while True:
        if start:
            mouse.press(Button.right)
            time.sleep(0.1)
            # 鼠标右键抬起
            mouse.release(Button.right)
            time.sleep(0.4)


def keybaord_on_release(key):
    global start
    if format(key) == 'Key.f9':
        print("start")

        start = True

    if format(key) == 'Key.f10':
        print("close")
        start = False


def start_listen():
    with Listener(on_press=None, on_release=keybaord_on_release) as listener:
        listener.join()


if __name__ == '__main__':

    t = threading.Thread(target=_click)
    t.setDaemon(True)
    t.start()

    start_listen()







