#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
import tushare as ts
from django.shortcuts import render
from  django.http  import  JsonResponse
from .models import *
import datetime
#from django.shortcuts import render_to_response

import pandas as pd

ts.set_token('abc23dc1908af03d82e14f830e52e28300ef5ac69bb5fe14e2ba8630')
pro = ts.pro_api()

def homePage(request):
    #return render(request, "test.html")

    if request.method == 'POST':
        #json.loads(request.POST.get('stockCodes'))
        indexCodes = request.POST.getlist('indexCodes')
        stockCodes = request.POST.getlist('stockCodes')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')
        macroParams=request.POST.getlist('macroParams')
        financialIndexParams=request.POST.getlist('financialIndexParams')
        datas = {'indexCodes':indexCodes,'stockCodes':stockCodes,'startDate':startDate,'macroParams':macroParams,'financialIndexParams':financialIndexParams,
                 'indexTradingDatas':{},'tradingDatas':{},'macroDatas':{},'financialIndexDatas':{},'tradingCalendarData':{}}
        indexTradingDatas = {}
        tradingDatas={}
        macroDatas={}
        numOfStockCodes = len(stockCodes)
        tradingCalendar = getTradingCalendar(startDate, endDate)

        for ts_code in indexCodes:
            indexDatas = getIndexOrStock('I', ts_code, startDate, endDate)
            indexTradingDatas[ts_code]=indexDatas;
            #print(indexTradingDatas[ts_code]);

        for ts_code in stockCodes:
            stockData = getIndexOrStock('E', ts_code, startDate, endDate)
            tradingDatas[ts_code] = stockData;
            #print(tradingDatas[ts_code]);
        datas['indexTradingDatas'] = indexTradingDatas
        datas['tradingDatas']=tradingDatas

        if(macroParams):
            numOfMacroParams = len(macroParams)
            for macroType in macroParams:
                macroDatas[macroType]=getMacroDataByType(macroType, startDate, endDate)
                #print(macroDatas)
        datas['macroDatas']= macroDatas

        if(financialIndexParams):
            fieldStr = 'ann_date,end_date'
            for finaIndex in financialIndexParams:
                fieldStr+=","+finaIndex
            df = pro.query('fina_indicator', ts_code=stockCodes[0], start_date=startDate, end_date=endDate, fields=fieldStr)
            finaIndexData = df.values.tolist()
            for i in range(len(finaIndexData)):
                finaIndexData[i][0] = int(finaIndexData[i][0])
                finaIndexData[i][1] = int(finaIndexData[i][1])
            finaIndexData.reverse()
            print(finaIndexData)
            datas['financialIndexDatas'] = finaIndexData
        datas['tradingCalendarData'] = tradingCalendar

        return JsonResponse(datas)
    endDate = datetime.datetime.now().strftime('%Y%m%d')
    startDate = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y%m%d')
    tradingCalendar = getTradingCalendar(startDate, endDate)
    datas = getIndexOrStock('I','000001.SH', startDate, endDate)
    return render(request, "index.html", {'stockData': datas, 'TradingCalendar':tradingCalendar})

def getIndexOrStock(type,ts_code, startDate, endDate):
    #输出 trade_date      close       open       high        low    vol(成交量（手）)
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', asset=type, start_date=startDate,end_date=endDate)
    df.drop(columns=["ts_code",'pre_close','change','pct_chg','amount'], inplace=True)
    if(type=='E'):#从tushare查询出的股票交易数据顺序与指数的交易数据不一样，需要通过下面的方法排一下序
        cols = ['trade_date','close','open','high','low','vol']
        df = df.loc[:, cols]
    print(df)
    datas = df.values.tolist()
    datas.reverse()
    return datas

def getIndexOrStockFull(type,ts_code, startDate, endDate):
    # 输出  ts_code trade_date      close       open       high  low  pre_close(昨日收盘点)  change(涨跌点)  pct_chg(涨跌幅 %)    vol(成交量（手）)  amount(成交额_千元）
    df = pro.trade_cal(exchange='SSE', start_date=startDate, end_date=endDate)
    df.drop(columns=['ts_code'], inplace=True)
    datas = df.values.tolist()
    datas.reverse()
    return datas

def getTradingCalendar(startDate, endDate):
    df = pro.trade_cal(exchange='SSE', start_date=startDate, end_date=endDate)
    newdf = df[(df.is_open == 1)]
    newdf.drop(columns=['is_open','exchange'], inplace=True)
    datas = newdf.values.tolist()
    print(datas)
    return datas

def getMacroDataByType(macroType, startDate, endDate):
    if("macroCPI"==macroType):
        return getCpi(startDate,endDate)
    if ("macroGdp" == macroType):
        return getGdp(startDate, endDate)
    if ("macroMondySupply" == macroType):
        return getMoneySupply(startDate, endDate)
    if ("macroLPR" == macroType):
        return getLPR(startDate, endDate)

def getCpi(startDate, endDate):

    df = pro.cn_cpi(start_m=startDate[0:6], end_m=endDate[0:6], fields='month,nt_yoy')
    #print( "pro.cn_cpi(start_m="+ startDate[0:6]+", end_m="+endDate[0:6]+", fields='month,nt_yoy'")
    datas = df.values.tolist()
    print(datas)
    for i in range(len(datas)):
        datas[i][0] = int(datas[i][0]+"30")
    datas.reverse()
    return datas

