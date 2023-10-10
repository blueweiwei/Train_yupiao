#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  order.py
#  
#  Copyright 2021 ������ <������@DESKTOP-03B3450>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import requests
import json
import bs4
import time
import sys
import yaml
from email_sender import send_email

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) A'
                  'ppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
}
model="""
<div>
    <h1>您已开启了火车票预定提醒服务</h1>
    <p>查询当前时间为：{}</p>
    <p>列车车次为：{}</p>
    <p>发车时间：{} 到达时间：{}</p>
    <p>耗时：{}</p>
    <p>出发站：{}   终点站：{}</p>
    <p>座位类型：{} 单价：{}元  余票：{}张</p>
</div>
"""


# 读取yml配置
def getYmlConfig(yaml_file='./config.yml'):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    return dict(config)

# 获取当前时间
def getLocalTime():
    timeStamp = int(time.time())
    timeArray = time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

# 根据station字典获取车站名称
def getStation(name):
    station_name = {}
    name_station = {}
    f = open('./station.txt', encoding='utf-8')
    lines = f.readlines()
    f.close()
    for i in lines:
        temps = i.split(' ')
        station_name[temps[0]] = temps[1][:-1]
        name_station[temps[1][:-1]] = temps[0]
    return station_name[name]

# 消息通知
def sendMes(tomail,text):
    smtpCon=config['apis']['smtp']
    subject='--火车票余票通知--'
    send_email(tomail, subject, text, smtpCon)

# 接口查询车票信息
def search(departureStation,arrivalStation,dateTime,trainCode,seatTypeName):
    url='https://i.meituan.com/uts/train/train/querytripnew?fromPC=1' \
        '&train_source=meituanpc@wap&uuid=a2bab8b38b364d7f8d7a.1590661315.1.0.0' \
        '&from_station_telecode={}&to_station_telecode={}&yupiaoThreshold=0&start_date={}' \
        '&isStudentBuying=false'.format(getStation(departureStation), getStation(arrivalStation), dateTime)
    print(url)
    response=requests.get(url,headers=headers).json()
    # print('当前时间为：'+getLocalTime()+'\n火车查询区间--始发站：'+departureStation+'    终点站:'+arrivalStation+'\n预定车次为:'+trainCode)
    seats_info = {}
    for train in response['data']['trains']:
        if(train['full_train_code']==trainCode):
            print(train['seats'])
            for seats in train['seats']:
                seats_info['now_time']=getLocalTime()
                seats_info['train_code']=train['full_train_code']  
                seats_info['start_time'] =train['startDateTime']
                seats_info['arrive_time'] = train['arrive_time'] 
                seats_info['run_time'] =train['run_time'] 
                seats_info['from_station_name'] = train['from_station_name']  
                seats_info['to_station_name'] = train['to_station_name']
                if seats['seat_type_name']==seatTypeName and seats['seat_yupiao'] > config['users'][0]['user']['seat_yupiao'] :
                    seats_info['seat_type_name'] =seats['seat_type_name']
                    seats_info['seat_min_price']=seats['seat_min_price']
                    seats_info['seat_yupiao']=seats['seat_yupiao']
                    seats_info['mess']="true"
                    return seats_info
                else:
                    seats_info['mess']='false'
                    return seats_info
            break
            

# 全局配置
config = getYmlConfig(yaml_file='config.yml')

def getResult():
   user = config['users'][0]['user']
   full_train_code=user['full_train_code']
   trainDate=user['trainDate']
   from_station_name=user['from_station_name']
   to_station_name=user['to_station_name']
   seat_type_name=user['seat_type_name']
   return search(from_station_name,to_station_name,trainDate,full_train_code,seat_type_name)

if __name__ == '__main__':
    mes= getResult()
    email = config['users'][0]['user']['email']
    if mes['mess']=='true':
        text=model.format(mes['now_time'],mes['train_code'],mes['start_time'],mes['arrive_time'],mes['run_time'],mes['from_station_name'],mes['to_station_name'],mes['seat_type_name'],mes['seat_min_price'],mes['seat_yupiao'])
        sendMes(email,text)
        print('email send success !')
    else:
        print('当前火车车次余票未达到预期')