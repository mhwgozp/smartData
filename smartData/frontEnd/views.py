#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
import tushare as ts
from django.shortcuts import render
from  django.http  import  JsonResponse
from .models import *
#from django.shortcuts import render_to_response

import pandas as pd

def hello(request):
    ts.set_token('5bc67278bb0450c5077b5deca6277ebb5171e9f97507d1c588560979')
    pro = ts.pro_api()
    if request.method == 'POST':
        ts_code = request.POST.get('ts_code')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        showMacroData = request.POST.get('showMacroData')
        df = pro.index_daily(ts_code=ts_code, start_date= startDate, end_date=endDate,
                             fields='trade_date,open,close,low,high,vol')
        mydata = df.values.tolist()
        for i in range(len(mydata)):
            mydata[i][0] = int(mydata[i][0])
        mydata.reverse()
        print(showMacroData)
        if showMacroData == '1':
            macroData=[[20191101,100],[20191115,120],[20191128,110],[20191201,125],[20191210,100],[20191215,130],[2020105,132]]
        return JsonResponse({'newData': mydata, 'macroData':macroData})

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
    return render(request, "index.html", {'stockData': mydata})
    #return render(request, "index.html", {'stockData': json.dumps(mydata)})
    #return HttpResponse()
    # return render_to_response("index.html", {'stockData': mydata}, context_instance=RequestContext(request))

def getRR():
    items = ReserveRequirementManager.objects.all().order_by("-date")
    recordsNum = len(items)

    data = {}
    data["tableData"] = list(items.values())
    dataList = []
    for i in range(recordsNum):
        bigFinancialInstitutionsValue = data["tableData"][i]["bigFinancialInstitutionsValue"]
        smallMediumFinancialInstitutionsValue = data["tableData"][i]["smallMediumFinancialInstitutionsValue"]
        bigFinancialInstitutionsChange = 0
        smallMediumFinancialInstitutionsChange = 0
        if (i + 1) < recordsNum:
            bigFinancialInstitutionsChange = data["tableData"][i]["bigFinancialInstitutionsValue"] - data["tableData"][i+1]["bigFinancialInstitutionsValue"]
            smallMediumFinancialInstitutionsChange = data["tableData"][i]["smallMediumFinancialInstitutionsValue"] - \
                                             data["tableData"][i + 1]["smallMediumFinancialInstitutionsValue"]

        dataList.append([str(data["tableData"][i]["date"]), bigFinancialInstitutionsValue, bigFinancialInstitutionsChange, smallMediumFinancialInstitutionsValue, smallMediumFinancialInstitutionsChange, str(data["tableData"][i]["publicDate"])])
    return {'tableData': dataList, 'tableTitle': ["日期", "大型金融机构调整后值","大型金融机构调整幅度" "中小金融机构调整后", "中小金融机构调整幅度", "公布日期"]}

def getCpi():
    items = CpiManager.objects.all().order_by("-date")

    recordsNum = len(items)

    data = {}
    data["tableData"] = list(items.values())
    dataList = []
    for i in range(recordsNum):
        YOYIndex = i + 12
        YOY = -1
        if YOYIndex < recordsNum:
            newValue=data["tableData"][i]["value"]
            oldValue=data["tableData"][YOYIndex]["value"]
            YOY = format(round(((newValue - oldValue) / oldValue), 4), '.2%')
            # aaa=data["tableData"][i]["date"]
            # print(aaa)
            # print(newValue)
            # print(oldValue)
            # print(YOY)

        lRRIndex = i + 1
        linkRelativeRatio = -1
        if lRRIndex < recordsNum:
            newValue = data["tableData"][i]["value"]
            oldValue = data["tableData"][lRRIndex]["value"]
            linkRelativeRatio = format(round(((newValue - oldValue) / oldValue), 4), '.2%')

        month = data["tableData"][i]["date"].month
        accumulative = 0
        for j in range(month):
            if (i + j) < recordsNum:
                accumulative += data["tableData"][i + j]["value"]
            else:
                break;
        accumulative = round(accumulative / (j+1), 1)

        dataList.append(
            [str(data["tableData"][i]["date"]), data["tableData"][i]["value"], YOY, linkRelativeRatio, accumulative, str(data["tableData"][i]["publicDate"])])
    return {'tableData': dataList, 'tableTitle': ["日期", "CPI", "同比", "环比", "累积","公布日期"]}

