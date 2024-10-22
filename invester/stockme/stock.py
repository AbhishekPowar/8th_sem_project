import pandas as pd
from random import choice
from datetime import datetime
from matplotlib import pyplot as plt
import json
import pickle
# import pandas as pd
import matplotlib.dates as mdates
plt.style.use('seaborn-darkgrid')
inf = 99999999999999
ninf = -inf
mx = list()
mn = list()
short_not  = list()
DATASET = 'stockme/dataset'

def money(x,y,df):
    return round((df[x]-df[y]),2)
    return round(abs(df[y]-df[x]),2)

def gen_peaks(df):
    peak = dict()
    truf = dict()
    for k in df:
        cur = df.get(k)
        if (df.get(k - 1, inf) > cur < df.get(k + 1, inf)):
            truf[k] = cur
        if (df.get(k - 1, ninf) < cur > df.get(k + 1, ninf)):
            peak[k] = cur
    return peak, truf

def scatmake(df,plist):
    d = [None]* len(df)
    for k in plist:
        d[k] = df[k]
    return d



def graph(df,low,high,peak,truf,short=0,window = 30):
    global mx,mn

    if abs(high-low) >=window:
        pk = list(filter(lambda k: low <= k <= high, peak))
        tf = list(filter(lambda k: low <= k <= high, truf))
        x =  max(pk, key=peak.get,default=None)
        y =  min(tf, key=truf.get, default=None)
        if x !=None and y!=None:
            if short == 0:
                mx.append(x)
                mn.append(y)
                short_not.append(x<y)

            elif short == 1:
                if  x>y:
                    mx.append(x)
                    mn.append(y)
                    short_not.append(x < y)
            elif short == -1:
                if x < y:
                    mx.append(x)
                    mn.append(y)
                    short_not.append(x < y)

            s, b = (x, y) if x < y else (y, x)
            graph(df, low, s, peak, truf, short, window)
            graph(df, b, high, peak, truf, short, window)
            if x > y and short in [0,-1]:
                graph(df, s+1 , b-1 , peak, truf, -1, window)
            elif x < y :
                graph(df, s+1 , b-1 , peak, truf, 1, window)

def clean(s,today):
    today = str(today)
    year = int(today[0:4])
    month = int(today[4:6])
    day = int(today[6:])
    hour,minute,*second =s.split(':')
    if len(second) == 0:
        second.append(0)
    return datetime(year,month,day,int(hour),int(minute),int(second[0]))


def make_indexed_dict(close,time):
    idxtime = {}
    idxclose = {}
    for idx, tc in enumerate(zip(time, close)):
        idxtime[idx] = tc[0]
        idxclose[idx] = tc[1]
    return  idxclose,idxtime

def get_today_df(company_name='nifty',today = 20140505, prediction=False):
    # TEMP : checks whether data access if for predition or not
    # Old
    # if prediction:
    #     pred = 'Predictions'
    # else:
    #     pred = 'Test'

    if prediction:
        pred = '25Predictions'
    else:
        pred = '25'

    base = DATASET
    # old
    # path = base + f"""/{company_name}/{company_name}{pred}2.csv"""

    path = base + f"""/{company_name}/{company_name}{pred}.csv"""

    # path = base + f"""/{company_name}/{company_name}.csv"""

    data = pd.read_csv(path)
    # today = choice(list(set(data['date'])))
    flt = (data['date'] == today)
    todaydf = data.loc[flt]


    # todaydf =  data

    #TEMP : Making data accesible
    time = list(todaydf['time'])

    #Reformats data according to need
    if not prediction:
        time = todaydf['time'].apply(lambda x: clean(x, today))
        time = [ts.to_pydatetime().strftime('%H:%M') for ts in time]
    close = list(todaydf['close'])
    # if prediction:
    #     close = [float(i[1:-1]) for i in list(todaydf['close'])]
    return close,time, today

def get_all_actual(company_name='nifty'):
    base = DATASET
    path = base + f"""/{company_name}/{company_name}.csv"""
    data = pd.read_csv(path)
    step = 500
    close = list(data['close'])[::step]
    time = list(data['date'].apply(str)+ data['time'])[::step]
    time.sort()
    return  close, time

def matplot(df,time):
    global mx,mn
    plt.plot(time, df.values())
    plt.scatter(time,scatmake(df,mx),c='g')
    plt.scatter(time,scatmake(df,mn),c='r')
    plt.legend(['Stock','Sell','Buy'])
    plt.xlabel('Time')
    plt.ylabel('Stock price')
    plt.title('Hello')
    plt.gcf().autofmt_xdate()
    myFmt = mdates.DateFormatter('%H:%M')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.show()

def init_mxmn():
    global mx,mn,short_not
    mx = list()
    mn = list()
    short_not = list()

def idx_to_time(idxtime,idx):
    return idxtime[idx]



