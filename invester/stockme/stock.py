import pandas as pd
from random import choice
from datetime import datetime
from matplotlib import pyplot as plt
import json
import matplotlib.dates as mdates
plt.style.use('seaborn-darkgrid')
inf = 99999999999999
ninf = -inf
mx = list()
mn = list()
short_not  = list()

def money(x,y,df):
    return round(abs(df[x]-df[y]),2)

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

def get_today_df(company_name='nifty',today = 20140505):
    base = 'dataset'
    path = base + f"""/{company_name}/{company_name}.csv"""
    data = pd.read_csv(path)
    today = choice(list(set(data['date'])))
    flt = (data['date'] == today)
    todaydf = data.loc[flt]

    time = todaydf['time'].apply(lambda x:clean(x,today))
    time = [ts.to_pydatetime().strftime('%H:%M')   for ts in time]
    close = list(todaydf['close'])
    return close,time


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



def bestpoints(company_name='nifty',want_to_short = 0,num_of_points = 3,window = 30):

    init_mxmn()
    global mx,mn
    close,time = get_today_df(company_name,0)
    df, idxtime = make_indexed_dict(close,time)
    time = list(idxtime.values())

    peak,truf = gen_peaks(df)
    graph(df,0,len(df),peak,truf,want_to_short,window)
    mxmn = sorted(zip(mx,mn,short_not),key=lambda x:money(x[0],x[1],df),reverse=True)[:num_of_points]
    mx, mn ,sn= zip(*mxmn)

    # matplot(df,time)
    my_dict = dict()
    actual_invest_points = []
    for buy,sell,short in zip(mn,mx,sn):
        actual_invest_points.append( {
            "Buy": idx_to_time(idxtime,buy),
            "Sell":idx_to_time(idxtime,sell),
            "Short":short,
            "Actual_money": money(buy,sell,df),
        })
    my_dict["actual"] = actual_invest_points
    return my_dict

if __name__ == '__main__':
    bestpoints('nifty',
               want_to_short=0,
               num_of_points=3,
               window=30)
