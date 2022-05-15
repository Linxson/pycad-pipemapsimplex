# -*- coding: utf-8 -*-
"""
    =============================
    Author: Linxson
    E-mail: 1853299@tongji.edu.cn
    =============================
"""

from pyautocad import APoint, aDouble
import math


def layer(acad, name, color=0, Lineweight=0):
    """
    name：图层名字
    color:图层颜色，数字
    lineweight：图层线宽，数字
    """
    LayerObj = acad.ActiveDocument.Layers.Add(name)  # 添加新图层
    LayerObj.color = color
    LayerObj.Lineweight = Lineweight
    return LayerObj


def textStyle(acad, StyleName, FontName, Width):
    """
    stylename：字体自命名，如标注500
    Fontname：字体系统名字，如仿宋
    Width：宽度因子，0.75一般
    """
    txtStyleObj = acad.ActiveDocument.TextStyles.add(StyleName)
    acad.ActiveDocument.ActiveTextStyle = acad.ActiveDocument.TextStyles.Item(
        StyleName)
    acad.ActiveDocument.ActiveTextStyle.SetFont(FontName, False, False, 1, 0 or 0)
    txtStyleObj.Width = Width  # 宽度0.75
    return txtStyleObj


def plot1(acad, d, radius=50):
    """
    绘制节点
    """
    for nodei in range(1, d.nodeTotal):
        # 画圆：根据坐标以半径画圆
        center = APoint(d.nodex[nodei].value, d.nodey[nodei].value)
        circleObj = acad.model.AddCircle(center, radius)
        # 节点标注
        textStrNode = d.nodeId[nodei].value[-3:]  # 取节点ID的后三位
        insertPntNode = APoint(d.nodex[nodei].value, d.nodey[nodei].value)
        heightNode = radius * 0.8  # heightnode：节点内圆字体高度
        textObjNode = acad.model.AddText(textStrNode, insertPntNode, heightNode)
        textObjNode.Alignment = 4  # alignment:text以什么位置为中心，默认为middle对齐
        textObjNode.TextAlignmentPoint = insertPntNode


def plot2(acad, d, radius=50):
    """
    绘制管段直线，并在管段直线中间添加水流方向填充块
    radius不仅是节点半径，还作为水流方向填充块的长度
    """
    for pipei in range(1, d.pipeTotal):

        # 寻找节点对应坐标
        starti, endi = 0, 0
        for n in range(1, d.nodeTotal):
            if d.nodeId[n].value == d.pipe_startnode[pipei].value:
                starti = n
            if d.nodeId[n].value == d.pipe_endnode[pipei].value:
                endi = n
            if starti != 0 and endi != 0:
                break

        # 将直线头尾部分各减一个半径的距离
        angle = math.atan2(d.nodey[endi].value - d.nodey[starti].value,
                           d.nodex[endi].value - d.nodex[starti].value)
        temp_startx = d.nodex[starti].value + abs(radius * math.cos(
            angle)) if d.nodex[starti].value < d.nodex[endi].value else \
            d.nodex[starti].value - abs(radius * math.cos(angle))
        temp_endx = d.nodex[endi].value + abs(radius * math.cos(
            angle)) if d.nodex[starti].value > d.nodex[endi].value else \
            d.nodex[endi].value - abs(radius * math.cos(angle))
        temp_starty = d.nodey[starti].value + abs(radius * math.sin(
            angle)) if d.nodey[starti].value < d.nodey[endi].value else \
            d.nodey[starti].value - abs(radius * math.sin(angle))
        temp_endy = d.nodey[endi].value + abs(radius * math.sin(
            angle)) if d.nodey[starti].value > d.nodey[endi].value else \
            d.nodey[endi].value - abs(radius * math.sin(angle))

        # 水流方向：填充块，置于管段中点处，如果流量是正值，则从上游节点指向下游节点，反之
        xmid = (d.nodex[starti].value + d.nodex[endi].value) / 2
        ymid = (d.nodey[starti].value + d.nodey[endi].value) / 2
        lmid = radius  # 水流填充块的长度，这里与radius取相同值
        if d.isclose[pipei].value != 'Closed':
            if d.q[pipei].value < 0:
                trix1 = xmid - lmid * math.cos(angle)
                triy1 = ymid - lmid * math.sin(angle)
                trix2 = trix1 + 2.0 * lmid / math.cos(math.pi / 12) * math.cos(angle + math.pi / 12)
                triy2 = triy1 + 2.0 * lmid / math.cos(math.pi / 12) * math.sin(angle + math.pi / 12)
                trix3 = trix1 + 2.0 * lmid / math.cos(math.pi / 12) * math.cos(angle - math.pi / 12)
                triy3 = triy1 + 2.0 * lmid / math.cos(math.pi / 12) * math.sin(angle - math.pi / 12)
            else:
                trix1 = xmid + lmid * math.cos(angle)
                triy1 = ymid + lmid * math.sin(angle)
                trix2 = trix1 - 2.0 * lmid / math.cos(math.pi / 12) * math.cos(angle + math.pi / 12)
                triy2 = triy1 - 2.0 * lmid / math.cos(math.pi / 12) * math.sin(angle + math.pi / 12)
                trix3 = trix1 - 2.0 * lmid / math.cos(math.pi / 12) * math.cos(angle - math.pi / 12)
                triy3 = triy1 - 2.0 * lmid / math.cos(math.pi / 12) * math.sin(angle - math.pi / 12)
            trpnt1, trpnt2, trpnt3 = (APoint(trix1, triy1), APoint(trix2, triy2), APoint(trix3, triy3))
            solidObj = acad.model.AddSolid(trpnt1, trpnt2, trpnt3, trpnt3)

        # 三点多段线
        startPoint = APoint(temp_startx, temp_starty)
        endPoint = APoint(temp_endx, temp_endy)
        midPoint = APoint(xmid, ymid)
        pntpolyline = [startPoint, midPoint, endPoint]
        pntpolyline = [j for i in pntpolyline for j in i]
        pntpolyline = aDouble(pntpolyline)
        acad.model.AddPolyLine(pntpolyline)