def bestpoints(company_name='nifty',want_to_short = 0,num_of_points = 3,window = 30,datePanel=20140505,pred=True):

    init_mxmn()
    global mx,mn
    close,time,today = get_today_df(company_name,datePanel,True)
    df, idxtime = make_indexed_dict(close,time)
    time = list(idxtime.values())

    peak,truf = gen_peaks(df)
    graph(df,0,len(df),peak,truf,want_to_short,window)
    mxmn = sorted(zip(mx,mn,short_not),key=lambda x:money(x[0],x[1],df),reverse=True)[:num_of_points]
    mx, mn ,sn= zip(*mxmn)

    dfO = df
    if pred:
        closeO, timeO, todayO = get_today_df(company_name, datePanel)
        dfO, idxtimeO = make_indexed_dict(closeO,timeO)

    # matplot(df,time)
    my_dict = dict()
    actual_invest_points = []
    for buy,sell,short in zip(mn,mx,sn):
        actual_invest_points.append({
            "Buy": idx_to_time(idxtime, buy)[:5],
            "Sell": idx_to_time(idxtime, sell)[:5],
            "Short": short,
            "Actual_money": money(sell, buy, dfO),
        })


    actual_invest_points.sort(key=lambda d:d['Actual_money'],reverse=True)
    my_dict["actual"] = actual_invest_points
    my_dict['today'] = today
    return my_dict

# import pickle
# import pandas as pd
def predictor(from_date,to_date):#enter date as yyyymmdd
    # file = input("Enter company name:")
    file = 'infosys'
    DATASET = 'dataset'
    loaded_model = pickle.load(open(f'{DATASET}/{file}/{file}LinearRegression.pickle', 'rb'))
    time_list=[916,917,918,919,920,921,922,923,924,925,926,927,928,929,930,931,932,933,934,935,936,937,938,939,940,941,942,943,944,945,946,947,948,949,950,951,952,953,954,955,956,957,958,959,1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019,1020,1021,1022,1023,1024,1025,1026,1027,1028,1029,1030,1031,1032,1033,1034,1035,1036,1037,1038,1039,1040,1041,1042,1043,1044,1045,1046,1047,1048,1049,1050,1051,1052,1053,1054,1055,1056,1057,1058,1059,1100,1101,1102,1103,1104,1105,1106,1107,1108,1109,1110,1111,1112,1113,1114,1115,1116,1117,1118,1119,1120,1121,1122,1123,1124,1125,1126,1127,1128,1129,1130,1131,1132,1133,1134,1135,1136,1137,1138,1139,1140,1141,1142,1143,1144,1145,1146,1147,1148,1149,1150,1151,1152,1153,1154,1155,1156,1157,1158,1159,1200,1201,1202,1203,1204,1205,1206,1207,1208,1209,1210,1211,1212,1213,1214,1215,1216,1217,1218,1219,1220,1221,1222,1223,1224,1225,1226,1227,1228,1229,1230,1231,1232,1233,1234,1235,1236,1237,1238,1239,1240,1241,1242,1243,1244,1245,1246,1247,1248,1249,1250,1251,1252,1253,1254,1255,1256,1257,1258,1259,1300,1301,1302,1303,1304,1305,1306,1307,1308,1309,1310,1311,1312,1313,1314,1315,1316,1317,1318,1319,1320,1321,1322,1323,1324,1325,1326,1327,1328,1329,1330,1331,1332,1333,1334,1335,1336,1337,1338,1339,1340,1341,1342,1343,1344,1345,1346,1347,1348,1349,1350,1351,1352,1353,1354,1355,1356,1357,1358,1359,1400,1401,1402,1403,1404,1405,1406,1407,1408,1409,1410,1411,1412,1413,1414,1415,1416,1417,1418,1419,1420,1421,1422,1423,1424,1425,1426,1427,1428,1429,1430,1431,1432,1433,1434,1435,1436,1437,1438,1439,1440,1441,1442,1443,1444,1445,1446,1447,1448,1449,1450,1451,1452,1453,1454,1455,1456,1457,1458,1459,1500,1501,1502,1503,1504,1505,1506,1507,1508,1509,1510,1511,1512,1513,1514,1515,1516,1517,1518,1519,1520,1521,1522,1523,1524,1525,1526,1527,1528,1529,1530,1531,1532,1533,1534,1535,1536,1537,1538,1539,1540,1541,1542,1543,1544,1545,1546,1547,1548,1549,1550,1551,1552,1553,1554,1555,1556,1557,1558,1559,1600]
    last_close = int(input("Enter previous day close value:"))
    cols = ['date','time','close']
    predictions = pd.DataFrame(columns = cols)
    for date in range(from_date,to_date):
        for time in time_list:
            last_close=loaded_model.predict([[date ,time,last_close]])
            predictions.loc[len(predictions)] = [date,time,last_close]
    return predictions

def allDates(company_name):
    pred = '25Predictions'
    base = DATASET
    path = base + f"""/{company_name}/{company_name}{pred}.csv"""
    # print(path)
    data = pd.read_csv(path)
    alllist = list(set(data['date']))
    alllist = list(map(str,alllist))
    alllist.sort()
    return  alllist

def buySell(cname,today,start,end):
    closeO, timeO, todayO = get_today_df(cname, today)
    dfO, idxtimeO = make_indexed_dict(closeO, timeO)

    try:
        mapinv = {}
        mapinv.update(zip(idxtimeO.values(), idxtimeO.keys()))
        buy, sell = mapinv[start], mapinv[end]
        return round(dfO[sell]-dfO[buy],2)
    except :
        return  'Time format error'




if __name__ == '__main__':
    # bestpoints('nifty',
    #            want_to_short=0,
    #            num_of_points=3,
    #            window=30)
    # c,t = get_today_df('tcs')
    # print(c,t)
    predictor(20150805,20150807)
    # from os import listdir
    # print(listdir('dataset'))

