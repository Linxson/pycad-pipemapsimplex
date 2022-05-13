function out=contourMap(dirin,dirout,minlevel,maxlevel,outsheet,partten)
% dirin 为输入文件excel的绝对地址
% dirout 为输出文件的绝对路径
% minlevel 为level的最小值,maxlevel反之,工况为15-60，高程为-5-50
% outsheet 为输出到第几个sheet里
% partten 为判断是高程线还是等水压线
% test:在命令行窗口输入以下语句
% contourMap('','',15,60,1[,0])
if(~exist('partten','var'))
    partten = 0;  % 如果未出现该变量，则对其进行赋值
end
A=xlsread(dirin,'sheet1');
% 算法
q=A(:,3);
x=A(q>0,8);y=A(q>0,9);p=A(q>0,7);% 排除水厂节点
height=A(q>0,1); %记录高程值
xi=linspace(20000,35000,3000);
yi=linspace(6000,14000,3000);
[xi,yi]=meshgrid(xi,yi);
if partten==0
    zi=griddata(x,y,p,xi,yi,'cubic');
else
    zi=griddata(x,y,height,xi,yi,'cubic');
end
level=minlevel:5:maxlevel;
[C,h]=contour(xi,yi,zi,level);
clabel(C,h);
% 导出数据
str1='A1:B';str2=int2str(size(C,2));
strout=strcat(str1,str2);
sheet1='Sheet';sheet2=int2str(outsheet);
sheetout=strcat(sheet1,sheet2);
xlswrite(dirout,C.',sheetout,strout);