def plot3(acad, d, radius, layerUP, layerDOWM):
    """
    因为上下管段标注在两个不同的图层
    layerUP即上管段标注图层对象
    layerDOWM为下管段标注图层对象
    radius用于作为管段文字标注高度
    """
    for pipej in range(1, d.pipeTotal):
        # 寻找节点对应坐标
        starti, endi = 0, 0
        for n in range(1, d.nodeTotal):
            if d.nodeId[n].value == d.pipe_startnode[pipej].value:
                starti = n
            if d.nodeId[n].value == d.pipe_endnode[pipej].value:
                endi = n
            if starti != 0 and endi != 0:
                break
        # 基本数据
        xmid = d.nodex[starti].value + (d.nodex[endi].value - d.nodex[starti].value) * 0.5
        ymid = d.nodey[starti].value + (d.nodey[endi].value - d.nodey[starti].value) * 0.5
        angle = (math.atan2(d.nodey[endi].value - d.nodey[starti].value,
                            d.nodex[endi].value - d.nodex[starti].value))
        insertPntPipe = APoint(xmid, ymid)
        heightPipe = radius * 0.8  # 管段标注的文字高度，取半径的0.8倍
        BasePointPipe = APoint(xmid, ymid)
        RotationAnglePipe = math.radians(angle * 180 / math.pi)

        # 画上管段：将图层设置为当前图层
        acad.ActiveDocument.ActiveLayer = layerUP
        # 标注1：在线的中点上方“[管段编号]-长度-管径”
        textStrPipe1 = ('[' + d.pipeId[pipej].value[-3:] + ']-' +
                        str(d.ln[pipej].value) + '-' + str(d.dn[pipej].value))
        textObjPipe1 = acad.model.AddText(
            textStrPipe1, insertPntPipe, heightPipe)
        textObjPipe1.Alignment = 13  # bottomcenter对齐
        textObjPipe1.TextAlignmentPoint = insertPntPipe
        textObjPipe1.Rotate(BasePointPipe, RotationAnglePipe)
        movx1 = xmid - 30 * math.sin(angle)
        movy1 = ymid + 30 * math.cos(angle)
        MovePointPipe1 = APoint(movx1, movy1)
        textObjPipe1.Move(BasePointPipe, MovePointPipe1)

        # 画下管段：将图层设置为当前图层
        acad.ActiveDocument.ActiveLayer = layerDOWM
        # 标注2：在线的中点下方“流量-流速-单位水损”,保留两位小数
        textStrPipe2 = '{:.2f}-{:.2f}-{:.2f}'.format(d.absq[pipej].value,
                                                     d.vn[pipej].value,
                                                     d.unithj[pipej].value)
        textObjPipe2 = acad.model.AddText(
            textStrPipe2, insertPntPipe, heightPipe)
        textObjPipe2.Alignment = 7  # topcenter对齐
        textObjPipe2.TextAlignmentPoint = insertPntPipe
        textObjPipe2.Rotate(BasePointPipe, RotationAnglePipe)
        movx2 = xmid + 30 * math.sin(angle)
        movy2 = ymid - 30 * math.cos(angle)
        MovePointPipe2 = APoint(movx2, movy2)
        textObjPipe2.Move(BasePointPipe, MovePointPipe2)


