import json
import pandas as pd
import numpy as np
import os, sys

def rayCasting(p, poly):
    px = p['lng']
    py = p['lat']
    flag = False
 
    i = 0
    l = len(poly)
    j = l - 1
    while i < l:
        sx = poly[i]['lng']
        sy = poly[i]['lat']
        tx = poly[j]['lng']
        ty = poly[j]['lat']
        if (sx == px and sy == py) or (tx == px and ty == py):
            return (px, py)
        if (sy < py and ty >= py) or (sy >= py and ty < py):
            x = sx + (py - sy) * (tx - sx) / (ty - sy)
            if x == px:
                return (px,py)
            if x > px:
                flag = not flag
        j = i
        i += 1
    return (px,py) if flag else 'out'
 
def get_coordinate(a):
    coordinate = []
    for z in a:
        coordinate.append({'lng': float(z[0]),'lat': float(z[1])})
    return coordinate

def get_coordinate1(a):
    coordinate = []
    for z in list(a):
        coordinate.append({'lng': float(z[0]),'lat': float(z[1])})
    return coordinate

def rs(coordinate, shijiedata,data):
    zm = get_coordinate1(coordinate)
    for i,point in enumerate(zm): 
        if point['lng'] == 0:
            data['community'][i] = ''
        else:
            for community in shijiedata:
                shijiecommunity = community['path']   
                dbx = get_coordinate(shijiecommunity)
                count = 0    
                rs = rayCasting(point, dbx)
                if rs == 'out':
                    count += 1
                else:
                    data['community'][i] = community['countryName']
            if count == len(zm):
                print("no")
    return data

def find_community(data):
    data[['lng','lat']] = data[['lng','lat']].replace(np.nan,0)
    data['community'] = ''
    coordinate = data[['lng','lat']].values
    with open('../shijie.json','r',encoding='utf-8') as txt_file:
        contents = txt_file.read()
        shijiedata = json.loads(contents)       
    return rs(coordinate, shijiedata, data)

#if __name__ =='__main__':
#
#    data=pd.read_excel(r'C:\Users\yazce\Desktop\tts6.xlsx')
#    data[['lng','lat']] = data[['lng','lat']].replace(np.nan,0)
#    data['community'] = ''
#    coordinate = data[['lng','lat']].values
#    
#    with open('./shijie.json','r',encoding='utf-8') as txt_file:
#        contents = txt_file.read()
#        shijiedata = json.loads(contents)   
#    
#    dds = rs(coordinate, shijiedata)       
#    dds.to_excel(r'C:\Users\yazce\Desktop\tt24.xlsx')
