import pandas as pd
from random import choice
from random import randint
from itertools import accumulate
from datetime import datetime,time
from matplotlib import pyplot as plt
from matplotlib import dates
plt.style.use('seaborn-darkgrid')
inf = 99999999999999
ninf = -inf

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


mx = []
mn = []
short_not  = []
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

def clean(s):
    x,y =s.split(':')
    return datetime(1,1,1,int(x),int(y))

def bestpoints(filename='nifty.csv',want_to_short = 0,num_of_points = 3,window = 30):
    global mx,mn
    data = pd.read_csv(filename)
    today = choice(list(set(data['date'])))
    flt = (data['date'] == today)
    todaydf = data.loc[flt]


    time = todaydf['time'].apply(clean)
    close = list(todaydf['close'])
    idxtime = {}
    idxclose = {}
    for idx,tc in enumerate(zip(time,close)):
        idxtime[idx] = tc[0]
        idxclose[idx] = tc[1]
    df = idxclose





    # time = list(range(len(df)))
    plt.plot(time, df.values())

    peak,truf = gen_peaks(df)
    graph(df,0,len(df),peak,truf,want_to_short,window)
    mxmn = sorted(zip(mx,mn,short_not),key=lambda x:money(x[0],x[1],df),reverse=True)[:num_of_points]
    mx, mn ,sn= zip(*mxmn)
    plt.scatter(time,scatmake(df,mx),c='g')
    plt.scatter(time,scatmake(df,mn),c='r')
    plt.legend(['Stock','Sell','Buy'])
    plt.xlabel('Time')
    plt.ylabel('Stock price')
    plt.show()
    print('Point1,point2, isshort','money u made')
    for g,r,p in zip(mn,mx,sn):
        print(idxtime[g],idxtime[r],p,money(g,r,df))


if __name__ == '__main__':
    bestpoints('nifty.csv',
               want_to_short=1,
               num_of_points=4,
               window=1)