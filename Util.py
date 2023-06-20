import numpy as np
import math

class Box:
    def  __init__(self, wUpperLeft, hUpperLeft, width, height):
        self.wUpperLeft = wUpperLeft
        self.hUpperLeft = hUpperLeft
        self.width = width
        self.height = height
        
    def __str__(self):
        return "w0: %d, h0: %d" % (self.wUpperLeft, self.hUpperLeft)

class Util:
    def __init__(self, inputImage):
        self.height = len(inputImage)
        self.width = len(inputImage[0])
        self.inputImage = inputImage

    def getBoxImage(self, box):
        width = box.width
        height = box.height
        w0 = box.wUpperLeft
        h0 = box.hUpperLeft
        
        boxImage = np.zeros((width, height, 3), dtype = np.uint8)
        
        for w in range(width):
            for h in range(height):
                boxImage[h, w] = self.inputImage[h + h0, w + w0]
        
        return boxImage
    
    def getAllBoxes(self):
        wOrigin = 0
        hOrigin = 0
        wStride = int(self.width / 10)
        hStride = int(self.height / 10)
        
        traversedBoxes = []
        
        for wTemp in range(0, self.width - wStride, wStride):
            for hTemp in range(0, self.height - hStride, hStride):
                box = Box(wTemp, hTemp, wStride, hStride)
                traversedBoxes.append(box)
        
        return traversedBoxes