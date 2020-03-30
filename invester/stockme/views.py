from django.shortcuts import render
from django.http import HttpResponse
from . import stock
import json
# Create your views here.
def index(request):
    s = stock.bestpoints('nifty')
    return  HttpResponse(s)

def actual_data(request):
    close, time = stock.get_today_df('nifty')
    mydict = {
        "close":close,
        "time" :time
    }
    return HttpResponse(json.dumps(mydict))