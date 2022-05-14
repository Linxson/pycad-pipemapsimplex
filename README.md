# pycad-pipemapsimplex
通过python控制Autocad绘制市政管网平面图及三大工况图
# 一、需要外部库
1. 主要：
    - pyautocad：绘图
    - openpyxl：传导数据
2. 次要：
    - ezdxf：文本替换
    - win32com：删除图层、导出pdf
    - pythoncom：数据转换
# 二、运行环境
以下为本人运行代码的环境，仅做参考
- Python 3.9
- Matlab 2018a
- Excel 2016
- Autocad 2018 
- Anaconda 2.1.1
# 三、使用说明
## 1. 数据导入
1. 将工况数据按`data/data_max.xlsx`的格式导入，其中最高时最高日导入至data_max里，消防工况导入至data_fire里，意外事故工况数据导入至data_acc里；
2. 运行`contour/contourPlot.m`文件，文件里的参数见`contour/contourMap.m`函数注释，生成的数据在`data/contourM.xlsx`文件里
## 2. 绘制模板图
1. 写在前面：
    - 运行代码前一定要把对于的背景图文件打开
    - `test1`目的是输出dxf文件，便于绘制工况图时进行文本替换
    - `test1`函数`func1()`目的是封装画图函数，便于直接调用
2. 在`src/main`里运行`test1`函数，其中内置函数`func1()`参数为：
    - `dir`是当前背景图的名词
    - `sht`为高程数据表`contourM.xlsx`的sheet
    - `outdir`为导出数据的路
    - `dxf`为导出格式内容，true导出为dxf格式，false则导出dwg格式 
## 3. 手动修改tmp.dwg文件
- [x] 移动双管：上下各偏移一定距离 
- [x] 折管：移动多段线的中点,把流向块等旋转移动
- [x] 引线：对标注过于密集的管段使用引线，注意不要删除管段标注！ 
- [x] 水厂、加压泵站：增加图例
- [ ] Attention：不要删除任何一个text，如果报错`index list range error`，那么问题就大概率出在这里！
## 4. 绘制定线图、工况图
1. 写在前面：
    - 手动修改好tmp文件后首先并将tmp文件导出为dxf文件
    - 导出的tmp.dxf文件为四份，分别作为`tmp_max、tmp_acc、tmp_fire、tmp_alignment`的背景图，放在`data/dxf`里
    - `test2`目的在于文本替换
    - `test3`目的在于绘制等水压线
    - `test4`目的在于删除最高时工况图上多余图层，作为定线图
2. 在`src/main`里运行`test2`函数，其中参数为：
    - `template`为模板函数，即各自的tmp
    - `dir`为待替换文本的文件，即各自的dxf
3. 运行`test2`之后会生成dxf文件，需要全部转换为dwg文件后再运行`test3`，其中`test3`参数与`test1`同理
4. 同理，打开对应的dwg文件后再运行`test4`
## 5. 图纸输出
1. 修改双管上标注,e.g.[280\281]-1000-100
2. 填充水厂泵站节点，并为水厂节点命名,e.g.山南水厂
3. 删除等水压线多余的标注
4. 手动增加A1图框，然后将各节点的坐标记录下来
5. 打印
# 四、参考资料
1. [Python 二次开发 AutoCAD 简介](https://blog.csdn.net/hulunbuir/category_8525163.html) 作者：Hulunbuir
2. [335工作室 pythonCAD教程](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=Mzg2ODUzNTIwMA==&action=getalbum&album_id=1881779461612765186&scene=173&from_msgid=2247486513&from_itemidx=1&count=3&nolastread=1#wechat_redirect) 作者：微信公众号(335工作室)
