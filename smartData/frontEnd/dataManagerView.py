#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
import tushare as ts
from django.shortcuts import render
from  django.http  import  JsonResponse
from .models import *
from .dataManagerInterface import *
import datetime
#from django.shortcuts import render_to_response
import numpy as np
import pandas as pd

ts.set_token('abc23dc1908af03d82e14f830e52e28300ef5ac69bb5fe14e2ba8630')
pro = ts.pro_api()
def main(request):
    return
    #updateStockListOfIndustryClassify()
    #updateStockLimitUpDown('20200701', '20200712')
    #updateStockListOfIndustryClassify()
    #updateIndustryClassify()
    # updateFinanceIndicatorOfAllStocks('19490101','20200808')


def getTradingCalendar(startDate, endDate):
    df = pro.trade_cal(exchange='SSE', start_date=startDate, end_date=endDate)
    newdf = df[(df.is_open == 1)]
    newdf.drop(columns=['is_open','exchange'], inplace=True)
    datas = newdf.values.tolist()
    #print(datas)
    return datas

def updateStockLimitUpDown(startDate, endDate):
    tradingCalendar = getTradingCalendar(startDate, endDate)
    for date in tradingCalendar:
        dfUp = pro.limit_list(trade_date=date[0], limit_type='U')
        dfDown = pro.limit_list(trade_date=date[0], limit_type='D')
        numOfDfUp = dfUp.shape[0];
        numOfDfDown = dfDown.shape[0];
        if 0 < numOfDfUp:
            for row in dfUp.values:
                dataManagerStoreStockLimitUp(row)
        if 0<numOfDfDown:
            for row in dfDown.values:
                dataManagerStoreStockLimitDown(row)
        NumOfStockLimitUpDown=[date[0], numOfDfUp, numOfDfDown];
        dataManagerNumOfStockLimitUpDown(NumOfStockLimitUpDown)

def getIndustryClassify():  #获得申万分类
    dfIndustryClassifyL3 = pro.index_classify(level='L3', src='SW')
    return dfIndustryClassifyL3.values.tolist()

def updateStockListOfIndustryClassify():  #收集各分类的股票列表并写入数据库
    industryClassifyL3 = getIndustryClassify()
    for industryItem in industryClassifyL3:
        dfStockList = pro.index_member(index_code=industryItem[0])
        stocklist = dfStockList.values.tolist()
        for stockItem in stocklist:
            dataManagerStockListOfdustryClassify(stockItem)

def updateIndustryClassify():#获取申万分类并写入数据库
    dfIndustryClassify = pro.index_classify(src='SW')
    industryClassify = dfIndustryClassify.values.tolist()
    for row in industryClassify:
        dataManagerIndustryClassify(row)

def updateIncomeOfSingleStock(stockCode, startDate, endDate):
    #dataManagerCreateIncomeTableForStock
    df = pro.income(ts_code=stockCode, start_date=startDate, end_date=endDate)
    df = df.where(df.notnull(), None)
    recordsTitle = list(df.columns.values)
    values = df.values.tolist()
    for row in range(len(values)):
        dataManagerUpdateIncomeTableForStock(stockCode, recordsTitle, values[row])

def updateIncomeOfAllStocks(startDate, endDate):
    #return getAllModels()
    industryClassifyItems = dataManagerGetIndustryClassify()
    for item in industryClassifyItems:
        stockListOfdustryClassify = dataManagerGetStockListOfdustryClassify(item['industryCode'])
        for stock in stockListOfdustryClassify:
            updateIncomeOfSingleStock(stock['stockCode'], startDate, endDate)

def updateFinanceIndicatorOfSingleStock(stockCode, startDate, endDate):
    #dataManagerCreateIncomeTableForStock
    df = pro.query('fina_indicator', ts_code=stockCode, start_date=startDate, end_date=endDate)
    df = df.where(df.notnull(), None)
    recordsTitle = list(df.columns.values)
    values = df.values.tolist()
    for row in range(len(values)):
        dataManagerUpdateFinanceindicator(stockCode, recordsTitle, values[row])

def updateFinanceIndicatorOfAllStocks(startDate, endDate):
    #return getAllModels()
    industryClassifyItems = dataManagerGetIndustryClassify()
    for item in industryClassifyItems:
        stockListOfdustryClassify = dataManagerGetStockListOfdustryClassify(item['industryCode'])
        for stock in stockListOfdustryClassify:
            updateFinanceIndicatorOfSingleStock(stock['stockCode'], startDate, endDate)

