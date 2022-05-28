function out=contourMap(dirin,dirout,levels,box,outsheet,partten)
% dirin 为输入文件excel的绝对地址
% dirout 为输出文件的绝对路径
% levels 为1*3的矩阵：
%        levels(1,1)是压力范围的最小值；
%        levels(1,2)是压力变化的梯度；
%        levels(1,3)是压力范围的最大值。
% box 为2*3的矩阵：
%        box(1,1)是绘制等压线的x坐标最小值
%        box(1,2)是x坐标的插值点数
%        box(1,3)是绘制等压线的x坐标最大值
%        box(2,1:end)即为y坐标的
% outsheet 为输出到第几个sheet里
% partten 为判断是高程线还是等水压线

% test:在命令行窗口输入以下语句
% contourMap('','',15,60,1[,0])
if(~exist('partten','var'))
    partten = 0;  % 如果未出现该变量，则对其进行赋值
end
A=xlsread(dirin,'sheet1');
% 算法
q=A(:,end-6);
x=A(q>0,end-1);y=A(q>0,end);p=A(q>0,end-2);% 排除水厂节点
height=A(q>0,end-8); %记录高程值
xi=linspace(box(1,1),box(1,3),box(1,2));
yi=linspace(box(2,1),box(2,3),box(2,2));
[xi,yi]=meshgrid(xi,yi);
if partten==0
    zi=griddata(x,y,p,xi,yi,'cubic');
else
    zi=griddata(x,y,height,xi,yi,'cubic');
end
level=levels(1):levels(2):levels(3);
[C,h]=contour(xi,yi,zi,level);
clabel(C,h);
% 导出数据
str1='A1:B';str2=int2str(size(C,2));
strout=strcat(str1,str2);
sheet1='Sheet';sheet2=int2str(outsheet);
sheetout=strcat(sheet1,sheet2);
xlswrite(dirout,C.',sheetout,strout);

