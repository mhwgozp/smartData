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
import json
import os

ts.set_token('abc23dc1908af03d82e14f830e52e28300ef5ac69bb5fe14e2ba8630')
pro = ts.pro_api()
def main(request):
    #storeStockList()
    #storeFinanceIndicatorIntoJson()
    return
    # df = pro.query('fina_indicator', ts_code='300088.SZ', start_date='20200701', end_date='20200801')
    # df = df.where(df.notnull(), None)
    # print(df)

    #updateFinancialIndicatorForIndustries('20110331', '20200930')
    #return
    #updateStockListOfIndustryClassify()
    #updateStockLimitUpDown('20200701', '20200712')
    #updateStockListOfIndustryClassify()
    #updateIndustryClassify()
    #updateFinanceIndicatorOfAllStocks('19800101','20201031')


def getTradingCalendar(startDate, endDate):
    df = pro.trade_cal(exchange='SSE', start_date=startDate, end_date=endDate)
    newdf = df[(df.is_open == 1)]
    newdf.drop(columns=['is_open','exchange'], inplace=True)
    datas = newdf.values.tolist()
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
                storeStockLimitUp(row)
        if 0<numOfDfDown:
            for row in dfDown.values:
                storeStockLimitDown(row)
        NumOfStockLimitUpDown=[date[0], numOfDfUp, numOfDfDown];
        numOfStockLimitUpDown(NumOfStockLimitUpDown)

# def getIndustryClassify():  #获得申万分类
#     dfIndustryClassifyL3 = pro.index_classify(level='L3', src='SW')
#     print(dfIndustryClassifyL3)
#     return dfIndustryClassifyL3.values.tolist()

def updateStockListOfIndustryClassify():  #收集各分类的股票列表并写入数据库
    industryClassifyL3 = getIndustryClassify()
    for industryItem in industryClassifyL3:
        dfStockList = pro.index_member(index_code=industryItem['industryCode'])
        stocklist = dfStockList.values.tolist()
        for stockItem in stocklist:
            stockListOfdustryClassify(stockItem)

def updateIndustryClassify():#获取申万分类并写入数据库
    dfIndustryClassify = pro.index_classify(src='SW')
    industryClassify = dfIndustryClassify.values.tolist()
    for row in industryClassify:
        industryClassify(row)

def updateIncomeOfSingleStock(stockCode, startDate, endDate):
    #dataManagerCreateIncomeTableForStock
    df = pro.income(ts_code=stockCode, start_date=startDate, end_date=endDate)
    df = df.where(df.notnull(), None)
    recordsTitle = list(df.columns.values)
    values = df.values.tolist()
    for row in range(len(values)):
        updateIncomeTableForStock(stockCode, recordsTitle, values[row])

def updateIncomeOfAllStocks(startDate, endDate):
    #return getAllModels()
    industryClassifyItems = getIndustryClassify()
    for item in industryClassifyItems:
        stockListOfdustryClassify = getStockListOfdustryClassify(item['industryCode'])
        for stock in stockListOfdustryClassify:
            updateIncomeOfSingleStock(stock['stockCode'], startDate, endDate)

