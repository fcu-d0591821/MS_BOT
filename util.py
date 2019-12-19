import random
import cv2
import pyautogui
import win32gui
import numpy as np

def screenshot(lx, ly, rx, ry):
    return cv2.cvtColor(np.array(pyautogui.screenshot(region=(lx, ly, rx - lx, ry - ly))), cv2.COLOR_RGB2BGR)

def findClosest(node, nodes):
    px, py = node
    dist = [(px - x) ** 2 + (py - y) ** 2 for x, y in nodes]
    return nodes[dist.index(min(dist))]

def randomTime(min, max, decimal):
    return random.randrange(min, max) / (10 ** decimal)

def getGamePos():
    result = []

    def callback(hwnd, extra):
        if win32gui.GetWindowText(hwnd) == "MapleStory":
            result.append(win32gui.GetWindowRect(hwnd))
            
    win32gui.EnumWindows(callback, None)

    return result[0]