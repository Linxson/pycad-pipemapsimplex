# -*- coding: utf-8 -*-
"""
    =============================
    Author: Linxson
    E-mail: 1853299@tongji.edu.cn
    =============================
"""
from pyautocad import APoint, aDouble


def plot(acad, dir, d):
    # 背景图确定
    acad.ActiveDocument.Application.Documents(dir).Activate()

    # 图层
    LayerObj = acad.ActiveDocument.Layers.Add("等水压线")  # 添加新图层
    acad.ActiveDocument.ActiveLayer = LayerObj  # 将图层设置为当前图层。
    LayerObj.color = 44  # 设置颜色，颜色为橘黄
    LayerObj.Lineweight = 30  # 设置线宽，13为0.13

    # 线型
    try:
        acad.ActiveDocument.Linetypes.Load("ACAD_ISO04W100", "acadiso.lin")
    except:
        print("线型已加载")
    LayerObj.Linetype = "ACAD_ISO04W100"

    # 文字标注
    txtStyleObj = acad.ActiveDocument.TextStyles.add("水压线仿宋")
    acad.ActiveDocument.ActiveTextStyle = acad.ActiveDocument.TextStyles.Item(
        "水压线仿宋")
    acad.ActiveDocument.ActiveTextStyle.SetFont("仿宋", False, False, 1, 0 or 0)
    txtStyleObj.Width = 0.75  # 宽度0.75

    # 算法
    n = 0  # 头标签
    while n < d.nodeTotal:
        label = d.nodex[n].value
        num = d.nodey[n].value
        splinePnts = []
        for i in range(1, num+1):  # 循环：把坐标放到splinePnts里
            splinePnts.append(APoint(d.nodex[n+i].value, d.nodey[n+i].value))
        startTan = splinePnts[0]
        endTan = splinePnts[-1]
        splinePnts = [j for i in splinePnts for j in i]
        splinePnts = aDouble(splinePnts)
        # 循环外：对splinePant进行处理，start选择第一个点坐标，end选择最后一个点坐标
        SplineObj = acad.model.AddSpline(splinePnts, startTan, endTan)
        SplineObj.LinetypeScale = 20  # 线型比例为20
        # 标签
        textString = str(label)+".00"
        insertPnt = endTan
        height = 50
        textObj = acad.model.AddText(textString, insertPnt, height)
        textObj.Alignment = 4  # middle
        textObj.TextAlignmentPoint = insertPnt
        # 一次循环
        n = n+num+1
