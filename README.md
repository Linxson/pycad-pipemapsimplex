# pycad-pipemapsimplex

通过python控制AutoCAD绘制市政管网平面图及三大工况图

# 一、需要外部库及数据来源

1. 主要：
    - pyautocad：绘图
    - openpyxl：传导数据
2. 次要：
    - ezdxf：文本替换
    - PyWin32：删除图层、导出pdf、数据转换
3. 数据来源：
    - Epanet 2.2 or WaterDesk：进行水力平差
    - arcgis：将dwg转换为shp文件导入平差软件作为背景图

# 二、运行环境

以下为本人运行代码的环境，仅做参考:

- Python 3.9
- Matlab 2018a
- Excel 2016
- AutoCAD 2018
- Anaconda 2.1.1

# 三、操作步骤

## 1. 数据导入

1. 将工况数据按文件`data/data_max.xlsx`的格式导入，其中:
    - 最高时最高日导入至`data_max`里
    - 消防工况导入至`data_fire`里
    - 意外事故工况数据导入至`data_acc`里
2. 背景图存放至`background.dwg`里
3. 运行`contour/contourPlot.m`文件，文件里的参数见`contour/contourMap.m`函数注释，生成的数据在`data/contourM.xlsx`文件里,其中：
    - `Sheet1`存放定线图高程数据
    - `Sheet2`存放最高时最高日节点压力数据
    - `Sheet3`存放消防工况节点压力数据
    - `Sheet4`存放意外事故工况节点压力数据

## 2. 绘制模板图

1. 打开背景图文件`background.dwg`
2. 打开Pycharm， 在python的编译配置中，working directory中的路径需落在pycad-pipemapsimplex

```python
import os

os.getcwd()
# 若输出类似于：'X:\\xxx\\pycad-pipemapsimplex'
# 即为成功
```

3. 分别在`src/main.py`里运行：

```python
test1_max()
test1_fire()
test1_acc()
test1_tmp()
```

4. 检查在路径`data\dxf`里是否出现：
   `test1_acc.dxf;test1_fire.dxf;test1_max.dxf;test1_tmp`四份文件，出现则意味成功

## 3. 手动修改tmp.dwg文件

1. 打开`test1_new.dwg`文件，对该文件做出以下修改：
    - [x] 移动双管：上下各偏移一定距离
    - [x] 折管：移动多段线的中点,把流向块等旋转移动
    - [x] 引线：对标注过于密集的管段使用引线，注意不要删除管段标注！
    - [x] 水厂、加压泵站：增加图例
    - [ ] Attention：不要删除任何一个text，如果报错`index list range error`，那么问题就大概率出在这里！
2. 修改好之后将`test1_new.dwg`另存为(通过AutoCAD)四份文件，分别命名为：
    - tmp_max.dxf、tmp_acc.dxf、tmp_fire.dxf、tmp_ali.dxf

## 4. 绘制工况图

1. 在`src/main`里运行`test2`函数
2. 运行成功后，分别将以下四份dxf文件转换为dwg文件(通过AutoCAD)：

> origin：tmp_max.dxf、tmp_acc.dxf、tmp_fire.dxf、tmp_ali.dxf
>
> ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
>
>  after：tmp_max.dwg、tmp_acc.dwg、tmp_fire.dwg、tmp_ali.dwg

3. 分别打开背景图文件：`tmp_max.dwg、tmp_acc.dwg、tmp_fire.dwg、tmp_ali.dwg`
4. 在`src/main.py`里分别运行：

```python
test3_max()
test3_fire()
test3_acc()
```

5. 到此为止，三张工况图已经基本画完了，检查`output/`文件夹里是否出现：
    - acc.dwg、fire.dwg、max.dwg

## 5. 绘制定线图

1. 打开背景图文件`tmp_ali.dwg`
2. 在`src/main`里运行`test4`函数
3. 检查`output/`文件夹里是否出现`ali.dwg`

## 6. 图纸输出

1. 修改双管上标注，*e.g.[280\281]-1000-100*
2. 填充水厂泵站节点，并为水厂节点命名，*e.g.山南水厂*
3. 删除等水压线多余的标注
4. 手动增加A1图框，然后将各节点的坐标记录下来
5. 打印出图

# 四、参考资料

1. [Python 二次开发 AutoCAD 简介](https://blog.csdn.net/hulunbuir/category_8525163.html) 作者：Hulunbuir
2. [335工作室 pythonCAD教程](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg2ODUzNTIwMA==&action=getalbum&album_id=1881779461612765186&scene=173&from_msgid=2247486513&from_itemidx=1&count=3&nolastread=1#wechat_redirect)
   作者：微信公众号(335工作室)
