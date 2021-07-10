# area-coordinate
判断一个坐标是否在一个固定区域内

# 1 区域的坐标
首先需要找出区域的坐标数据，N个坐标组成一个区域块。以json格式存储，如下：
[{"countryName":"XX村","position":"113.779861,23.117188","path":[[113.771358,23.130526],[113.770756,23.126405],[113.769062,23.126229],[113.768446,23.123569],[113.768753,23.119172],[113.76806,23.118747],[113.767983,23.117151],[113.768791,23.114526],[113.770062,23.114561],[113.770062,23.113603],[113.770793,23.113567],[113.77114,23.112042],[113.773296,23.112112],[113.773373,23.111473],[113.774604,23.111685],[113.774797,23.111118],[113.775259,23.111046],[113.775451,23.109769],[113.776336,23.109804],[113.776644,23.108385],[113.777683,23.108385],[113.77776,23.107711],[113.779067,23.107666],[113.779099,23.107677],[113.779335,23.107859],[113.779934,23.108148],[113.779934,23.108567],[113.780524,23.108534],[113.78077,23.108577],[113.78122,23.108619],[113.781316,23.108651],[113.781664,23.109188],[113.786871,23.118118],[113.787064,23.118418],[113.786912,23.118669],[113.787255,23.119012],[113.787383,23.119355],[113.787426,23.119784],[113.786826,23.120214],[113.786739,23.120543],[113.78685,23.120923],[113.787171,23.12166],[113.78752,23.124031],[113.787555,23.125108],[113.787898,23.125708],[113.787727,23.127598],[113.78792,23.128231],[113.786,23.128446],[113.780925,23.130776],[113.775659,23.131187]]}

# 2 核心代码
将N个坐标点连接形成一个区域，这里我是判断一个坐标点是否在该区域内。

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
    
# 2 坐标获取
对于坐标获取可以使用高德的API，https://restapi.amap.com/v3/place/text?parameters

