#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
                 对图像进行颜色的识别V3,V4
      颜色一共被分为八类，输入为图像，输出为每大类颜色的百分比
          注意，只是单张，对不同图像，需要比对输出
          改进了分类算法，基本上30s处理一张图
          如果可以把cal（）函数的返回值存入数据库，效率更高
                                       陈诚 BruceIce
'''

import cv2 as cv
import numpy as np
import sys

#print __doc__

#读图
'''
java来调用你的文件，那么java获得用户表单里提交的文件名，作为参数传给你的脚本就可以了。
import sys
f1 = sys.argv[1]
f2 = sys.argv[2]
img1 = cv.imread(f1)
img2 = cv.imread(f2)
调用的时候，按照脚本名 +空格 +参数1 + 参数2的方式来运行就可以了
'''
f1 = sys.argv[1]
f2 = sys.argv[2]
img1 = cv.imread(f1)
img2 = cv.imread(f2)



def reshapemat(img):
  '''
  调整图片大小，过小的图片不论，大图片统一变成680*480
  '''
  a, b, c = img.shape
  if a > 680:
    a = 680
  if b > 480:
    b = 480
  frame = np.zeros((b,a))
  holder = cv.resize(img, (b, a), frame, cv.INTER_LINEAR)
  return (holder)
      
def coloreduce(img, div=64):
  '''
  对图片进行降色处理，对提速效果不明显，可以不用
  '''
  w, h, c = img.shape
  for i in range(w-1):
    for j in range(h-1):
      for w in range(c-1):
        img[i,j,w] = img[i,j,w]/div*div+div/2
  return(img)
  
def classcol(img):
  '''
  最主要的函数，对每个像素进行比对分类
  '''
  a, b, c = img.shape
  imgHSV = cv.cvtColor(img,cv.COLOR_BGR2HSV)
  h,s,v =cv.split(imgHSV)
  h = h.reshape((a*b,1))
  v = v.reshape((a*b,1))
  holder = np.zeros((a*b,1))
  for i in range(a*b-1):
    if v[i] == 255:
      holder[i] = 1
    elif v[i] == 0:
      holder[i] = 0
    elif 330<=2*h[i]<360 & 0<2*h[i]<30:
      holder[i] = 2
    elif 30<=2*h[i]<90:
      holder[i] = 3
    elif 90<=2*h[i]<150:
      holder[i] = 4
    elif 150<=2*h[i]<210:
      holder[i] = 5
    elif 210<=2*h[i]<270:
      holder[i] = 6
    else:
      holder[i] = 7
  return(holder)

def cal(classfier):
  '''
  返计算并返回一个长度为8的向量，表示每种颜色的百分比
  '''
  n0 = 0.0
  n1 = 0.0
  n2 = 0.0
  n3 = 0.0
  n4 = 0.0
  n5 = 0.0
  n6 = 0.0
  n7 = 0.0
  l = len(classfier)
  for i in range(l-1):
    if classfier[i] == 0:
    	n0 = n0 + 1
    elif classfier[i] == 1:
    	n1= n1 + 1
    elif classfier[i] == 2:
    	n2 = n2 + 1
    elif classfier[i] == 3:
    	n3 = n3 + 1
    elif classfier[i] == 4:
    	n4 = n4 + 1
    elif classfier[i] == 5:
    	n5 = n5 + 1
    elif classfier[i] == 6:
    	n6 = n6 + 1
    else:
    	n7 = n7 + 1
  vector = [100 * n0/l,100 * n1/l,100 * n2/l,100 * n3/l,100 * n4/l,100 * n5/l,100 * n6/l,100 * n7/l]
  print 'Col0: ', round(100 * n0/l,4), '%'
  print 'Col1: ', round(100 * n1/l,4), '%'
  print 'Col2: ', round(100 * n2/l,4), '%'
  print 'Col3: ', round(100 * n3/l,4), '%'
  print 'Col4: ', round(100 * n4/l,4), '%'
  print 'Col5: ', round(100 * n5/l,4), '%'
  print 'Col6: ', round(100 * n6/l,4), '%'
  print 'Col7: ', round(100 * n7/l,4), '%\n'
  return(vector)



def compare(r1,r2): # vectors to be compared
  '''
  只显示了曼哈顿距离,没有设定cutoff value， thus this function
  won't print out the descion buy only the numbers
  数值越小，说明图片越相似
  '''
  x = 0.0
  for i in range(7):
    x = x + abs(r1[i] - r2[i])
  print '%.2f' % x
  return x


img1 = coloreduce(img1)
img2 = coloreduce(img2)
classfier1 = classcol(img1)
classfier2 = classcol(img2)


pct1 = cal(classfier1)
pct2 = cal(classfier2)

compare(pct1,pct2)
