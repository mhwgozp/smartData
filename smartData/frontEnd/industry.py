#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
import tushare as ts
from django.shortcuts import render
from  django.http  import  JsonResponse
from .models import *
from .dataManagerInterface import *
from .dataManagerView import *
import datetime
#from django.shortcuts import render_to_response
import numpy as np
import pandas as pd
import json
import os

ts.set_token('abc23dc1908af03d82e14f830e52e28300ef5ac69bb5fe14e2ba8630')
pro = ts.pro_api()

def main(request):
    allStocksName = getStocksName()
    if request.method == 'POST':
        action = request.POST.get('action')
        industryCode = request.POST.get("industryCode")
        datas = {}
        datas['industryCode'] = industryCode
        if(action == 'getTradingDatas'):
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            selectTopNum = int(request.POST.get('selectTopNum'))
            selectPeriod = request.POST.get('selectPeriod')
            tradingDatasStocksName = {}
            datas['tradingCalendar'] = getTradingCalendar(startDate, endDate)
            datas['tradingDatas']  = getStockPriceTopList(industryCode, selectPeriod, startDate, endDate, selectTopNum)
            for key in datas['tradingDatas']:
                tradingDatasStocksName[key] =allStocksName[key]
            datas['tradingDatasStocksName'] = tradingDatasStocksName
        elif (action == 'getFinancialDatas'):
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')
            selectTopNum = int(request.POST.get('selectTopNum'))
            financialIndicatorSelected = request.POST.get('financialIndicatorSelected')
            datas['calendarData'] = getEndDates(startDate, endDate)
            indicatorsList = ['end_date', financialIndicatorSelected]
            datas['financialDatas'] = getFinancialIndicatorTopList(industryCode, startDate, endDate, indicatorsList, selectTopNum)
        elif (action == 'getAllFinancialDatas'):
            reportPeriod = request.POST.get('reportPeriod')
            indicatorsList = ['ts_code', 'end_date', 'grossprofit_margin', 'netprofit_margin', 'roe', 'roe_dt',
                              'op_yoy', 'or_yoy', 'equity_yoy']
            allFinancialDatas = getFinancialIndicators(industryCode, reportPeriod, indicatorsList)
            stocksName = [0 for row in range(len(allFinancialDatas))]
            for index in range(len(allFinancialDatas)):
                stocksName[index] = allStocksName[allFinancialDatas[index][0]]
            allFinancialDatas = np.insert(allFinancialDatas, 0, stocksName, axis=1)
            datas['allFinancialDatas'] = allFinancialDatas.tolist()
        return JsonResponse(datas)
    elif request.method == 'GET':
        curDate = datetime.datetime.now()
        if curDate.hour < 18:
            preDate = datetime.timedelta(days=1, hours=0, minutes=0, seconds=10)
            curDate = curDate - preDate
        endDate = curDate.strftime('%Y%m%d')
        startDate = (curDate - datetime.timedelta(days=365)).strftime('%Y%m%d')
        industryCode = request.GET.get("industryCode")
        industryName = request.GET.get("industryName")
        tradingCalendar = getTradingCalendar(startDate, endDate)
        tradingDatas = getStockPriceTopList(industryCode, 'W', startDate, endDate, 10)

        tradingDatasStocksName = {}
        for key in tradingDatas:
            tradingDatasStocksName[key] = allStocksName[key]
        return render(request, "industry.html", {'industryCode':industryCode, 'industryName':industryName, 'tradingCalendar': tradingCalendar, 'tradingDatas':tradingDatas, 'tradingDatasStocksName':tradingDatasStocksName})

def getStockPriceTopList(industryCode, periodType, startDate, endDate, topNumber):
    stockListOfdustryClassify = getStockListOfdustryClassify(industryCode)
    topStockCodeList = []
    allTradingDatas = {}
    topTradingDatas = {}
    for stockItem in stockListOfdustryClassify:
        if periodType=='D':
            stockData = getIndexOrStock('E', stockItem['stockCode'], startDate, endDate)
        elif periodType=='W':
            stockData = getIndexOrStockWeekly('E', stockItem['stockCode'], startDate, endDate)
        elif periodType=='M':
            stockData = getIndexOrStockMonthly('E', stockItem['stockCode'], startDate, endDate)
        allTradingDatas[stockItem['stockCode']] = stockData;
        increaseRate = stockData[len(stockData)-1][2] / stockData[0][2]
        topStockCodeList.append([stockItem['stockCode'], increaseRate])
    topStockCodeList.sort(key=lambda x: x[1], reverse=True)
    topNumber = min(topNumber, len(stockListOfdustryClassify))
    for i in range(topNumber):
        topTradingDatas[topStockCodeList[i][0]] = allTradingDatas[topStockCodeList[i][0]]
    return topTradingDatas

def getFinancialIndicatorTopList(industryCode, startDate, endDate, indicatorsList, topNumber):
    stockListOfdustryClassify = getStockListOfdustryClassify(industryCode)
    topStockCodeList = []
    allFinancialDatas = {}
    topFinancialDatas = {}

    for stockItem in stockListOfdustryClassify:
        allFinancialDatas[stockItem['stockCode']] = queryFinanceindicator(stockItem['stockCode'], startDate, endDate, indicatorsList)
        stockCode = stockItem['stockCode']
        numOfOneStock = len(allFinancialDatas[stockItem['stockCode']])
        topStockCodeList.append( [ stockCode,  allFinancialDatas[stockCode][numOfOneStock-1][1] ] )
    print(" getFinancialIndicatorTopList ")
    print(topStockCodeList)
    topStockCodeList.sort(key=lambda x: x[1], reverse=True)
    print(topStockCodeList)

    topNumber = min(topNumber, len(stockListOfdustryClassify))
    for i in range(topNumber):
        topFinancialDatas[topStockCodeList[i][0]] = allFinancialDatas[topStockCodeList[i][0]]
        print("top " + str(i)+":")
        print(topFinancialDatas[topStockCodeList[i][0]])
    return topFinancialDatas

def getFinancialIndicators(industryCode, reportPeriod, indicatorsList):
    stockListOfdustryClassify = getStockListOfdustryClassify(industryCode)
    allFinancialDatas = []
    for stockItem in stockListOfdustryClassify:
        financialDatas = queryFinanceindicator(stockItem['stockCode'], reportPeriod, reportPeriod, indicatorsList)
        allFinancialDatas.append(financialDatas[0])
    return allFinancialDatas

