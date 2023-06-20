import cv2
from Util import *
import numpy as np

inputImage = cv2.imread("tim.jpeg")
inputHeight = len(inputImage)
inputWidth = len(inputImage[0])

print("h: %d, w: %d" % (inputHeight, inputWidth))

util = Util(inputImage)
boxes = util.getAllBoxes()

box15 = boxes[15]
boxImage = util.getBoxImage(box15)

width = box15.width
height = box15.height
w = box15.wUpperLeft
h = box15.hUpperLeft

print(box15)

for ww in range(w, w + width):
    inputImage[h, ww] = (255, 255, 0)
    inputImage[h + height, ww] = (255, 255, 0)

for hh in range(h, h + height):
    inputImage[hh, w] = (255, 255, 0)
    inputImage[hh, w + width] = (255, 255, 0)


cv2.imshow('', inputImage)
cv2.waitKey(0)