def plot4(acad, d, radius, distance=185):
    """
    绘制节点流量及其标注
    distance为节点流量圆和节点编号圆的距离，默认为185
    """
    for nodei in range(1, d.nodeTotal):
        if d.nodeq[nodei].value != 0:
            # 画圆
            centerNodexq = d.nodex[nodei].value - distance * math.cos(math.pi / 4)
            centerNodeyq = d.nodey[nodei].value - distance * math.sin(math.pi / 4)
            centerQ = APoint(centerNodexq, centerNodeyq)
            radiusQ = radius * 1.2
            circleObjQ = acad.model.AddCircle(centerQ, radiusQ)
            # 标出流量数据
            textStrNodeQ = '{:.2f}'.format(d.nodeq[nodei].value)
            insertPntNodeQ = APoint(centerNodexq, centerNodeyq)
            heightNodeQ = radius * 0.8
            textObjNodeQ = acad.model.AddText(textStrNodeQ, insertPntNodeQ, heightNodeQ)
            textObjNodeQ.Alignment = 4  # middle对齐
            textObjNodeQ.TextAlignmentPoint = insertPntNodeQ

            # 画直线：将直线头尾部分各减一个半径的距离，角度采用pi/4，长度用distance
            temp_startxQ, temp_startyQ = (centerNodexq + radiusQ * math.cos(math.pi / 4),
                                          centerNodeyq + radiusQ * math.sin(math.pi / 4))
            temp_endxQ, temp_endyQ = (d.nodex[nodei].value - radius * math.cos(math.pi / 4),
                                      d.nodey[nodei].value - radius * math.sin(math.pi / 4))
            startPointQ = APoint(temp_startxQ, temp_startyQ)
            endPointQ = APoint(temp_endxQ, temp_endyQ)
            lineObjQ = acad.model.AddLine(startPointQ, endPointQ)
            # 辅助线
            l = radius * 0.5
            subq1x, subq1y = temp_startxQ + l * math.cos(75 / 180 * math.pi), \
                             temp_startyQ + l * math.sin(75 / 180 * math.pi)
            subq2x, subq2y = temp_startxQ + l * math.cos(15 / 180 * math.pi), \
                             temp_startyQ + l * math.sin(15 / 180 * math.pi)
            endPointQsub1 = APoint(subq1x, subq1y)
            endPointQsub2 = APoint(subq2x, subq2y)
            lineObjQsub1 = acad.model.AddLine(startPointQ, endPointQsub1)
            lineObjQsub2 = acad.model.AddLine(startPointQ, endPointQsub2)
        else:
            pass


def plot5(acad, d, radius, box=[140, 180]):
    """
    绘制节点水头
    比较复杂，是一个类似于三层抽屉的箱子，每层都存放一个数据
    box：三个数据分别为这个箱子的长、宽,宽最好是3的倍数
    """
    for nodei in range(1, d.nodeTotal):
        if d.nodeq[nodei].value != 0:
            # 直线：长140，宽180，每格60
            boxw, boxh, unith = box[0], box[1], box[1] / 3
            heightNode = radius * 0.8
            # 坐标
            prex1, prey1 = (d.nodex[nodei].value + radius * math.cos(math.pi / 4),
                            d.nodey[nodei].value + radius * math.sin(math.pi / 4))
            prex2, prey2 = (prex1 + 100 * math.cos(math.pi / 4),
                            prey1 + 100 * math.sin(math.pi / 4))
            prex3, prey3 = prex2, prey2 + boxh
            prex4, prey4 = prex2 + boxw, prey2
            pointPre1, pointPre2, pointPre3, pointPre4 = (APoint(prex1, prey1),
                                                          APoint(prex2, prey2),
                                                          APoint(prex3, prey3),
                                                          APoint(prex4, prey4))
            # 连斜线
            linePre1 = acad.model.AddLine(pointPre1, pointPre2)
            # 连水平线并偏移三次，向上移动每次50
            linePre2 = acad.model.AddLine(pointPre2, pointPre4)
            prex30, prey30 = prex2, prey2 + unith
            prex31, prey31 = prex2, prey2 + unith * 2
            pointPre30, pointPre31 = APoint(
                prex30, prey30), APoint(prex31, prey31)
            off1_linePre2 = linePre2.Copy()
            off1_linePre2.Move(pointPre2, pointPre3)  # 最下边一根线
            off2_linePre2 = linePre2.Copy()
            off2_linePre2.Move(pointPre2, pointPre30)  # 中间一根线
            off3_linePre2 = linePre2.Copy()
            off3_linePre2.Move(pointPre2, pointPre31)  # 最上边一根线
            # 连垂直线并偏移1次，向右移动130
            linePre3 = acad.model.AddLine(pointPre2, pointPre3)
            off1_linePre3 = linePre3.Copy()
            off1_linePre3.Move(pointPre2, pointPre4)

            # 标注标高，两位小数 放在prex2、prex4之间
            strHeight = '{:.2f}'.format(d.nodeheight[nodei].value)
            insertHeight = APoint(prex2 + boxw / 2, prey2)  # 直线中点
            textObjHeight = acad.model.AddText(
                strHeight, insertHeight, heightNode)
            textObjHeight.Alignment = 13  # bottomcenter对齐
            textObjHeight.TextAlignmentPoint = insertHeight

            # 标注自由水头，两位小数 放在prex30直线的中点上
            strPre = '{:.2f}'.format(d.nodepre[nodei].value)
            insertPre = APoint(prex30 + boxw / 2, prey30)  # 直线中点
            textObjPre = acad.model.AddText(strPre, insertPre, heightNode)
            textObjPre.Alignment = 13  # bottomcenter对齐
            textObjPre.TextAlignmentPoint = insertPre
            # 标注总水头，两位小数 放在prex31直线的中点上
            strHp = '{:.2f}'.format(d.nodehp[nodei].value)
            insertHp = APoint(prex31 + boxw / 2, prey31)  # 直线中点
            textObjHp = acad.model.AddText(strHp, insertHp, heightNode)
            textObjHp.Alignment = 13  # bottomcenter对齐
            textObjHp.TextAlignmentPoint = insertHp
        else:
            pass


