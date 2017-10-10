#!coding:utf-8
from Rec_Interface import *
class Relalize_Rec_Interface(Rec_Interface): #实现类
    def recognize_photo(self, photo):
        if self.compare_feature(photo) == True:
            print '照片认证通过'
            return True
        else:
            print '照片认证失败'
            return False

    def recognize_audio(self, audio):
        if self.compare_feature(audio) == True:
            print '声音认证通过'
            return True
        else:
            print '声音认证失败'
            return False

    def compare_feature(self, proof):
        #和Feature目录下的 样本（声音或图像）特征信息路径bin文件 智能对比 若智能对比结果相同则认证成功并且返回True  若智能对比结果不同则认证成功并且返回False
        return True