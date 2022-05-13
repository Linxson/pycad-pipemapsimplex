function out=contourMap(dirin,dirout,minlevel,maxlevel,outsheet,partten)
% dirin Ϊ�����ļ�excel�ľ��Ե�ַ
% dirout Ϊ����ļ��ľ���·��
% minlevel Ϊlevel����Сֵ,maxlevel��֮,����Ϊ15-60���߳�Ϊ-5-50
% outsheet Ϊ������ڼ���sheet��
% partten Ϊ�ж��Ǹ߳��߻��ǵ�ˮѹ��
% test:�������д��������������
% contourMap('','',15,60,1[,0])
if(~exist('partten','var'))
    partten = 0;  % ���δ���ָñ������������и�ֵ
end
A=xlsread(dirin,'sheet1');
% �㷨
q=A(:,3);
x=A(q>0,8);y=A(q>0,9);p=A(q>0,7);% �ų�ˮ���ڵ�
height=A(q>0,1); %��¼�߳�ֵ
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
% ��������
str1='A1:B';str2=int2str(size(C,2));
strout=strcat(str1,str2);
sheet1='Sheet';sheet2=int2str(outsheet);
sheetout=strcat(sheet1,sheet2);
xlswrite(dirout,C.',sheetout,strout);