def getGdp(startDate, endDate):
    startQ=startDate[0:4]+"Q"+str(1+(int(startDate[4:6]))//4)
    endQ = endDate[0:4] + "Q" + str(1+(int(endDate[4:6])) // 4)
    print("startQ:")
    print (int(startDate[4:6]))
    df = pro.cn_gdp(start_q=startQ, end_q=endQ, fields='quarter,gdp_yoy')
    print( "pro.cn_cpi(start_q="+ startQ+", end_q="+endQ+", fields='quarter,gdp_yoy'")
    datas = df.values.tolist()
    print(datas)
    for i in range(len(datas)):
        datas[i][0] = int(datas[i][0][0:4]+ str(int(datas[i][0][5:6])*3).zfill(2) +"30")
    datas.reverse()
    return datas

def getMoneySupply(startDate, endDate):
    items = MoneySupplyDb.objects.filter(time__gt=startDate[0:6], time__lt=endDate[0:6])
    recordsNum = len(items)
    dbData = list(items.values())
    datas = []
    for i in range(recordsNum):
        newTime = int(dbData[i]["time"]+ "30")
        datas.append([newTime,dbData[i]["m2YOY"]])
        #      data["tableData"][i]["m2Value"],);
        # dataList.append(
        #     [data["tableData"][i]["time"],
        #      data["tableData"][i]["m2Value"],
        #      data["tableData"][i]["m2YOY"],
        #      data["tableData"][i]["m1Value"],
        #      data["tableData"][i]["m1YOY"],
        #      data["tableData"][i]["m1Value"],
        #      data["tableData"][i]["m1YOY"]
        #      ])
    datas.reverse()
    print(datas)
    return datas
    #return {'tableData': dataList, 'tableTitle': ["日期", "PPI", "同比", "环比", "累积", "公布日期"]}

def getLPR(startDate, endDate):
    print (int(startDate[4:6]))
    df = pro.shibor_lpr(start_date=startDate, end_date=endDate)
    datas = df.values.tolist()
    print(datas)
    for i in range(len(datas)):
        datas[i][0] = int(datas[i][0]);
    datas.reverse()
    return datas

# def getCpiSpider(format,startDate, endDate):
#     #items = CpiSpiderManager.objects.filter(time__gte=startDate)
#     items = CpiSpiderManager.objects.all().order_by("-time")
#     recordsNum = len(items)
#     data = {}
#     data["tableData"] = list(items.values())
#     dataList = []
#     for i in range(recordsNum):
#         YOYIndex = i + 12
#         YOY = -1
#         if YOYIndex < recordsNum:
#             newValue=data["tableData"][i]["value"]
#             oldValue=data["tableData"][YOYIndex]["value"]
#             YOY = format(round(((newValue - oldValue) / oldValue), 4), '.2%')
#             # aaa=data["tableData"][i]["date"]
#             # print(aaa)
#             # print(newValue)
#             # print(oldValue)
#             # print(YOY)
#
#         lRRIndex = i + 1
#         linkRelativeRatio = -1
#         if lRRIndex < recordsNum:
#             newValue = data["tableData"][i]["value"]
#             oldValue = data["tableData"][lRRIndex]["value"]
#             linkRelativeRatio = format(round(((newValue - oldValue) / oldValue), 4), '.2%')
#
#         month = int(data["tableData"][i]["time"][-2:])
#         accumulative = 0
#         for j in range(month):
#             if (i + j) < recordsNum:
#                 accumulative += data["tableData"][i + j]["value"]
#             else:
#                 break;
#         accumulative = round(accumulative / (j+1), 1)
#
#         dataList.append(
#             [str(data["tableData"][i]["time"]), data["tableData"][i]["value"], YOY, linkRelativeRatio, accumulative])
#     if("full"==format):
#         return {'tableData': dataList, 'tableTitle': ["日期", "CPI", "同比", "环比", "累积","公布日期"]}
#     elif ("dataOnly"==format):
#         print(dataList)
#         return dataList

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


# def getCpi(format):
#     items = CpiManager.objects.all().order_by("-date")
#
#     recordsNum = len(items)
#
#     data = {}
#     data["tableData"] = list(items.values())
#     dataList = []
#     for i in range(recordsNum):
#         YOYIndex = i + 12
#         YOY = -1
#         if YOYIndex < recordsNum:
#             newValue=data["tableData"][i]["value"]
#             oldValue=data["tableData"][YOYIndex]["value"]
#             YOY = format(round(((newValue - oldValue) / oldValue), 4), '.2%')
#             # aaa=data["tableData"][i]["date"]
#             # print(aaa)
#             # print(newValue)
#             # print(oldValue)
#             # print(YOY)
#
#         lRRIndex = i + 1
#         linkRelativeRatio = -1
#         if lRRIndex < recordsNum:
#             newValue = data["tableData"][i]["value"]
#             oldValue = data["tableData"][lRRIndex]["value"]
#             linkRelativeRatio = format(round(((newValue - oldValue) / oldValue), 4), '.2%')
#
#         month = data["tableData"][i]["date"].month
#         accumulative = 0
#         for j in range(month):
#             if (i + j) < recordsNum:
#                 accumulative += data["tableData"][i + j]["value"]
#             else:
#                 break;
#         accumulative = round(accumulative / (j+1), 1)
#
#         dataList.append(
#             [str(data["tableData"][i]["date"]), data["tableData"][i]["value"], YOY, linkRelativeRatio, accumulative, str(data["tableData"][i]["publicDate"])])
#     if("full"==format):
#         return {'tableData': dataList, 'tableTitle': ["日期", "CPI", "同比", "环比", "累积","公布日期"]}
#     elif ("dataOnly"==format):
#         return dataList

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
        return JsonResponse(getCpi("full"))
    #print(getCpi())
    return render(request, 'dataManagerCpi.html', getCpi("full"))

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