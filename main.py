import threading
import numpy as np
import pyautogui
import cv2
import time
from find import findMob, findPlayer
from move import KeyPress, TwoKeyPress
from util import screenshot, findClosest, randomTime
from globalhotkeys import GlobalHotKeys

LEFT = 0xCB
RIGHT = 0xCD
CTRL = 0x1D
ALT = 0x38
speed = 90

running = False
playerTemplate = cv2.imread("player.png", cv2.IMREAD_GRAYSCALE)
mobTemplate = cv2.imread("mob.png", cv2.IMREAD_GRAYSCALE)

class Info():
    def getInfo(self):
        screen = screenshot()
        self.playerPos = findPlayer(screen, playerTemplate)
        self.playerX, self.playerY = self.playerPos
        mobPos = findMob(screen, mobTemplate)
        self.closestMob = findClosest(self.playerPos, mobPos)
        self.dist = (self.closestMob[0] - self.playerX)
        self.direction = RIGHT if self.dist > 0 else LEFT

def bot():
    print("Thread start")
    info = Info()
    while 1:
        if not running:
            continue
        time.sleep(0.01)
        try:
            info.getInfo()
            KeyPress(info.direction, abs(info.dist) / speed)
            info.getInfo()
            if info.playerY > info.closestMob[1] + 50:
                KeyPress(RIGHT, randomTime(400, 500, 3))
                TwoKeyPress(ALT, RIGHT)
                continue
            if abs(info.dist) < 150:
                KeyPress(info.direction, abs(info.dist) / speed)
                KeyPress(CTRL, randomTime(200, 1500, 3))
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(e)

thread = threading.Thread(target=bot, daemon=True)
thread.start()

@GlobalHotKeys.register(GlobalHotKeys.VK_F2)
def toggle():
    global running
    running = not running
    print("running:", running)

GlobalHotKeys.register(GlobalHotKeys.VK_C, GlobalHotKeys.MOD_CTRL, False)
GlobalHotKeys.listen()