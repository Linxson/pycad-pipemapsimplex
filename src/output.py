# -*- coding: utf-8 -*-
"""
    =============================
    Author: Linxson
    E-mail: 1853299@tongji.edu.cn
    =============================
"""


def outdxf(acad, dir):
    """
    dir 为保存的文件路径 version2013
    """
    acad.ActiveDocument.SaveAs(dir, 61)


def outdwg(acad, dir):
    """
    dir 为保存的文件路径 version2013
    """
    acad.ActiveDocument.SaveAs(dir, 60)


def outpdf(dir):
    """
    导出pdf
    """
    import pythoncom
    import win32com.client

    def ConvertArrays2Variant(inputdata):
        """数据转换函数"""
        outputdata = win32com.client.VARIANT(
            pythoncom.VT_ARRAY | pythoncom.VT_R8, inputdata)
        return outputdata

    acad = win32com.client.Dispatch(
        "Autocad.Application")  # 获取CAD程序，默认启动最后一次的cad
    doc = acad.ActiveDocument
    # acadmod = doc.ModelSpace
    currentLayout = doc.layouts.item('Model')
    currentPlot = doc.Plot

    # 打印参数设置
    currentLayout.ConfigName = "DWG To PDF.pc3"
    # 设置待打印的图纸
    currentLayout.CanonicalMediaName = 'ISO_full_bleed_A1_(841.00_x_594.00_MM)'
    currentLayout.PlotWithLineweights = True  # 打印线宽
    currentLayout.PaperUnits = 1  # 图纸单位:毫米
    currentLayout.PlotRotation = 0  # 横向打印
    currentLayout.StandardScale = 0  # 打印比例
    currentLayout.CenterPlot = True  # 居中打印
    currentLayout.PlotWithPlotStyles = True  # 依照样式打印
    currentLayout.PlotHidden = False  # 隐藏图纸空间对象

    # 打印
    x1, y1 = 0, 0  # 图框左下角点坐标
    x2, y2 = x1 + 841, y1 + 594  # A1纸规格
    LowerLeft = [x1, y1]  # 图框左下角点/二维点坐标
    UpperRight = [x2, y2]  # 图框右上角点/二维点坐标
    LowerLeft = ConvertArrays2Variant(LowerLeft, "Double")
    UpperRight = ConvertArrays2Variant(UpperRight, "Double")
    currentLayout.SetWindowToPlot(LowerLeft, UpperRight)
    currentLayout.PlotType = 3.5  # acPlotType enum/acWindow=1,2,3.5,4(按照窗口打印)
    currentPlot.PlotToFile(dir)
