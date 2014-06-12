#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
                 对图像进行颜色的识别V2
      颜色一共被分为八类，输入为图像，输出为每大类颜色的百分比
          注意，只是单张，对不同图像，需要比对输出
'''

import cv2 as cv
import numpy as np
import sys

#print __doc__

#读图
'''
如果是java来调用你的文件，那么java获得用户表单里提交的文件名，作为参数传给你的脚本就可以了。
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

#img3 = cv.imread('test3.jpg')
#img4 = cv.imread('test4.jpg')
#img5 = cv.imread('test5.png')
#img6 = cv.imread('test6.png')

def reshapemat(img):
  a, b, c = img.shape
  size = a*b
  holder = np.zeros((size,3))
  b, g, r = cv.split(img)
  b = b.reshape((size,1))
  r = r.reshape((size,1))
  g = g.reshape((size,1))
  for i in range(size-1):
    for j in range(2):
      if j == 0:
        holder[i, j] = b[i]
      elif j == 1:
        holder[i, j] = g[i]
      else:
        holder[i, j] = r[i]
  return (holder)
      
def coloreduce(img, div=64):
    w, h, c = img.shape
    for i in range(w-1):
      for j in range(h-1):
        for w in range(c-1):
          img[i,j,w] = img[i,j,w]/div*div+div/2
    return(img)
  
def classcol(img):
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
  n0 = float(sum(classfier == 0)) / len(classfier)*100
  n1 = float(sum(classfier == 1)) / len(classfier)*100
  n2 = float(sum(classfier == 2)) / len(classfier)*100
  n3 = float(sum(classfier == 3)) / len(classfier)*100
  n4 = float(sum(classfier == 4)) / len(classfier)*100
  n5 = float(sum(classfier == 5)) / len(classfier)*100
  n6 = float(sum(classfier == 6)) / len(classfier)*100
  n7 = float(sum(classfier == 7)) / len(classfier)*100
  vector = [n0,n1,n2,n3,n4,n5,n6,n7]
  print 'col 0:', n0,'%'
  print 'col 1:', n1,'%'
  print 'col 2:', n2,'%'
  print 'col 3:', n3,'%'
  print 'col 4:', n4,'%'
  print 'col 5:', n5,'%'
  print 'col 6:', n6,'%'
  print 'col 7:', n7,'%\n'
  return(vector)

def compare(r1,r2): # vectors to be compared
  x = 0.0
  for i in range(7):
    x = x + abs(r1[i] - r2[i])
  return '%.2f' % x

classfier1 = classcol(img1)
classfier2 = classcol(img2)
#classfier3 = classcol(img3)
#classfier4 = classcol(img4)
#classfier5 = classcol(img5)
#classfier6 = classcol(img6)

pct1 = cal(classfier1)
pct2 = cal(classfier2)
#pct3 = cal(classfier3)
#pct4 = cal(classfier4)
#pct5 = cal(classfier5)
#pct6 = cal(classfier6)

