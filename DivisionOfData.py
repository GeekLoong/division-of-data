import os
import numpy as np
import math
import shutil
import tkinter as tk
from tkinter import filedialog

# 使用时请选择数据集根目录，根目录必须包含images与labels两个子目录
# images（原图）与labels（标签）对应
# train：训练集（训练模型）
# val：验证集（选择模型）
# test：测试集（评估模型）

# 遍历images、labels目录中的文件树
# 得到单个文件对象
# 利用随机数将文件名打乱放入数组对象中
# 对数组进行切割，分成三份元组，按照比例 train(7),val(2),test(1)
# 遍历单个元组，按照元组中的文本查找文件并分类

# walk 函数，一个目录，返回三个元组，第一个是目录路径，第二个参数是子目录树，第三个参数是该目录下的文件树


# 数据提取函数，将文件夹中的名称提取出来
# paths 文件夹路径
def data_extraction(paths):
    file_name_list = np.array([])
    for dirs, subdir, fileList in os.walk(paths):
        for file in fileList:
            # 文件名与文件后辍分割
            file_name = os.path.splitext(file)[0]
            # 将文件名放入数组中
            if file_name != 'classes':
                file_name_list = np.append(file_name_list, file_name)
    return file_name_list


# 分配资源（随机）
def allocation(file_list: np.array([]), percentage: list):
    # 随机为 train 分配资源
    train_num = math.floor(np.size(file_list) * percentage[0])
    train_list = np.random.choice(file_list, train_num, replace=False)

    # 得到剩余资源
    leftover_list = np.setdiff1d(file_list, train_list)

    # 随机为 val 分配资源
    val_num = math.floor(np.size(file_list) * percentage[1])
    val_list = np.random.choice(leftover_list, val_num, replace=False)

    # test 拾取剩下资源
    test_list = np.setdiff1d(leftover_list, val_list)
    return np.array([train_list, val_list, test_list], dtype=object)


# 检测文件夹是否存在
def dir_make(path):
    if not os.path.exists(path):
        os.makedirs(path)


# 根据文件名移动文件
def file_move(path, path2, __name__):
    # 遍历老目录
    for root, dirs, files in os.walk(path):
        # 查找文件
        for filename in files:
            if name in filename:
                var = r'\%s' % filename
                shutil.move(path + var, path2 + var)
                print(path + var + ' 已经被划分到 ' + path2 + var)
                break
        break


# 主函数
if __name__ == '__main__':
    # 实例化tkinter
    tk.Tk().withdraw()
    # 打开资源管理器对话框选择根路径
    PATH = filedialog.askdirectory()
    # 图片路径
    ImgPath = PATH + r'\images'
    # 标注路径
    LabelPath = PATH + r'\labels'
    # 训练占比，分别对应 train、val，分配前两个参数时，请不要超过0.9，因为test会自动得到剩下的图片
    PERCENTAGE = [0.7, 0.2]
    # 检测 train 文件夹
    ImgTrainPath = ImgPath + r'\train'
    dir_make(ImgTrainPath)
    LabTrainPath = LabelPath + r'\train'
    dir_make(LabTrainPath)

    # 检测 val 文件夹
    ImgValPath = ImgPath + r'\val'
    dir_make(ImgValPath)
    LabValPath = LabelPath + r'\val'
    dir_make(LabValPath)

    # 检测 test 文件夹
    ImgTestPath = ImgPath + r'\test'
    dir_make(ImgTestPath)
    LabTestPath = LabelPath + r'\test'
    dir_make(LabTestPath)

    # 获得资源分配
    res = allocation(data_extraction(ImgPath), PERCENTAGE)
    # 遍历三个数组
    for res_item in res:
        # 遍历当前数组
        for name in res_item:
            # train 分类
            if name in res[0]:
                file_move(ImgPath, ImgTrainPath, name)
                file_move(LabelPath, LabTrainPath, name)
            # val 分类
            elif name in res[1]:
                file_move(ImgPath, ImgValPath, name)
                file_move(LabelPath, LabValPath, name)
            # test 分类
            else:
                file_move(ImgPath, ImgTestPath, name)
                file_move(LabelPath, LabTestPath, name)
