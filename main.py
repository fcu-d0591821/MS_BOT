import threading
import cv2
import time
from find import findMob, findPlayer
from move import KeyPress, TwoKeyPress
from util import screenshot, findClosest, randomTime, getGamePos
from globalhotkeys import GlobalHotKeys

LEFT = 0xCB
RIGHT = 0xCD
CTRL = 0x1D
ALT = 0x38
speed = 155

running = False
playerTemplate = cv2.imread("player.png", cv2.IMREAD_GRAYSCALE)
mobTemplate = cv2.imread("mob.png", cv2.IMREAD_GRAYSCALE)
lx = ly = rx = ry = 0

class Info():
    def getInfo(self):
        screen = screenshot(lx, ly, rx, ry)
        screenGray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        self.playerPos = findPlayer(screenGray, playerTemplate)
        self.playerX, self.playerY = self.playerPos
        mobPos = findMob(screenGray, mobTemplate)
        self.closestMob = findClosest(self.playerPos, mobPos)
        self.dist = (self.closestMob[0] - self.playerX)
        self.direction = RIGHT if self.dist > 0 else LEFT
        cv2.rectangle(screen, (self.playerX - 30, self.playerY - 20), (self.playerX + 30, self.playerY + 50), (0, 0, 255), 5)
        cv2.rectangle(screen, (self.closestMob[0] - 10, self.closestMob[1] + 30), (self.closestMob[0] + 30, self.closestMob[1] + 65), (255, 0, 0), 5)
        cv2.imshow("Game", cv2.resize(screen, (640, 360)))
        cv2.waitKey(1)

def bot():
    print("Thread start")
    info = Info()
    while 1:
        if not running:
            continue
        try:
            info.getInfo()
            KeyPress(info.direction, abs(info.dist) / speed)
            info.getInfo()
            print("Player:", info.playerPos)
            print("Mob:", info.closestMob)
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
            pass
            #print(e)

thread = threading.Thread(target=bot, daemon=True)
thread.start()

@GlobalHotKeys.register(GlobalHotKeys.VK_F2)
def toggle():
    global running
    global lx
    global ly
    global rx
    global ry

    if running:
        cv2.destroyAllWindows()
    else:
        lx, ly, rx, ry = getGamePos()

    running = not running
    print("Running:", running)

GlobalHotKeys.register(GlobalHotKeys.VK_C, GlobalHotKeys.MOD_CTRL, False)
GlobalHotKeys.listen()