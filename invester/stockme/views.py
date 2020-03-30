from django.shortcuts import render
from os import listdir
from django.http import HttpResponse
from . import stock
import json
# Create your views here.
def index(request):
    company_names = listdir('./dataset')
    return  render(request,'index.html',{'company_names':company_names})


def invest(request):
    actual_points = stock.bestpoints('nifty')
    return render(request,'invest.html',actual_points)

def actual_data(request):
    close, time = stock.get_today_df('nifty')
    clor = '#3cba9f' if close[-1] > close[0] else '#FF6347'
    mydict = {
        "close":close,
        "time" :time
    }
    return render(request,'pie.html',{'labels': time,
        'data': close,'clr':clor})