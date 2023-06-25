import cv2
from Util import Util
import numpy as np
import random

inputImage = cv2.imread("tim.jpeg")
inputHeight = len(inputImage)
inputWidth = len(inputImage[0])

print("h: %d, w: %d" % (inputHeight, inputWidth))

def drawBox(box, color):
    width = box.width
    height = box.height
    w = box.wUpperLeft
    h = box.hUpperLeft
    
    for ww in range(w, w + width - 1):
        inputImage[h, ww] = color
        inputImage[h + height - 1, ww] = color
    
    for hh in range(h, h + height - 1):
        inputImage[hh, w] = color
        inputImage[hh, w + width - 1] = color
        
util = Util(inputImage)
boxes = util.getAllBoxes()

    
indicesContainTim = [
    (1, 8), (1, 9),
    (2, 7), (2, 8), (2, 9),
    (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9),
    (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9),
    (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
    (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9)
    ]

boxesContainTim = []
for index in indicesContainTim:
    wIndex, hIndex = index
    box = boxes[wIndex][hIndex]
    boxesContainTim.append(box)
    #drawBox(box, (0, 0, 255))

fineBoxesWithoutTim = util.getFineBoxesWithoutTim(boxesContainTim)
#drawBox(fineBoxesWithoutTim[1], (255, 0, 0))

while len(boxesContainTim) > 0:
    print(len(boxesContainTim))
    nextIterationBoxes = []
    for boxTim in boxesContainTim:
        neighbourBoxes = util.neighbourBox(boxTim)
        neighbourAndNotTimBoxes = []
        
        for neighbourBox in neighbourBoxes:
            if not neighbourBox.box in boxesContainTim:
                neighbourAndNotTimBoxes.append(neighbourBox)
                #drawBox(neighbourBox.box, (255, 0, 0))
        
        if len(neighbourAndNotTimBoxes) <= 1 :
            nextIterationBoxes.append(boxTim)
        else:
            width = boxTim.width
            height = boxTim.height
            w0 = boxTim.wUpperLeft
            h0 = boxTim.hUpperLeft
            
            replaceBox = util.findBestBox(neighbourAndNotTimBoxes, fineBoxesWithoutTim)
            wReplace = replaceBox.wUpperLeft
            hReplace = replaceBox.hUpperLeft
            
            wOffset = w0 - wReplace
            hOffset = h0 - hReplace
            
            for w in range(w0, w0 + width):
                for h in range(h0, h0 + height):
                    inputImage[h, w] = inputImage[h - hOffset, w - wOffset]
             
            # drawBox(replaceBox, (255, 0, 0))   
            # drawBox(boxTim, (0, 255, 0))   
            # break
        
    boxesContainTim = nextIterationBoxes
    #break



cv2.imshow('', inputImage)
cv2.waitKey(0)