def plot(acad, dir, d, radius=50, distance=185, box=[140, 180]):
    """
    绘制图形及标注
    acad即cad对象
    dir为当前背景图图名
    d为data数据
    radius为节点圆的半径，默认为50
    distance为节点编号至节点流量直接的距离，默认为185
    box为画节点压力标注的总长和总宽，box[1]最好为三的整数倍
    """
    # 背景图确定
    acad.ActiveDocument.Application.Documents(dir).Activate()

    # %% 绘制节点：包含了水厂节点
    # 图层：“节点”、粉红、线宽默认长度
    LayerObj1 = layer(acad, "节点", color=30, Lineweight=13)  # 颜色为橘黄,线宽为13即0.13
    acad.ActiveDocument.ActiveLayer = LayerObj1  # 将图层设置为当前图层
    # 文字标注
    txtStyleObj1 = textStyle(acad, StyleName="节点仿宋", FontName="仿宋", Width=0.75)
    # 算法1
    plot1(acad, d, radius=radius)

    # %% 绘制管段：注意水厂节点可能会搜不到坐标
    # 图层：“管段”、蓝色、线宽0.70
    LayerObj2 = layer(acad, "管段", color=4, Lineweight=70)  # 颜色为蓝,线宽为0.70mm
    acad.ActiveDocument.ActiveLayer = LayerObj2  # 将图层设置为当前图层
    # 画线：外循环遍历管段，内循环遍历上下游节点，连接节点直线
    plot2(acad, d, radius=radius)

    # %% 管段文字标注
    # 建立图层：“标注”、青色、线宽默认长度
    LayerObj3 = layer(acad, "上管段标注", 93, 13)  # 颜色为青,13为0.13
    LayerObj6 = layer(acad, "下管段标注", 93, 13)  # 颜色为青,13为0.13
    # 文字样式
    txtStyleObj2 = textStyle(acad, StyleName="管段仿宋", FontName="仿宋", Width=0.75)
    # 管段数据标注 ：
    plot3(acad, d, radius=radius, layerUP=LayerObj3, layerDOWM=LayerObj6)

    # %% 节点流量标注
    # 建立图层
    LayerObj4 = layer(acad, "节点流量", 40, 13)  # 颜色为淡黄,13为0.13
    acad.ActiveDocument.ActiveLayer = LayerObj4  # 将图层设置为当前图层。
    # 文字样式：设为节点仿宋，即txtStyleObj1
    acad.ActiveDocument.ActiveTextStyle = acad.ActiveDocument.TextStyles.Item("节点仿宋")
    plot4(acad, d, radius=radius, distance=distance)

    # %% 节点水头标注
    # 建立图层
    LayerObj5 = layer(acad, "节点压力", 6, 13)  # 颜色为洋红,13为0.13
    acad.ActiveDocument.ActiveLayer = LayerObj5  # 将图层设置为当前图层。
    # 文字样式：设为节点仿宋，即txtStyleObj1
    acad.ActiveDocument.ActiveTextStyle = acad.ActiveDocument.TextStyles.Item("节点仿宋")
    # 画线
    plot5(acad, d, radius=radius, box=box)