def getPpi():
    items = PpiManager.objects.all().order_by("-date")

    recordsNum = len(items)

    data = {}
    data["tableData"] = list(items.values())
    dataList = []
    for i in range(recordsNum):
        YOYIndex = i + 12
        YOY = -1
        if YOYIndex < recordsNum:
            newValue=data["tableData"][i]["value"]
            oldValue=data["tableData"][YOYIndex]["value"]
            YOY = format(round(((newValue - oldValue) / oldValue), 4), '.2%')
            # aaa=data["tableData"][i]["date"]
            # print(aaa)
            # print(newValue)
            # print(oldValue)
            # print(YOY)

        lRRIndex = i + 1
        linkRelativeRatio = -1
        if lRRIndex < recordsNum:
            newValue = data["tableData"][i]["value"]
            oldValue = data["tableData"][lRRIndex]["value"]
            linkRelativeRatio = format(round(((newValue - oldValue) / oldValue), 4), '.2%')

        month = data["tableData"][i]["date"].month
        accumulative = 0
        for j in range(month):
            if (i + j) < recordsNum:
                accumulative += data["tableData"][i + j]["value"]
            else:
                break;
        accumulative = round(accumulative / (j+1), 1)

        dataList.append(
            [str(data["tableData"][i]["date"]), data["tableData"][i]["value"], YOY, linkRelativeRatio, accumulative, str(data["tableData"][i]["publicDate"])])
    return {'tableData': dataList, 'tableTitle': ["日期", "PPI", "同比", "环比", "累积","公布日期"]}

def getPmi():
    items = PmiManager.objects.all().order_by("-date")

    recordsNum = len(items)

    data = {}
    data["tableData"] = list(items.values())
    dataList = []

    for i in range(recordsNum):

        if (i + 1) < recordsNum:
            bigFinancialInstitutionsChange = data["tableData"][i]["bigFinancialInstitutionsValue"] - data["tableData"][i+1]["bigFinancialInstitutionsValue"]
            smallMediumFinancialInstitutionsChange = data["tableData"][i]["smallMediumFinancialInstitutionsValue"] - \
                                             data["tableData"][i + 1]["smallMediumFinancialInstitutionsValue"]

        dataList.append([str(data["tableData"][i]["date"]), bigFinancialInstitutionsValue, bigFinancialInstitutionsChange, smallMediumFinancialInstitutionsValue, smallMediumFinancialInstitutionsChange, str(data["tableData"][i]["publicDate"])])


    for i in range(recordsNum):
        manufacturingValue = data["tableData"][i]["manufacturingValue"]
        nonManufacturingValue = data["tableData"][i]["nonManufacturingValue"]

        YOYIndex = i + 12
        YOY_manufacturingValue = -1
        YOY_nonManufacturingValue = -1
        if YOYIndex < recordsNum:
            old_manufacturingValue=data["tableData"][YOYIndex]["manufacturingValue"]
            old_nonManufacturingValue=data["tableData"][YOYIndex]["nonManufacturingValue"]
            YOY_manufacturingValue = format(round(((manufacturingValue - old_manufacturingValue) / old_manufacturingValue), 4), '.2%')
            YOY_nonManufacturingValue = format(
                round(((nonManufacturingValue - old_nonManufacturingValue) / old_nonManufacturingValue), 4), '.2%')

        dataList.append(
            [str(data["tableData"][i]["date"]), manufacturingValue, YOY_manufacturingValue, nonManufacturingValue, YOY_nonManufacturingValue, str(data["tableData"][i]["publicDate"])])
    return {'tableData': dataList, 'tableTitle': ["日期", "制造业", "制造业同比","非制造业","非制造业同比","公布日期"]}

def dataManagerReserveRequirement(request):
    if request.method == 'POST':
        reserveRequirementManager = ReserveRequirementManager()
        reserveRequirementManager.date = request.POST.get('Date')
        reserveRequirementManager.bigFinancialInstitutionsValue = request.POST.get('BigFinancialInstitutionsValue')
        reserveRequirementManager.smallMediumFinancialInstitutionsValue = request.POST.get('SmallMediumFinancialInstitutionsValue')
        if "" !=request.POST.get('PublicDate'):
            reserveRequirementManager.publicDate = request.POST.get('PublicDate')

        reserveRequirementManager.save()
        return JsonResponse(getRR())
    #print(getCpi())
    return render(request, 'dataManagerRR.html', getRR())

def dataManagerCpi(request):
    if request.method == 'POST':
        cpiManager = CpiManager()
        cpiManager.date = request.POST.get('Date')
        cpiManager.value = request.POST.get('Value')
        if "" !=request.POST.get('PublicDate'):
            cpiManager.publicDate = request.POST.get('PublicDate')

        cpiManager.save()
        return JsonResponse(getCpi())
    #print(getCpi())
    return render(request, 'dataManagerCpi.html', getCpi())

def dataManagerPpi(request):
    if request.method == 'POST':
        ppiManager = PpiManager()
        ppiManager.date = request.POST.get('Date')
        ppiManager.value = request.POST.get('Value')
        if "" != request.POST.get('PublicDate'):
            ppiManager.publicDate = request.POST.get('PublicDate')

        ppiManager.save()

        return JsonResponse(getPpi())
    return render(request, 'dataManagerPpi.html', getPpi())

def dataManagerPmi(request):
    if request.method == 'POST':
        pmiManager = PmiManager()
        pmiManager.date = request.POST.get('Date')
        pmiManager.value = request.POST.get('Value')
        if "" != request.POST.get('PublicDate'):
            pmiManager.publicDate = request.POST.get('PublicDate')

        pmiManager.save()

        return JsonResponse(getPmi())
    return render(request, 'dataManagerPmi.html', getPmi())