function out=contourMap(dirin,dirout,levels,box,outsheet,partten)
% dirin Ϊ�����ļ�excel�ľ��Ե�ַ
% dirout Ϊ����ļ��ľ���·��
% levels Ϊ1*3�ľ���
%        levels(1,1)��ѹ����Χ����Сֵ��
%        levels(1,2)��ѹ���仯���ݶȣ�
%        levels(1,3)��ѹ����Χ�����ֵ��
% box Ϊ2*3�ľ���
%        box(1,1)�ǻ��Ƶ�ѹ�ߵ�x������Сֵ
%        box(1,2)��x����Ĳ�ֵ����
%        box(1,3)�ǻ��Ƶ�ѹ�ߵ�x�������ֵ
%        box(2,1:end)��Ϊy�����
% outsheet Ϊ������ڼ���sheet��
% partten Ϊ�ж��Ǹ߳��߻��ǵ�ˮѹ��

% test:�������д��������������
% contourMap('','',15,60,1[,0])
if(~exist('partten','var'))
    partten = 0;  % ���δ���ָñ������������и�ֵ
end
A=xlsread(dirin,'sheet1');
% �㷨
q=A(:,end-6);
x=A(q>0,end-1);y=A(q>0,end);p=A(q>0,end-2);% �ų�ˮ���ڵ�
height=A(q>0,end-8); %��¼�߳�ֵ
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
% ��������
str1='A1:B';str2=int2str(size(C,2));
strout=strcat(str1,str2);
sheet1='Sheet';sheet2=int2str(outsheet);
sheetout=strcat(sheet1,sheet2);
xlswrite(dirout,C.',sheetout,strout);

