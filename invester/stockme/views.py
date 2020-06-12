from django.shortcuts import render
from os import listdir
from django.http import HttpResponse,JsonResponse
from . import stock
import json
DATASET = 'stockme/dataset'
# Create your views here.
def index(request):
    company_names = listdir(DATASET)
    return  render(request,'index.html',{'company_names':company_names})

def landingPage(request):
    company_names = listdir(DATASET)
    return  render(request,'landingPage.html',{'company_names':company_names})


def invest(request):
    short = request.GET.get('short',0)
    count = request.GET.get('count',3)
    timeWindow = request.GET.get('timeWindow',30)
    datePanel = request.GET.get('datePanel',20140505)
    datePanel = int(datePanel)
    print('view',datePanel)

    short = int(short)
    count = int(count)
    timeWindow = int(timeWindow)
    cname = 'tcs'
    data = stock.bestpoints(cname,short, count, timeWindow,datePanel)
    actual_points = data['actual']
    today = data['today']
    datajson =  {"actual": actual_points, "today": today}
    return JsonResponse(datajson)
    # return render(request,'invest.html',{'actual': actual_points, 'today': today})

# def money(t1,t2)

def today(request):
    cname = request.GET.get('name')
    cname = 'tcs'
    date = request.GET.get('today')
    date = int(date)
    print('date',date)
    # date = 20150721
    # date = 20150422
    close, time, todayActual = stock.get_today_df(cname,date)
    data2, time2 , todayPred= stock.get_today_df(cname,date,True)
    # step = 300
    # close = close[::step]
    # data2 = data2[::step]
    # time = time[::step]
    # time2 = time2[::step]
    # clor = '#3cba9f' if close[-1] > close[0] else '#FF0000'
    mydict = {
        "close":close,
        "time" :time
    }
    return JsonResponse({'labels':time,'data':close, 'predictionData': data2,'actDate': todayActual,'predDatee':todayPred})
    return render(request,'today.html',{'time': time,
        'actualdata': close,'clr':clor, 'prediction':data2})

def predict(request):
    cname = request.GET.get('name')
    close, time = stock.get_all_actual(cname)
    return render(request,'prediction.html',{'labels': time,
        'data': close,'clr':'#FF0000'})

def autoComplete(request):
    cname = request.GET.get('name')
    search = request.GET.get('search')

    cname = 'tcs'
    res = stock.allDates(cname)
    resdict = dict()
    for i in res:
        if search in i:
            resdict[i] = None
    resj = {
        'list':resdict
    }
    return JsonResponse(resj)

def money(request):
    cname = request.GET.get('cname','tcs')
    cname= 'tcs'
    start = request.GET.get('start')
    end = request.GET.get('end')
    today = request.GET.get('today')
    today = int(today)
    profit = stock.buySell(cname,today,start,end)
    return JsonResponse({'profit':profit})
    return JsonResponse({'profit':start+end+today})



