# -*- coding: utf-8 -*-
data = {"name":"\u82b7\u951a\u6e7e","data":[[1563033600000,72],[1563037200000,63],[1563040800000,58],[1563044400000,59],[1563048000000,62],[1563051600000,66],[1563055200000,67],[1563058800000,65],[1563062400000,66],[1563066000000,73],[1563069600000,87],[1563073200000,99],[1563076800000,109],[1563080400000,119],[1563084000000,132],[1563087600000,146],[1563091200000,157],[1563094800000,160],[1563098400000,157],[1563102000000,145],[1563105600000,127],[1563109200000,108],[1563112800000,96],[1563116400000,89]]}
data_list = data.get('data')
# print(data_list)
sep = int((data_list[-1][0]-data_list[0][0])/24)
print(sep)
a = data_list[0][0]
b = data_list[-1][0]
print(a,b,sep)
y_list = []
# for i in range(a,b,sep):
#     # print(i)
for data in data_list:
    # if data[0]==i:
    print(data[0])
    y_list.append(data[1])

print(y_list, len(y_list))
file_name = '芷锚湾2019-07-14'
import numpy as np
# 实现插值的模块
from scipy import interpolate
#画图的模块
import matplotlib.pyplot as plt
import matplotlib
from pylab import *
#引入相关模块
import requests
import re
import json
import os
import datetime
import time

def mtplb(y_list,file_name):

    # y 表示纵轴，水位
    y = np.array(y_list)
    # x是一个横轴，时间（类似时间），从0 到数据端点，间隔为6，表示小时
    x_end_point  = len(y_list)*6
    x = np.array([num for num in range(0,x_end_point,6)])

    # 插值法之后的x轴值，表示从0 到 数据端点，每个数据间插入5个值，得出每十分钟
    xnew = np.arange(0, x_end_point-6, 1)

    """
    kind方法：
    nearest、zero、slinear、quadratic、cubic
    实现函数func
    """
    func = interpolate.interp1d(x, y, kind='cubic')
    # 利用xnew和func函数生成ynew，xnew的数量等于ynew数量
    ynew = func(xnew)
    f = open('{}-plot-tide.txt'.format(file_name),'w+')
    for i in ynew:
        f.write(format(i,'0.2f')+'\n')
    # print(type(ynew))
    f.close()
    print('文件已写入{}-plot-tide.txt'.format(file_name))
    # 画图部分
    figsize = 14,6
    figure, ax = plt.subplots(figsize = figsize)
    zhfont1 = matplotlib.font_manager.FontProperties(fname='SimHei.ttf')
    plt.title('{} 潮汐表(24h)'.format(file_name), fontproperties=zhfont1)
    plt.xlabel('时刻（h）',fontproperties=zhfont1)
    plt.ylabel('潮高（cm）', fontproperties=zhfont1)
    plt.tick_params(labelsize=8)

    #网格
    plt.subplots_adjust(left=0.06,right=1.0, top=0.9, bottom=0.1)
    # 原图

    plt.plot(x, y, color='g', marker='',label=u"Per 1 hour line")
    # 拟合之后的平滑曲线图
    # plt.subplot(2,1,1)
    plt.plot(xnew, ynew, '.-', color = 'r' ,label=u"Graph per 10 minutes")

    # plt.xticks(,[r'$00:00$'])
    plt.xticks([num for num in range(0, x_end_point,6)],[r'$00:00$',r'$01:00$',r'$02:00$',r'$03:00$',r'$04:00$',r'$05:00$',r'$06:00$',r'$07:00$',r'$08:00$',r'$09:00$',r'$10:00$',r'$11:00$',r'$12:00$',r'$13:00$',r'$14:00$',r'$15:00$',r'$16:00$',r'$17:00$',r'$18:00$',r'$19:00$',r'$20:00$',r'$21:00$',r'$22:00$',r'$23:00$',],)


    plt.legend(loc='upper left')
    plt.grid(True)
    plt.savefig('{}.png'.format(file_name))
    plt.show()


def get_t_file(filename):
    f = open('{}-plot-tide.txt'.format(filename))
    list_data = f.readlines()
    time_str = '{} 00:00'.format(filename[-10:])
    # print(time_str)

    time_tim = datetime.datetime.strptime(time_str,'%Y-%m-%d %H:%M')

    # print(time_tim)
    f_t = open('{}.t'.format(filename),'w+')
    f_tid = open('{}.tid'.format(filename),'w+')
    f_early_eight_tid = open('{}-eight.tid'.format(filename), 'w+')
    f_early_eight_tid.write('--------\n')
    for data in list_data:
        time_w = datetime.datetime.strftime(time_tim,'%H:%M')
        tide = format(eval(data)/100,'0.2f')
        f_t.write('"{}",{}\n'.format(time_w, tide))

        tide_w = '{:0>3d}'.format(int(eval(data)))
        f_tid.write('{day}.{moth}.{year} {time}:00 {tied}\n'.format(day = filename[-2:],moth = filename[-5:-3],year = filename[-10:-6],time = time_w,tied =tide_w ))
        time_eight=time_tim - datetime.timedelta(hours=8)

        f_early_eight_tid.write('{year}/{moth}/{day} {hour}:{minutes}:{sec} {tide}\n'.format(year = time_eight.year, moth=time_eight.month, day=time_eight.day, hour=time_eight.hour, minutes=str(time_eight.minute).zfill(2),sec=str(time_eight.second).zfill(2), tide = tide))
        time_tim = time_tim +datetime.timedelta(minutes = 10)
    f_t.close()
    f_tid.close()
    print('{}.t 已写入'.format(filename))
    print('{}.tid 已写入'.format(filename))
    print('{}-eight.tid 已写入'.format(filename))

mtplb(y_list,file_name)
get_t_file(file_name)