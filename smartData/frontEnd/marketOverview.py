#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
import tushare as ts
from django.shortcuts import render
from  django.http  import  JsonResponse
from .models import *
import datetime
#from django.shortcuts import render_to_response
import numpy as np
import pandas as pd
import talib as ta
from talib import MA_Type

ts.set_token('abc23dc1908af03d82e14f830e52e28300ef5ac69bb5fe14e2ba8630')
pro = ts.pro_api()

def main(request):
    getLimitUp()
    return render(request, "marketOverview.html", {})

def getLimitUp():
    tradingCalendar = getTradingCalendar("20200701","20200711")
    for date in tradingCalendar:
        #dfUp = pro.limit_list(trade_date=date, limit_type='U')
        dfUp = pro.limit_list(trade_date=date[0], limit_type='U')
        dfDown = pro.limit_list(trade_date=date[0], limit_type='D')

        print(date)
        #print(dfUp.values.tolist())
        print(":涨停家数：")
        print(dfUp.shape[0])


def getTradingCalendar(startDate, endDate):
    df = pro.trade_cal(exchange='SSE', start_date=startDate, end_date=endDate)
    newdf = df[(df.is_open == 1)]
    newdf.drop(columns=['is_open', 'exchange'], inplace=True)
    datas = newdf.values.tolist()
    # print(datas)
    return datas