def updateFinanceIndicatorOfSingleStock(stockCode, startDate, endDate):
    #dataManagerCreateIncomeTableForStock
    df = pro.query('fina_indicator', ts_code=stockCode, start_date=startDate, end_date=endDate,fields='ts_code,ann_date,end_date,eps,dt_eps,total_revenue_ps,revenue_ps,capital_rese_ps,surplus_rese_ps,undist_profit_ps,extra_item,profit_dedt,gross_margin,current_ratio,quick_ratio,cash_ratio,invturn_days,arturn_days,inv_turn,ar_turn,ca_turn,fa_turn,assets_turn,op_income,valuechange_income,interst_income,daa,ebit,ebitda,fcff,fcfe,current_exint,noncurrent_exint,interestdebt,netdebt,tangible_asset,working_capital,networking_capital,invest_capital,retained_earnings,diluted2_eps,bps,ocfps,retainedps,cfps,ebit_ps,fcff_ps,fcfe_ps,netprofit_margin,grossprofit_margin,cogs_of_sales,expense_of_sales,profit_to_gr,saleexp_to_gr,adminexp_of_gr,finaexp_of_gr,impai_ttm,gc_of_gr,op_of_gr,ebit_of_gr,roe,roe_waa,roe_dt,roa,npta,roic,roe_yearly,roa2_yearly,roe_avg,opincome_of_ebt,investincome_of_ebt,n_op_profit_of_ebt,tax_to_ebt,dtprofit_to_profit,salescash_to_or,ocf_to_or,ocf_to_opincome,capitalized_to_da,debt_to_assets,assets_to_eqt,dp_assets_to_eqt,ca_to_assets,nca_to_assets,tbassets_to_totalassets,int_to_talcap,eqt_to_talcapital,currentdebt_to_debt,longdeb_to_debt,ocf_to_shortdebt,debt_to_eqt,eqt_to_debt,eqt_to_interestdebt,tangibleasset_to_debt,tangasset_to_intdebt,tangibleasset_to_netdebt,ocf_to_debt,ocf_to_interestdebt,ocf_to_netdebt,ebit_to_interest,longdebt_to_workingcapital,ebitda_to_debt,turn_days,roa_yearly,roa_dp,fixed_assets,profit_prefin_exp,non_op_profit,op_to_ebt,nop_to_ebt,ocf_to_profit,cash_to_liqdebt,cash_to_liqdebt_withinterest,op_to_liqdebt,op_to_debt,roic_yearly,total_fa_trun,profit_to_op,q_opincome,q_investincome,q_dtprofit,q_eps,q_netprofit_margin,q_gsprofit_margin,q_exp_to_sales,q_profit_to_gr,q_saleexp_to_gr,q_adminexp_to_gr,q_finaexp_to_gr,q_impair_to_gr_ttm,q_gc_to_gr,q_op_to_gr,q_roe,q_dt_roe,q_npta,q_opincome_to_ebt,q_investincome_to_ebt,q_dtprofit_to_profit,q_salescash_to_or,q_ocf_to_sales,q_ocf_to_or,basic_eps_yoy,dt_eps_yoy,cfps_yoy,op_yoy,ebt_yoy,netprofit_yoy,dt_netprofit_yoy,ocf_yoy,roe_yoy,bps_yoy,assets_yoy,eqt_yoy,tr_yoy,or_yoy,q_gr_yoy,q_gr_qoq,q_sales_yoy,q_sales_qoq,q_op_yoy,q_op_qoq,q_profit_yoy,q_profit_qoq,q_netprofit_yoy,q_netprofit_qoq,equity_yoy,rd_exp')
    df = df.where(df.notnull(), None)
    # print(df)
    recordsTitle = list(df.columns.values)
    values=df.values.tolist()
    values.reverse()
    for row in range(len(values)):
         updateFinanceindicator(stockCode, values[row])

def updateFinanceIndicatorOfAllStocks(startDate, endDate):
    #return getAllModels()
    industryClassifyItems = getIndustryClassify()
    for item in industryClassifyItems:
        stockListOfdustryClassify = getStockListOfdustryClassify(item['industryCode'])
        for stock in stockListOfdustryClassify:
            print("    industryCode:"+ item['industryCode']+", stockCode:"+ stock['stockCode'])
            # items = IndustryClassify.objects.filter(industryLevel="L3")
            updateFinanceIndicatorOfSingleStock(stock['stockCode'], startDate, endDate)

def getNextQuarter(date):
    quarters = ["0331", "0630", "0930", "1231"]
    endMonthDay = ""
    print(date)
    for qIndex in range(4):
        # print("aaaaaaaa")
        # print(date[4:8])
        # print(quarters[qIndex])
        # print("bbbbbbb")
        if int(date[4:8]) <= int(quarters[qIndex]):
            endMonthDay = quarters[(qIndex+1)%4]
            if (3==qIndex):
                return (str(int(date[0:4]) + 1) + endMonthDay)
            else:
                return (date[0:4] + endMonthDay)

def getCurQuarter(date):
    quarters = ["0331", "0630", "0930", "1231"]
    endMonthDay = ""
    for qIndex in range(4):
        if date[4:8] <= quarters[qIndex]:
            endMonthDay = quarters[qIndex]
            return (date[0:4]+endMonthDay)

