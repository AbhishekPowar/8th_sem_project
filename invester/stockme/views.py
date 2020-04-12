from django.shortcuts import render
from os import listdir
from django.http import HttpResponse
from . import stock
import json
DATASET = 'stockme/dataset'
# Create your views here.
def index(request):
    # company_names = listdir('./dataset')
    company_names = listdir(DATASET)
    return  render(request,'index.html',{'company_names':company_names})


def invest(request):
    cname = request.GET.get('name')
    actual_points = stock.bestpoints(cname)
    return render(request,'invest.html',actual_points)


def actual_data(request):
    close, time = stock.get_today_df('nifty')
    clor = '#3cba9f' if close[-1] > close[0] else '#FF0000'
    mydict = {
        "close":close,
        "time" :time
    }
    return render(request,'compare.html',{'labels': time,
        'data': close,'clr':clor})

def predict(request):
    cname = request.GET.get('name')
    close, time = stock.get_all_actual(cname)
    return render(request,'prediction.html',{'labels': time,
        'data': close,'clr':'#FF0000'})
