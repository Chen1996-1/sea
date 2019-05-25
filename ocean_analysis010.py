# -*- coding: utf-8 -*-
import numpy as np
# 实现插值的模块
from scipy import interpolate
# 画图的模块
import matplotlib.pyplot as plt
#引入相关模块
import requests
import re
import json
import os
import datetime

#setp one 获取港口信息
def get_dir_code(presentation_id):
	#定义一个字典用于存放港口名称与港口编号
    dir_code_port = {}
    # get 访问url,得到json 数据，其实就是字典
    url = 'http://oce.ckcest.cn/web/tide/site/querySite.do'
    form_data = {
    'areaid':presentation_id,
    'siteGroupID':3,

    }
    response = requests.post(url, form_data)
    # response 对象的 text 为字符串类型，通过eval()方法转为字典对象。
    data_list = eval(response.text)
    #拿到data
    # print(text)

	#获取 showname:code
    for data in data_list:
    	port_id = data['code']
    	port_name = data['name']
    	a = {port_name:port_id}
    	dir_code_port.update(a)
    	# print(name, name)
    print('okkk')
    #数据本地化，以后可以将以下部分改为存储数据库

    a=open('港口信息.txt','w+')
    a.write(str(dir_code_port))
    a.close()
    print('港口信息.txt 已写入')
    return dir_code_port



def get_ocean_json_data(data):
    url = 'http://oce.ckcest.cn/web/knowledge/tide/chaoxi/data/queryDetails.do'
    response = requests.post(url,data)
    text = response.text
    data_json = json.loads(text)
    # print(data_json)
    file_tile = data_json.get('fileinfo').get('Title')
    file_info = data_json.get('fileinfo')
    file_data = data_json.get('filedata')
    # print(file_data[0].get('Day'))

    date = '{}-{}-{}'.format(file_info.get('Year'),file_info.get('Month').zfill(2),str(file_data[0].get('Day')).zfill(2))

    file_name = file_tile+date
    f = open(file_name+'.txt','w+')
    for i in range(0,25):

        line_time = '{}\t{}:00\t'.format(date, str(i).zfill(2))
        line_tide = file_data[0].get('a'+str(i))
        line_write = line_time+str(line_tide)+'\n'
        f.writelines(line_write)
    f.close()
    print(file_name+'.txt 文件 okkk')
# 获取y_list return y_list
def get_flie_data(file_name):
    f = open(file_name+'.txt')
    x= f.readlines()
    y_list = []
    for i in x:
        a,b,c = i.split('\t')
        y = eval(c)
        if y != None:
            y_list.append(y)

    # print(y_list)
    return y_list


#求出拟合后的水位，yNew
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
    # 原图
    plt.plot(x, y, color='g', marker='',label=u"old")
    # 拟合之后的平滑曲线图
    plt.plot(xnew, ynew, color = 'r' ,label=u"thenew")


    plt.legend(loc='upper left')
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
        f_early_eight_tid.write('{year}/{moth}/{day} {hour}:{minutes}:{sec} {tide}/n'.format(year = time_eight.year, moth=time_eight.month, day=time_eight.day, hour=time_eight.hour, minutes=time_eight.minute,sec=time_eight.second, tide = tide))
        time_tim = time_tim +datetime.timedelta(minutes = 10)
    f_t.close()
    f_tid.close()
    print('{}.t okkk'.format(filename))
    print('{}.tid okkk'.format(filename))
#运行函数

def get_port_code_and_data_file():
    while True:
        f = open('港口信息.txt')
        dir_code = eval(f.read())
        f.close()
        print(str(dir_code.keys())[9:])
        name_port = input('请输入查询港口：')
        code = dir_code.get(name_port,'没找到输入的港口')
        if code == '没找到输入的港口':
            print(code)
        else:
            date = input('请输入查询日期：')
            data = {
                'PortCode':code,
                'Date':date,
                'Type':0,
            }
            get_ocean_json_data(data)
            file_name = name_port+date
            y_list = get_flie_data(file_name)
            mtplb(y_list, file_name)
            get_t_file(file_name)
            break


def awayls_do():
    while True:
        dict_presentations = {
        "福建":"5359678358229842731",
        "广西":"5181903535968969393",
        "广州":"5413705892610612211",
        "海南":"5625484080778443327",
        "河北":"4975833679728738945",
        "江苏":"5293027798039637126",
        "辽宁":"5432072060831556751",
        "山东":"5323306066487582247",
        "上海":"5653349478231077601",
        "台湾":"4876987809364790815",
        "天津":"4935741873097441187",
        "浙江":"4845586374601047334"
        }


        print(str(dict_presentations.keys())[9:])
        presentation_name = input('Put in name of presentation:')
        pres_id = dict_presentations[presentation_name]
        get_dir_code(pres_id)
        get_port_code_and_data_file()

awayls_do()