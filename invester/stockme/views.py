from django.shortcuts import render
from os import listdir
from django.http import HttpResponse
from . import stock
import json
DATASET = 'stockme/dataset'
# Create your views here.
def index(request):
    company_names = listdir(DATASET)
    return  render(request,'index.html',{'company_names':company_names})


def invest(request):
    cname = request.GET.get('name')
    data = stock.bestpoints(cname)
    actual_points = data['actual']
    today = data['today']
    return render(request,'invest.html',{'actual': actual_points, 'today': today})


def today(request):
    cname = request.GET.get('name')
    close, time, today = stock.get_today_df(cname,20140505)
    data2, time2 , today= stock.get_today_df(cname,20140506)

    clor = '#3cba9f' if close[-1] > close[0] else '#FF0000'
    mydict = {
        "close":close,
        "time" :time
    }
    return render(request,'today.html',{'time': time,
        'actualdata': close,'clr':clor, 'prediction':data2})

def predict(request):
    cname = request.GET.get('name')
    close, time = stock.get_all_actual(cname)
    return render(request,'prediction.html',{'labels': time,
        'data': close,'clr':'#FF0000'})
