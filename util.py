import random
import cv2
import pyautogui
import numpy as np

def screenshot():
    return cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2GRAY)

def findClosest(node, nodes):
    px, py = node
    dist = [(px - x) ** 2 + (py - y) ** 2 for x, y in nodes]
    return nodes[dist.index(min(dist))]

def randomTime(min, max, decimal):
    return random.randrange(min, max) / (10 ** decimal)