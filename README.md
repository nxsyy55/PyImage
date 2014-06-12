pyL
===

PythonForImage


对应展示文档，整个项目有两部分组成，颜色识别和logo识别。
1.判断两幅图像颜色组成是否相似
2.根据客户提供的商标图片在目标图片中查找相同区域（或相似处）

第一个任务，由code5.py完成，自写
第二个，由asift.py, common.py, and find_obj.py完成，源自opencv的python2 sample
代码效果可以看展示文档
oldVersion目录下放的是code5的历史版本
testpics目录下是所有测试图片，调试是可以自己去代码里改路劲，注意后缀。

代码细节
看注释。

关于如何提高asift.py程序的识别图：
	用实际截图去做对比
	可以去微调两个函数的参数（推荐调第二个）
	affine_skew里的phi,控制模型里的向量空间的旋转角度
	128行matcher.knnMatch()里的k，注意：结果对k很敏感，2是理论上的最优结果。如果用k=3或更高，可以剔除80%的图片（如果只是用相似的logo去找）,过于苛刻。
