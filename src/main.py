# -*- coding: utf-8 -*-
"""
    =============================
    Author: Linxson
    E-mail: 1853299@tongji.edu.cn
    =============================
"""
# 导入外部库
import datetime
import os
from pyautocad import Autocad

# 导入自己写的模块
import afterPlot
import conPlot
import contour
import datafile
import output

# 绝对路径
workingdic= os.getcwd()

def datamax():
    """传入最高日最高时数据"""
    dir = workingdic + '\\data\\data_max.xlsx'
    d = datafile.Data(dir)
    return d


def datafire():
    """传入消防工况数据"""
    dir = workingdic + '\\data\\data_fire.xlsx'
    d = datafile.Data(dir)
    return d


def dataacc():
    """传入意外事故工况数据"""
    dir = workingdic + '\\data\\data_acc.xlsx'
    d = datafile.Data(dir)
    return d


def condata(sheet="Sheet2"):
    """
    传入高程数据
    Sheet1 是高程图
    Sheet2 是最高日最高时等水压线数据，默认值
    Sheet3 是消防工况数据
    Sheet4 是意外事故工况数据
    """
    dir = workingdic + '\\data\\contourM.xlsx'
    dc = datafile.ConData(dir, sheet)
    return dc


"""
    test1_后缀
    测试生成dxf代码，不会影响dwg文件
"""


def test1_func1(dir, sht, outdir, dxf):
    """
    内容：绘制工况图
    测试须知：运行此函数需提前打开acc、tmp、max、fire的dwg文件
    输出：dxf文件，属于手改图前操作
    """
    acad = Autocad(create_if_not_exists=True)
    if sht == 'Sheet2':
        d = datamax()
    elif sht == 'Sheet3':
        d = datafire()
    elif sht == 'Sheet4':
        d = dataacc()
    else:
        pass

        # 运行前先把如下名称的背景图打开
    conPlot.plot(acad, dir, d)

    # 保存为dxf文件
    if dxf == True:
        output.outdxf(acad, outdir)
    else:
        output.outdwg(acad, outdir)


def test1_max():
    t1 = datetime.datetime.now()

    test1_func1(dir="max.dwg",
                sht="Sheet2",
                outdir=workingdic + "\\data\\dxf\\max",
                dxf=True)
    t2 = datetime.datetime.now()
    print("绘制最高时最高日工况图用时:{0}".format(t2 - t1))


def test1_fire():
    t2 = datetime.datetime.now()
    test1_func1(dir="fire.dwg",
                sht="Sheet3",
                outdir=workingdic + "\\data\\dxf\\fire",
                dxf=True)
    t3 = datetime.datetime.now()
    print("绘制消防工况图用时:{0}".format(t3 - t2))


def test1_acc():
    t3 = datetime.datetime.now()
    test1_func1(dir="acc.dwg",
                sht="Sheet4",
                outdir=workingdic + "\\data\\dxf\\acc",
                dxf=True)
    t4 = datetime.datetime.now()
    print("绘制意外事故工况图用时:{0}".format(t4 - t3))


def test1_tmp():
    try:
        t4 = datetime.datetime.now()
        test1_func1(dir="tmp.dwg",
                    sht="Sheet2",
                    outdir=workingdic + "\\data\\dxf\\tmp_new",
                    dxf=False)
        t5 = datetime.datetime.now()
        print("生成template文件用时:{0}".format(t5 - t4))
    except:
        print("生成template文件失败")


"""
    test2
    内容：替换函数
    输出：更换参数后的dxf文件
"""


def test2():
    t1 = datetime.datetime.now()

    afterPlot.textreplace(template=workingdic + '\\data\\dxf\\tmp_fire.dxf',
                          dir=workingdic + '\\data\\dxf\\fire.dxf')
    afterPlot.textreplace(template=workingdic + '\\data\\dxf\\tmp_max.dxf',
                          dir=workingdic + '\\data\\dxf\\max.dxf')
    afterPlot.textreplace(template=workingdic + '\\data\\dxf\\tmp_acc.dxf',
                          dir=workingdic + '\\data\\dxf\\acc.dxf')
    t2 = datetime.datetime.now()
    print("test3用时:{0}".format(t2 - t1))


"""
    test3_后缀：
    绘制等值线，运行前先打开对应的文件
"""


def test3_func3(dir, sht, outdir):
    """没有func2"""
    acad = Autocad(create_if_not_exists=True)
    dc = condata(sheet=sht)
    contour.plot(acad, dir, dc)
    output.outdwg(acad, outdir)


def test3_fire():
    t1 = datetime.datetime.now()

    test3_func3(dir="tmp_fire.dwg",
                sht="Sheet3",
                outdir=workingdic + "\\output\\fire")
    t2 = datetime.datetime.now()
    print("绘制消防工况图等压线用时:{0}".format(t2 - t1))


def test3_max():
    t2 = datetime.datetime.now()
    test3_func3(dir="tmp_max.dwg",
                sht="Sheet2",
                outdir=workingdic + "\\output\\max")
    t3 = datetime.datetime.now()
    print("绘制最高时最高日工况图等压线用时:{0}".format(t3 - t2))


def test3_acc():
    t3 = datetime.datetime.now()
    test3_func3(dir="tmp_acc.dwg",
                sht="Sheet4",
                outdir=workingdic + "\\output\\acc")
    t4 = datetime.datetime.now()
    print("绘制意外事故工况图等压线用时:{0}".format(t4 - t3))


def test4():
    """制作定线图"""
    t1 = datetime.datetime.now()
    afterPlot.deleteLayer('节点流量')
    afterPlot.deleteLayer('节点压力')
    # afterPlot.deleteLayer('等水压线')
    afterPlot.deleteLayer('下管段标注')
    t2 = datetime.datetime.now()
    print("test4删除图层用时:{0}".format(t2 - t1))

    # 绘制等值线
    acad = Autocad(create_if_not_exists=True)
    dir = 'tmp_ali.dwg'
    dc = condata(sheet='Sheet1')
    contour.plot(acad, dir, dc)

    # 另存为
    output.outdwg(acad, dir=workingdic + "\\output\\ali")

    t3 = datetime.datetime.now()
    print("test4总用时:{0}".format(t3 - t1))


if __name__ == '__main__':
    """
    在python的编译配置中，working directory中的最后落脚是落在pycad-pipemapsimplex上
    e.g. working directory--> D:\01毕业设计\pycad-pipemapsimplex
    """
    test1_max()
    # test1_fire()
    # test1_acc()
    # test1_tmp()
    # test2()
    # test3_max()
    # test3_fire()
    # test3_acc()
    # test4()
    # pass
