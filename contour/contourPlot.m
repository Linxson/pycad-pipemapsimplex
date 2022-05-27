clc;clear;close all;
% 数据
level=[15,5,60];
box=[20000,3000,35000;6000,3000,14000];
% 高程
contourMap('../data/data_max.xlsx',...
    '../data/contourM.xlsx',[-5,5,50],box,1,1);
% 等水压线
contourMap('../data/data_max.xlsx',...
    '../data/contourM.xlsx',level,box,2,0);
contourMap('../data/data_fire.xlsx',...
    '../data/contourM.xlsx',level,box,3,0);
contourMap('../data/data_acc.xlsx',...
    '../data/contourM.xlsx',level,box,4,0);