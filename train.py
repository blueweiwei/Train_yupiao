#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  train.py
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

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) A'
                  'ppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
}

def getLocalTime():
    timeStamp = int(time.time())
    timeArray = time.localtime(timeStamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

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

def search(departureStation,arrivalStation,dateTime):
    url='https://i.meituan.com/uts/train/train/querytripnew?fromPC=1' \
        '&train_source=meituanpc@wap&uuid=a2bab8b38b364d7f8d7a.1590661315.1.0.0' \
        '&from_station_telecode={}&to_station_telecode={}&yupiaoThreshold=0&start_date={}' \
        '&isStudentBuying=false'.format(getStation(departureStation), getStation(arrivalStation), dateTime)
    response=requests.get(url,headers=headers).json()
    print('当前时间为：'+getLocalTime()+'\n火车查询区间--始发站：'+departureStation+'终点站'+arrivalStation+'\n')
    for train in response['data']['trains']:
        # print(train)
        print('车次号:'+train['full_train_code'] + '     出发时间:' + train['start_time'] + '     到达时间:' + train['arrive_time'] + '     耗时:' +train['run_time'] + '     出发站:' + train['from_station_name'] + '     终点站:' + train['to_station_name'])
        seats_info = ''
        for seats in train['seats']:
            seats_info += str(seats['seat_type_name'])+'--'
            seats_info += str(seats['seat_min_price'])+'元--'
            seats_info += str(seats['seat_yupiao'])
            seats_info += '张      '
        print('票价信息:   ' + seats_info+'\n')
    return '所有车票信息打印完毕'


if __name__ == '__main__':
    # print(getLocalTime())
   print(search('安阳','郑州','2021-02-28'))
