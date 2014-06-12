#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
                 对图像进行颜色的识别
      采用最naive的识别方式，比较图像三色直方图再加权
      缺陷：每次只能读取2个文件比较，且必须到源码里改路径
'''

import cv2 as cv
import numpy as np
print __doc__

#读取图像，自己改路径
img1 = cv.imread('test1.png') 
img2 = cv.imread('test2.png')

b1, g1, r1 = cv.split(img1)
b2, g2, r2 = cv.split(img2)

#画图，可用于直观检验
def calcAndDrawHist(image, color): 
    hist= cv.calcHist([image], [0], None, [256], [0.0,255.0])  
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(hist)  
    histImg = np.zeros([256,256,3], np.uint8)  
    hpt = int(0.9* 256);  
      
    for h in range(256):  
        intensity = int(hist[h]*hpt/maxVal)  
        cv.line(histImg,(h,256), (h,256-intensity), color)  
    return histImg;

histimgB1 = calcAndDrawHist(b1,[255,0,0])
histimgG1 = calcAndDrawHist(g1,[0,255,0])
histimgR1 = calcAndDrawHist(r1,[0,0,255])
histimgB2 = calcAndDrawHist(b2,[255,0,0])
histimgG2 = calcAndDrawHist(g2,[0,255,0])
histimgR2 = calcAndDrawHist(r2,[0,0,255])


histB1 = cv.calcHist([b1],[0], None, [256], [0.0,255.0])
histG1 = cv.calcHist([g1],[0], None, [256], [0.0,255.0])
histR1 = cv.calcHist([r1],[0], None, [256], [0.0,255.0])
histB2 = cv.calcHist([b2],[0], None, [256], [0.0,255.0])
histG2 = cv.calcHist([g2],[0], None, [256], [0.0,255.0])
histR2 = cv.calcHist([r2],[0], None, [256], [0.0,255.0])

histB1 = cv.normalize(histB1)
histG1 = cv.normalize(histG1) 
histR1 = cv.normalize(histR1)
histB2 = cv.normalize(histB2)
histG2 = cv.normalize(histG2)
histR2 = cv.normalize(histR2)


'''
cv.imshow('histimgB1',histimgB1)
cv.imshow('histimgG1',histimgG1)
cv.imshow('histimgR1',histimgR1)
cv.imshow('histimgB2',histimgB2)
cv.imshow('histimgG2',histimgG2)
cv.imshow('histimgR2',histimgR2)
cv.waitKey(0)
cv.destroyAllWindows()
'''

tempB = cv.compareHist(histB1,histB2,3)
tempR = cv.compareHist(histR1,histR2,3)
tempG = cv.compareHist(histG1,histG2,3)
result = round(.33*(1-tempB)+.33*(1-tempG)+.33*(1-tempR),4)

'''
具体细节参数，可以调看
print tempG,tempR,tempB
print u'蓝色相似度为%.4f\n' % (1-tempB)
print u'绿色相似度为%.4f\n' % (1-tempG)
print u'红色相似度为%.4f\n' % (1-tempR)
'''
print u'\t\t 两幅图像相似度', result,'\n'

#判定值，可以自己调整
cutoffValue = 0.7

if result > cutoffValue :
    print u"\t\t\t结论：盗版"
else:
    print u'\t\t结论：没有抄我的颜色'