def getPreQuarter(date):
    quarters = ["0331", "0630", "0930", "1231"]
    endMonthDay = ""
    for qIndex in range(4):
        if date[4:8] <= quarters[qIndex]:
            endMonthDay = quarters[(qIndex+4-1)%4]
            if(qIndex==0):
                return (str(int(date[0:4])-1)+endMonthDay)
            else:
                return (date[0:4]+endMonthDay)

def getEndDates(startDate, endDate):
    endDates=[]
    tempEndDate=""
    tempEndDate = getCurQuarter(startDate)
    endDates.append(tempEndDate)
    startDate=tempEndDate

    while startDate < endDate:
        tempEndDate = getNextQuarter(startDate)
        endDates.append(tempEndDate)
        startDate=tempEndDate
    return endDates

def updateFinancialIndicatorForIndustries(startDate, endDate):
    industryClassifyItems = getIndustryClassify()
    endDates = getEndDates(startDate, endDate)
    recordsTitle = getRecordsTitleOfFinanceIndicator()
    totalRecordsNum=len(recordsTitle)   # 166, don't include "id"
    skipNum = 4;
    print(endDates)

    for endDate in endDates:
        # print("start==========================================")
        # print(endDate)
        # print("\n")
        for item in industryClassifyItems:
            # print("    start industryCode===========================================")
            # print(item['industryCode'])
            # print("\n")
            stockListOfdustryClassify = getStockListOfdustryClassify(item['industryCode'])
            avgOfFinancialIndicators = [0] * (totalRecordsNum+1-skipNum)   #163
            countOfFinancialIndicators=[0] * (totalRecordsNum+1-skipNum)   #163
            needToSave = 0
            for stock in stockListOfdustryClassify:
                # print(int(stock['stockCode'][0:6]))
                if 1==1:
                #if (int(stock['stockCode'][0:6]) >599999 and int(stock['stockCode'][0:6])<603000) or (int(stock['stockCode'][0:6]) <2500):
                    # print("        start stock===========================================")
                    print(endDate + "_"+ item['industryCode']+ "_"+stock['stockCode'])
                    # print("\n")
                    data=queryFinancialIndicatorOneQuarter(stock['stockCode'], endDate)
                    if 0< len(data):
                        needToSave = 1
                        j=0
                        for v in data[0].values():
                            if j>=skipNum and v is not None:
                                avgOfFinancialIndicators[j-skipNum]+=v
                                countOfFinancialIndicators[j-skipNum] +=1
                            j += 1
                        # print("              ")
                        # print(avgOfFinancialIndicators)
                        # print("\n              ")
                        # print(countOfFinanceIndicators)
                # print("        end stock===========================================\n")

            # print(endDate)

            # print(avgOfFinancialIndicators)
            # print("\n")
            if 1==needToSave:
                for i in range(len(avgOfFinancialIndicators)):
                    if(0<countOfFinancialIndicators[i]):
                        avgOfFinancialIndicators[i] = avgOfFinancialIndicators[i]/countOfFinancialIndicators[i]
                updateAvgFinancialIndicatorsForIndustries(item['industryCode'], endDate, avgOfFinancialIndicators)
        #     print("    end industryCode===========================================\n")
        # print("end date ===========================================\n")

def storeIndustrysIntoJson():
    industryClassifyItems = getIndustryClassify()
    industry={}
    for industryClassifyItem in industryClassifyItems:
        industry[industryClassifyItem['industryCode']] = industryClassifyItem['industryName']
    data = {}
    data["data"] = industry
    with open('frontEnd/templates/assets/data/industryClassify.json', 'w') as fp:
        fp.write(json.dumps(data, indent=4))
        # fp.write(json.dumps(data, indent=4, ensure_ascii=False))

def storeFinanceIndicatorIntoJson():
    data = {}
    data["data"] = getFinanceIndicatorList()
    with open('frontEnd/templates/assets/data/financeIndicators.json', 'w') as fp:
        fp.write(json.dumps(data, indent=4))

def storeStockList():
    stocksListDf= pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')
    stocksList = stocksListDf.values.tolist()
    i=0;
    for row in range(len(stocksList)):
        saveStockList(stocksList[row])
