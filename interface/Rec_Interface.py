#!coding:utf-8
class Rec_Interface:
    def recognize_photo(self, photo):
        #传入photo 再将photo传入 compare_feature(proof)
        pass

    def recognize_audio(self, audio):
        # audio 再将audio传入 compare_feature(proof)
        pass

    def compare_feature(self, proof):
        # 和Feature目录下的 样本（声音或图像）特征信息路径bin文件  做对比
        #若对比结果相同则认证成功并且返回True  若智能对比结果不同则认证成功并且返回False
        pass

    def build_proof(self,proof):
        #学生样本构建 第一次传入时
        pass