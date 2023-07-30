import numpy as np
import math
from enum import Enum

class Box:
    def  __init__(self, wUpperLeft, hUpperLeft, width, height):
        self.wUpperLeft = wUpperLeft
        self.hUpperLeft = hUpperLeft
        self.width = width
        self.height = height
    
    def __eq__(self, other):
        if isinstance(other, Box):
            return self.wUpperLeft == other.wUpperLeft and self.hUpperLeft == other.hUpperLeft
        return False    
    
    def __str__(self):
        return "w0: %d, h0: %d" % (self.wUpperLeft, self.hUpperLeft)

class NeighbourType(Enum):
    LEFT = 1
    RIGHT = 2
    ABOVE = 3
    UNDER = 4    

class NeighbourBox:
    def  __init__(self, box, neighbourType):
        self.box = box
        self.neighbourType = neighbourType
    
    def __eq__(self, other):
        if isinstance(other, NeighbourBox):
            return self.box == other.box and self.neighbourType == other.neighbourType
        return False    
    
    def __str__(self):
        return "w0: %d, h0: %d, type: %d" % (self.box.wUpperLeft, self.box.hUpperLeft, self.neighbourType.value)   

class Util:
    def __init__(self, inputImage):
        self.height = len(inputImage)
        self.width = len(inputImage[0])
        self.inputImage = inputImage
        self.wStride = int(self.width / 10)
        self.hStride = int(self.height / 10)

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
        traversedBoxes = []
        
        for wTemp in range(0, self.width - self.wStride + 1, self.wStride):
            tempColumn = []
            for hTemp in range(0, self.height - self.hStride + 1, self.hStride):
                box = Box(wTemp, hTemp, self.wStride, self.hStride)
                tempColumn.append(box)
            traversedBoxes.append(tempColumn)
            
        return traversedBoxes
    
    def neighbourBox(self, box):
        w0 = box.wUpperLeft
        h0 = box.hUpperLeft
        
        neighbourBoxes = []
        # left
        if w0 - self.wStride >= 0:
            leftBox = Box(w0 - self.wStride, h0, self.wStride, self.hStride)
            neighbourBoxes.append(NeighbourBox(leftBox, NeighbourType.LEFT))
            
        # right
        if w0 + 2 * self.wStride < self.width:
            rightBox = Box(w0 + self.wStride, h0, self.wStride, self.hStride)
            neighbourBoxes.append(NeighbourBox(rightBox, NeighbourType.RIGHT))
            
        # above
        if h0 - self.hStride >= 0:
            aboveBox = Box(w0, h0 - self.hStride, self.wStride, self.hStride)
            neighbourBoxes.append(NeighbourBox(aboveBox, NeighbourType.ABOVE))
            
        # under
        if h0 + 2 * self.hStride < self.height:
            underBox = Box(w0, h0 + self.hStride, self.wStride, self.hStride)
            neighbourBoxes.append(NeighbourBox(underBox, NeighbourType.UNDER))
            
        return neighbourBoxes
    
    def imageDifference(self, box1, box2):
        image1 = self.getBoxImage(box1)
        image2 = self.getBoxImage(box2)
        width = box1.width
        height = box1.height
        
        averageDiff = 0
        
        for w in range(width):
            for h in range(height):
                color1 = image1[h, w]
                color2 = image2[h, w]
                sum1 = np.int16(color1[0]) + np.int16(color1[1]) + np.int16(color1[2])
                sum2 = np.int16(color2[0]) + np.int16(color2[1]) + np.int16(color2[2])
                averageDiff += abs(sum1 - sum2) / width / height
        
        return averageDiff
 
    def imageDifference2(self, box1, neighbourBox, neighbourType):
        image1 = self.getBoxImage(box1)
        neighbourImage = self.getBoxImage(neighbourBox)
        width = box1.width
        height = box1.height
        
        averageDiff = 0.0
        offest = 10
        
        if neighbourType == NeighbourType.LEFT:
            #print("----")
            # compare neighbour right column with box1 left column
            for w in range(offest):
                #diff = abs(image1[:, w] - neighbourImage[:, width - 1 - w])
                thing1 = np.array(image1[:, 0], dtype=np.int16)
                thing2 = np.array(neighbourImage[:, width - 1 - w], dtype=np.int16)
                diff = np.array(abs(thing1 - thing2), dtype=np.int16)
                diff2 = np.array(diff, dtype=np.int32)
                diff2 = np.square(diff2)
                averageDiff += np.average(diff2, (0, 1))
                #print("1 -- w: %d, average: %d" % (w, averageDiff))
            
        elif neighbourType == NeighbourType.RIGHT:
            for w in range(offest):
                thing1 = np.array(image1[:, width - 1], dtype=np.int16)
                thing2 = np.array(neighbourImage[:, w], dtype=np.int16)
                diff = np.array(abs(thing1 - thing2), dtype=np.int16)
                diff2 = np.array(diff, dtype=np.int32)
                diff2 = np.square(diff2)
                averageDiff += np.average(diff2, (0, 1))
                
        elif neighbourType == NeighbourType.ABOVE:
            # compare neighbour bottom row with box1 top row
            for h in range(offest):
                thing1 = np.array(image1[0, :], dtype=np.int16)
                thing2 = np.array(neighbourImage[height - 1 - h, :], dtype=np.int16)
                diff = np.array(abs(thing1 - thing2), dtype=np.int16)
                diff2 = np.array(diff, dtype=np.int32)
                diff2 = np.square(diff2)
                averageDiff += np.average(diff2, (0, 1))
                
        elif neighbourType == NeighbourType.UNDER:
            for h in range(offest):
                thing1 = np.array(image1[height - 1, :], dtype=np.int16)
                thing2 = np.array(neighbourImage[h, :], dtype=np.int16)
                diff = np.array(abs(thing1 - thing2), dtype=np.int16)
                diff2 = np.array(diff, dtype=np.int32)
                diff2 = np.square(diff2)
                averageDiff += np.average(diff2, (0, 1))
                  
        return averageDiff
    
    def pointInBox(self, point, box):
        width = box.width
        height = box.height
        w0 = box.wUpperLeft
        h0 = box.hUpperLeft
        
        wPoint, hPoint = point
        
        if wPoint < w0 or wPoint > w0 + width:
            return False
        
        if hPoint < h0 or hPoint > h0 + height:
            return False
   
        return True

    def boxesIntersect(self, box1, box2):
        width = box1.width
        height = box1.height
        w0 = box1.wUpperLeft
        h0 = box1.hUpperLeft
        
        #box1 left touches box2 right
        if w0 == box2.wUpperLeft + width:
            return False
 
         #box1 right touches box2 left
        if w0 + width == box2.wUpperLeft:
            return False  
        
        #check cross intersect
        pointUpperLeft = (w0, h0)
        if self.pointInBox(pointUpperLeft, box2):
            return True

        pointUpperRight = (w0 + width, h0)
        if self.pointInBox(pointUpperRight, box2):
            return True
        
        pointLowerLeft = (w0, h0 + height)
        if self.pointInBox(pointLowerLeft, box2):
            return True
        
        pointLowerRight = (w0 + width, h0 + height)
        if self.pointInBox(pointLowerRight, box2):
            return True
        
 
        return False
    
    def getFineBoxesWithoutTim(self, boxesContainTim):
        wFineStride = 8 # int(self.wStride / 6)
        hFineStride = 8 # int(self.hStride / 6)
        traversedBoxes = []
        #traversedImages = []
        
        for wTemp in range(0, self.width - self.wStride + 1, wFineStride):
            for hTemp in range(0, self.height - self.hStride + 1, hFineStride):
                box = Box(wTemp, hTemp, self.wStride, self.hStride)
                #boxImage = self.getBoxImage(box)
                
                intersectWithTim = False
                for boxContainTim in boxesContainTim:
                    if self.boxesIntersect(box, boxContainTim):
                        intersectWithTim = True
                        break
                
                if intersectWithTim:
                    continue
    
               
                traversedBoxes.append(box)
                        
        return traversedBoxes
    
    def findBestBox(self, neighbours, fineBoxesWithoutTim):
        bestBox = fineBoxesWithoutTim[0]
        bestScore = 100000
        
        for fineBox in fineBoxesWithoutTim:
            sumDiff = 0
            for neighbour in neighbours:
                sumDiff += self.imageDifference2(fineBox, neighbour.box, neighbour.neighbourType)
            
            if sumDiff < bestScore:
                bestScore = sumDiff
                bestBox = fineBox

        return bestBox            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    