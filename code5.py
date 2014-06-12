#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
                 对图像进行颜色的识别V5
      颜色一共被分为八类，输入为图像，输出为每大类颜色的百分比
          注意，只是单张，对不同图像，需要比对输出
          改进了分类算法，基本上30s处理一张图
          如果可以把cal（）函数的返回值存入数据库，效率更高
                            陈诚 IceBruce ******@163.com
'''

import cv2 as cv
import numpy as np
import sys

#显示自述文件，加注释可取消显示
print __doc__

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

#img1 = cv.imread('testpics/test1.png') #本地调试用
#img2 = cv.imread('testpics/test2.png')

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
  n0 = 0.0
  n1 = 0.0
  n2 = 0.0
  n3 = 0.0
  n4 = 0.0
  n5 = 0.0
  n6 = 0.0
  n7 = 0.0
  a, b, c = img.shape
  l = a*b
  imgHSV = cv.cvtColor(img,cv.COLOR_BGR2HSV)
  h,s,v =cv.split(imgHSV)
  h = h.reshape((a*b,1))
  v = v.reshape((a*b,1))
  for i in range(a*b-1):
    if v[i] == 255:
      n0 = n0 + 1
    elif v[i] == 0:
      n1 = n1 + 1 
    elif 330<=2*h[i]<360 & 0<2*h[i]<30:
      n2 = n2 + 1
    elif 30<=2*h[i]<90:
      n3 = n3 + 1
    elif 90<=2*h[i]<150:
      n4 = n4 + 1
    elif 150<=2*h[i]<210:
      n5 = n5 + 1
    elif 210<=2*h[i]<270:
      n6 = n6 + 1
    else:
      n7 = n7 + 1
  vector = [100 * n0/l,100 * n1/l,100 * n2/l,100 * n3/l,100 * n4/l,100 * n5/l,100 * n6/l,100 * n7/l]
  return(vector)

def printres(vector):
  '''
  返计算并返回一个长度为8的list，表示每种颜色的百分比
  '''
  n0, n1, n2, n3, n4, n5, n6, n7, =vector.sort(reverse = True)
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
  返回r1,r2比例最大的前三者之间差的绝对值的和， 也叫曼哈顿距离
  
  数值越小，说明图片越相似
  '''
  x = 0.0
  for i in range(2):
    x = x + abs(r1[i] - r2[i])
  print '%.2f' % x
  return x

#对图片进行降色处理
img1 = coloreduce(img1)
img2 = coloreduce(img2)
#调整图片大小，提高速度
img1 = reshapemat(img1)
img2 = reshapemat(img2)
#开始进行颜色分类
pct1 = classcol(img1)
pct2 = classcol(img2)
#输出结果
compare(pct1,pct2)
input('Press any key to quit')
