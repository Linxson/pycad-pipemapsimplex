# -*- coding: utf-8 -*-
"""
    =============================
    Author: Linxson
    E-mail: 1853299@tongji.edu.cn
    =============================
"""

from pyautocad import APoint,aDouble
import math


def plot(acad, dir, d):
    # 背景图确定
    acad.ActiveDocument.Application.Documents(dir).Activate()

    # %% 绘制节点：包含了水厂节点
    # 图层：“节点”、粉红、线宽默认长度
    LayerObj1 = acad.ActiveDocument.Layers.Add("节点")  # 添加新图层
    acad.ActiveDocument.ActiveLayer = LayerObj1  # 将图层设置为当前图层。
    LayerObj1.color = 30  # 设置颜色，颜色为橘黄
    LayerObj1.Lineweight = 13  # 设置线宽，13为0.13

    # 文字标注
    txtStyleObj1 = acad.ActiveDocument.TextStyles.add("节点仿宋")
    acad.ActiveDocument.ActiveTextStyle = acad.ActiveDocument.TextStyles.Item(
        "节点仿宋")
    acad.ActiveDocument.ActiveTextStyle.SetFont("仿宋", False, False, 1, 0 or 0)
    txtStyleObj1.Width = 0.75  # 宽度0.75

    # 算法
    for nodei in range(1, d.nodeTotal):
        # 画圆：根据坐标以半径画圆
        center = APoint(d.nodex[nodei].value, d.nodey[nodei].value)
        radius = 50
        circleObj = acad.model.AddCircle(center, radius)
        # 节点标注
        textStrNode = d.nodeId[nodei].value[-3:]  # 取节点ID的后三位
        insertPntNode = APoint(d.nodex[nodei].value, d.nodey[nodei].value)
        heightNode = 40
        textObjNode = acad.model.AddText(
            textStrNode, insertPntNode, heightNode)
        textObjNode.Alignment = 4  # middle对齐
        textObjNode.TextAlignmentPoint = insertPntNode

    # %% 绘制管段：注意水厂节点可能会搜不到坐标
    # 图层：“管段”、蓝色、线宽0.70
    LayerObj2 = acad.ActiveDocument.Layers.Add("管段")  # 添加新图层
    acad.ActiveDocument.ActiveLayer = LayerObj2  # 将图层设置为当前图层。
    LayerObj2.color = 4  # 设置颜色，颜色为青
    LayerObj2.Lineweight = 70  # 设置线宽，0.70mm

    # 画线：外循环遍历管段，内循环遍历上下游节点，连接节点直线
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
        temp_startx, temp_starty = d.nodex[starti].value, d.nodey[starti].value
        temp_endx, temp_endy = d.nodex[endi].value, d.nodey[endi].value
        angle = math.atan2(d.nodey[endi].value-d.nodey[starti].value,
                           d.nodex[endi].value-d.nodex[starti].value)
        temp_startx = d.nodex[starti].value + abs(radius*math.cos(
            angle)) if d.nodex[starti].value < d.nodex[endi].value else \
            d.nodex[starti].value-abs(radius*math.cos(angle))
        temp_endx = d.nodex[endi].value+abs(radius*math.cos(
            angle)) if d.nodex[starti].value > d.nodex[endi].value else \
            d.nodex[endi].value-abs(radius*math.cos(angle))
        temp_starty = d.nodey[starti].value+abs(radius*math.sin(
            angle)) if d.nodey[starti].value < d.nodey[endi].value else \
            d.nodey[starti].value-abs(radius*math.sin(angle))
        temp_endy = d.nodey[endi].value+abs(radius*math.sin(
            angle)) if d.nodey[starti].value > d.nodey[endi].value else \
            d.nodey[endi].value-abs(radius*math.sin(angle))

        # 水流方向：填充块，置于管段中点处，如果流量是正值，则从上游节点指向下游节点，反之
        xmid = (d.nodex[starti].value + d.nodex[endi].value) / 2
        ymid = (d.nodey[starti].value + d.nodey[endi].value) / 2
        lmid = 50
        if d.isclose[pipei].value != 'Closed':
            if d.q[pipei].value < 0:
                trix1 = xmid-lmid*math.cos(angle)
                triy1 = ymid-lmid*math.sin(angle)
                trix2 = trix1+2.0*lmid / \
                    math.cos(math.pi/12)*math.cos(angle+math.pi/12)
                triy2 = triy1+2.0*lmid / \
                    math.cos(math.pi/12)*math.sin(angle+math.pi/12)
                trix3 = trix1+2.0*lmid / \
                    math.cos(math.pi/12)*math.cos(angle-math.pi/12)
                triy3 = triy1+2.0*lmid / \
                    math.cos(math.pi/12)*math.sin(angle-math.pi/12)
            else:
                trix1 = xmid+lmid*math.cos(angle)
                triy1 = ymid+lmid*math.sin(angle)
                trix2 = trix1-2.0*lmid / \
                    math.cos(math.pi/12)*math.cos(angle+math.pi/12)
                triy2 = triy1-2.0*lmid / \
                    math.cos(math.pi/12)*math.sin(angle+math.pi/12)
                trix3 = trix1-2.0*lmid / \
                    math.cos(math.pi/12)*math.cos(angle-math.pi/12)
                triy3 = triy1-2.0*lmid / \
                    math.cos(math.pi/12)*math.sin(angle-math.pi/12)
            trpnt1, trpnt2, trpnt3 = (APoint(trix1, triy1), APoint(trix2, triy2),
                                      APoint(trix3, triy3))
            solidObj = acad.model.AddSolid(trpnt1, trpnt2, trpnt3, trpnt3)

        # 三点多段线
        startPoint = APoint(temp_startx, temp_starty)
        endPoint = APoint(temp_endx, temp_endy)
        midPoint=APoint(xmid,ymid)
        pntpolyline=[startPoint,midPoint,endPoint]
        pntpolyline=[j for i in pntpolyline for j in i]
        pntpolyline=aDouble(pntpolyline)
        acad.model.AddPolyLine(pntpolyline)

    # %% 管段文字标注
    # 建立图层：“标注”、青色、线宽默认长度
    LayerObj3 = acad.ActiveDocument.Layers.Add("上管段标注")  # 添加新图层
    LayerObj3.color = 93  # 设置颜色，颜色为青
    LayerObj3.Lineweight = 13  # 设置线宽，13为0.13

    LayerObj6 = acad.ActiveDocument.Layers.Add("下管段标注")  # 添加新图层
    LayerObj6.color = 93  # 设置颜色，颜色为青
    LayerObj6.Lineweight = 13  # 设置线宽，13为0.13
    # 文字样式
    txtStyleObj2 = acad.ActiveDocument.TextStyles.add("管段仿宋")
    acad.ActiveDocument.ActiveTextStyle = acad.ActiveDocument.TextStyles.Item(
        "管段仿宋")
    acad.ActiveDocument.ActiveTextStyle.SetFont("仿宋", False, False, 1, 0 or 0)
    txtStyleObj2.Width = 0.75  # 宽度0.75

    # 管段数据标注 ：
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
        xmid = (d.nodex[starti].value+d.nodex[endi].value)/2
        ymid = (d.nodey[starti].value+d.nodey[endi].value)/2
        angle = (math.atan2(d.nodey[endi].value-d.nodey[starti].value,
                            d.nodex[endi].value-d.nodex[starti].value))
        insertPntPipe = APoint(xmid, ymid)
        heightPipe = 40
        BasePointPipe = APoint(xmid, ymid)
        RotationAnglePipe = math.radians(angle*180/math.pi)

        # 画上管段：将图层设置为当前图层
        acad.ActiveDocument.ActiveLayer = LayerObj3
        # 标注1：在线的中点上方“[管段编号]-长度-管径”
        textStrPipe1 = ('['+d.pipeId[pipej].value[-3:]+']-' +
                        str(d.ln[pipej].value)+'-'+str(d.dn[pipej].value))
        textObjPipe1 = acad.model.AddText(
            textStrPipe1, insertPntPipe, heightPipe)
        textObjPipe1.Alignment = 13  # bottomcenter对齐
        textObjPipe1.TextAlignmentPoint = insertPntPipe
        textObjPipe1.Rotate(BasePointPipe, RotationAnglePipe)
        movx1 = xmid-30*math.sin(angle)
        movy1 = ymid+30*math.cos(angle)
        MovePointPipe1 = APoint(movx1, movy1)
        textObjPipe1.Move(BasePointPipe, MovePointPipe1)

        # 画下管段：将图层设置为当前图层
        acad.ActiveDocument.ActiveLayer = LayerObj6
        # 标注2：在线的中点下方“流量-流速-单位水损”,保留两位小数
        textStrPipe2 = '{:.2f}-{:.2f}-{:.2f}'.format(d.absq[pipej].value,
                                                     d.vn[pipej].value,
                                                     d.unithj[pipej].value)
        textObjPipe2 = acad.model.AddText(
            textStrPipe2, insertPntPipe, heightPipe)
        textObjPipe2.Alignment = 7  # topcenter对齐
        textObjPipe2.TextAlignmentPoint = insertPntPipe
        textObjPipe2.Rotate(BasePointPipe, RotationAnglePipe)
        movx2 = xmid+30*math.sin(angle)
        movy2 = ymid-30*math.cos(angle)
        MovePointPipe2 = APoint(movx2, movy2)
        textObjPipe2.Move(BasePointPipe, MovePointPipe2)
    # %% 节点流量标注
    # 建立图层
    LayerObj4 = acad.ActiveDocument.Layers.Add("节点流量")  # 添加新图层
    acad.ActiveDocument.ActiveLayer = LayerObj4  # 将图层设置为当前图层。
    LayerObj4.color = 40  # 设置颜色，颜色为淡黄
    LayerObj4.Lineweight = 13  # 设置线宽，13为0.13

    # 文字样式：设为节点仿宋，即txtStyleObj1
    acad.ActiveDocument.ActiveTextStyle = acad.ActiveDocument.TextStyles.Item(
        "节点仿宋")
    # 画圆
    distance = 185
    for nodei in range(1, d.nodeTotal):
        if d.nodeq[nodei].value != 0:
            centerNodexq = d.nodex[nodei].value-distance*math.cos(math.pi/4)
            centerNodeyq = d.nodey[nodei].value-distance*math.sin(math.pi/4)
            centerQ = APoint(centerNodexq, centerNodeyq)
            radiusQ = 60
            circleObjQ = acad.model.AddCircle(centerQ, radiusQ)
            # 标出流量数据
            textStrNodeQ = '{:.2f}'.format(d.nodeq[nodei].value)
            insertPntNodeQ = APoint(centerNodexq, centerNodeyq)
            heightNodeQ = 40
            textObjNodeQ = acad.model.AddText(textStrNodeQ, insertPntNodeQ, heightNodeQ)
            textObjNodeQ.Alignment = 4  # middle对齐
            textObjNodeQ.TextAlignmentPoint = insertPntNodeQ

            # 画直线：将直线头尾部分各减一个半径的距离，角度采用pi/4，长度用distance
            temp_startxQ, temp_startyQ = (centerNodexq+radiusQ*math.cos(math.pi/4),
                                          centerNodeyq+radiusQ*math.sin(math.pi/4))
            temp_endxQ, temp_endyQ = (d.nodex[nodei].value-radius*math.cos(math.pi/4),
                                      d.nodey[nodei].value-radius*math.sin(math.pi/4))
            startPointQ = APoint(temp_startxQ, temp_startyQ)
            endPointQ = APoint(temp_endxQ, temp_endyQ)
            lineObjQ = acad.model.AddLine(startPointQ, endPointQ)
            # 辅助线
            subq1x, subq1y = temp_startxQ+25 * \
                math.cos(75/180*math.pi), temp_startyQ + \
                25*math.sin(75/180*math.pi)
            subq2x, subq2y = temp_startxQ+25 * \
                math.cos(15/180*math.pi), temp_startyQ + \
                25*math.sin(15/180*math.pi)
            endPointQsub1 = APoint(subq1x, subq1y)
            endPointQsub2 = APoint(subq2x, subq2y)
            lineObjQsub1 = acad.model.AddLine(startPointQ, endPointQsub1)
            lineObjQsub2 = acad.model.AddLine(startPointQ, endPointQsub2)
        else:
            pass
    # %% 节点水头标注
    # 建立图层
    LayerObj5 = acad.ActiveDocument.Layers.Add("节点压力")  # 添加新图层
    acad.ActiveDocument.ActiveLayer = LayerObj5  # 将图层设置为当前图层。
    LayerObj5.color = 6  # 设置颜色，颜色为洋红
    LayerObj5.Lineweight = 13  # 设置线宽，13为0.13

    # 文字样式：设为节点仿宋，即txtStyleObj1
    acad.ActiveDocument.ActiveTextStyle = acad.ActiveDocument.TextStyles.Item(
        "节点仿宋")
    # 画线
    for nodei in range(1, d.nodeTotal):
        if d.nodeq[nodei].value != 0:
            # 斜线：60度、长度100（不包括圆半径50）
            # 直线：长140，宽180，每格60
            boxw, boxh, unith = 140, 180, 60
            # 坐标
            prex1, prey1 = (d.nodex[nodei].value+radius*math.cos(math.pi/4),
                            d.nodey[nodei].value+radius*math.sin(math.pi/4))
            prex2, prey2 = (prex1+100*math.cos(math.pi/4),
                            prey1+100*math.sin(math.pi/4))
            prex3, prey3 = prex2, prey2+boxh
            prex4, prey4 = prex2+boxw, prey2
            pointPre1, pointPre2, pointPre3, pointPre4 = (APoint(prex1, prey1),
                                                          APoint(prex2, prey2),
                                                          APoint(prex3, prey3),
                                                          APoint(prex4, prey4))
            # 连斜线
            linePre1 = acad.model.AddLine(pointPre1, pointPre2)
            # 连水平线并偏移三次，向上移动每次50
            linePre2 = acad.model.AddLine(pointPre2, pointPre4)
            prex30, prey30 = prex2, prey2+unith
            prex31, prey31 = prex2, prey2+unith*2
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
            strHeight ='{:.2f}'.format(d.nodeheight[nodei].value)
            insertHeight = APoint(prex2+boxw/2, prey2)  # 直线中点
            textObjHeight = acad.model.AddText(
                strHeight, insertHeight, heightNode)
            textObjHeight.Alignment = 13  # bottomcenter对齐
            textObjHeight.TextAlignmentPoint = insertHeight

            # 标注自由水头，两位小数 放在prex30直线的中点上
            strPre = '{:.2f}'.format(d.nodepre[nodei].value)
            insertPre = APoint(prex30+boxw/2, prey30)  # 直线中点
            textObjPre = acad.model.AddText(strPre, insertPre, heightNode)
            textObjPre.Alignment = 13  # bottomcenter对齐
            textObjPre.TextAlignmentPoint = insertPre
            # 标注总水头，两位小数 放在prex31直线的中点上
            strHp = '{:.2f}'.format(d.nodehp[nodei].value)
            insertHp = APoint(prex31+boxw/2, prey31)  # 直线中点
            textObjHp = acad.model.AddText(strHp, insertHp, heightNode)
            textObjHp.Alignment = 13  # bottomcenter对齐
            textObjHp.TextAlignmentPoint = insertHp
        else:
            pass
