import cv2
import numpy as np

def findMob(image, target):
    res = cv2.matchTemplate(image, target, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.9)
    return list(zip(*loc[::-1]))

def findPlayer(image, target):
    targetFlip = cv2.flip(target, 1)
    res = cv2.matchTemplate(image, target, cv2.TM_CCOEFF_NORMED)
    resFlip = cv2.matchTemplate(image, targetFlip, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    _, max_valFlip, _, max_locFlip = cv2.minMaxLoc(resFlip)
    if max_val <= max_valFlip < 0.8:
        return None
    else:
        return max_loc if max_val > max_valFlip else max_locFlip