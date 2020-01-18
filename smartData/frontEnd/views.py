#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
import tushare as ts
from django.shortcuts import render
from  django.http  import  JsonResponse
#from django.shortcuts import render_to_response

import pandas as pd

def hello(request):
    ts.set_token('5bc67278bb0450c5077b5deca6277ebb5171e9f97507d1c588560979')
    pro = ts.pro_api()
    if request.method == 'POST':
        ts_code = request.POST.get('ts_code')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        df = pro.index_daily(ts_code=ts_code, start_date= startDate, end_date=endDate,
                             fields='trade_date,open,close,low,high,vol')
        mydata = df.values.tolist()
        for i in range(len(mydata)):
            mydata[i][0] = int(mydata[i][0])
        mydata.reverse()
        print(startDate)
        print(endDate)
        print(mydata)
        return JsonResponse({'newData': mydata})

    df = pro.index_daily(ts_code='000001.SH', start_date='20190101', end_date='datetime.datetime.now()',
                         fields='trade_date,open,close,low,high,vol')
    #df = pro.monthly(ts_code='000001.SH', start_date='20000101', end_date='datetime.datetime.now()')
    #df = pro.monthly(ts_code='000001.SH', start_date='20180101', end_date='20181101',fields='trade_date,open,high,low,close,vol,amount')
    #print(df)
    mydata = df.values.tolist()
    for i in range(len(mydata)):
        mydata[i][0] = int(mydata[i][0])
    mydata.reverse()
     #   print(type(mydata[i][0]))
#    for indexs in df.index:
#        print(df.loc[indexs].values[0:-1])
#        mydata.append(df.loc[indexs].values[0:-1])
    return render(request, "main.html", {'stockData': mydata})
    #return render(request, "index.html", {'stockData': json.dumps(mydata)})
    #return HttpResponse()
    # return render_to_response("index.html", {'stockData': mydata}, context_instance=RequestContext(request))


def test(request):
    if request.method == 'POST':
        i1 = request.POST.get('i1')
        i2 = request.POST.get('i2')
        i1 = int(i1)
        i2 = int(i2)
        res = i1 + i2
        return HttpResponse(res)
    return render(request, 'main.html')