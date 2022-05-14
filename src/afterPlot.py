# -*- coding: utf-8 -*-
"""
    =============================
    Author: Linxson
    E-mail: 1853299@tongji.edu.cn
    =============================
"""


def textreplace(template, dir):
    """
    template: 手动调整好的dxf文件
    dir: 原始数据
    """
    import ezdxf

    doc1 = ezdxf.readfile(template)
    doc2 = ezdxf.readfile(dir)
    msp1 = doc1.modelspace()
    msp2 = doc2.modelspace()
    oriText = []
    for e2 in msp2:
        if e2.dxftype() == "TEXT":
            oriText.append(e2.dxf.text)
    n = 0
    for e1 in msp1:
        if e1.dxftype() == "TEXT":
            e1.dxf.text = oriText[n]
            n += 1
    doc1.save()


def deleteLayer(layername, Point1=[20000, 4000, 0], Point2=[35000, 14000, 0]):
    """
    删除图层：节点流量、节点压力、等水压线
    运行前确保cad只打开了待修改的文件！
    """
    import win32com.client
    import pythoncom

    def ConvertArrays2Variant(inputdata, vartype="Variant"):

        if vartype == "Double":  # 双精度
            outputdata = win32com.client.VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_R8, inputdata)
        if vartype == "ShortInteger":  # 短整型
            outputdata = win32com.client.VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_I2, inputdata)
        if vartype == "Variant":  # 变体
            outputdata = win32com.client.VARIANT(
                pythoncom.VT_ARRAY | pythoncom.VT_VARIANT, inputdata)
        return outputdata

    acad = win32com.client.Dispatch(
        "Autocad.Application")  # 获取CAD程序，默认启动最后一次的cad
    doc = acad.ActiveDocument

    Mode = 0
    Point1 = ConvertArrays2Variant(Point1, "Double")
    Point2 = ConvertArrays2Variant(Point2, "Double")

    try:
        doc.SelectionSets.Item("SS1").Delete()
    except:
        print("Delete selection failed")

    ssetObj = doc.SelectionSets.Add("SS1")  # 创建选择集

    FilterType = [8, ]  # 组码8表示图层
    FilterData = [layername, ]
    FilterType = ConvertArrays2Variant(FilterType, "ShortInteger")
    FilterData = ConvertArrays2Variant(FilterData, "Variant")
    ssetObj.Select(Mode, Point1, Point2, FilterType, FilterData)
    print(len(ssetObj))  # 被选择对象的个数
    for obj in ssetObj:
        obj.Delete()  # 删除对象
    ssetObj = 0
