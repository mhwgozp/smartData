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
    if request.method == 'POST':
        industryClassifySelected = request.POST.getlist('industryClassifySelected')
        financeIndicatorsSelected = request.POST.getlist('financialIndicatorsSelected')
        financeIndicatorsSelected.insert(0,'end_date')
        startDate = request.POST.get('startDate')
        endDate = request.POST.get('endDate')

        datas = {'calendarData':{}, 'financialDatas': {}}
        financialDatas = {}
        for industryClassify in industryClassifySelected:
            print(industryClassify+"\n")
            print(financeIndicatorsSelected)
            print("startDate:"+startDate)
            print("endDate:" + endDate)
            financialDatas[industryClassify] = queryAvgFinancialIndicatorForOneIndustry(startDate, endDate, industryClassify, financeIndicatorsSelected)
            print(financialDatas[industryClassify])
        datas['financialDatas'] = financialDatas
        datas['calendarData'] = getEndDates(startDate, endDate)
        return JsonResponse(datas)
    indicatorsList = ['industryCode', 'end_date', 'grossprofit_margin', 'netprofit_margin', 'roe', 'roe_dt',
                      'op_yoy', 'or_yoy', 'equity_yoy']
    getTopFinanceIndicators('20200630', indicatorsList)
    return render(request, "industries.html", {})

def getIndustryNameByIndustryCode(industryCode, industryClassifyItems):
    for industryClassify in industryClassifyItems:
        if(industryClassify['industryCode'] == industryCode):
            return industryClassify['industryName']

def getTopFinanceIndicators(endDate, indicatorsList):
    # indicatorsList = ['行业', '报告期', '销售毛利率','销售净利率','净资产收益率','净资产收益率(扣除非经常损益)','营业利润同比增长率','营业收入同比增长率','净资产同比增长率']
    # if (not os.path.exists('frontEnd/templates/assets/data/industryIndicator.json')):

        indicatorDatas = queryAvgFinanceindicaIndustriesForIndustries(endDate, indicatorsList)
        industryClassifyItems = getIndustryClassify()
        industryNames=[0 for row in range(len(indicatorDatas))]
        for index in range(len(indicatorDatas)):
            industryNames[index] = getIndustryNameByIndustryCode(indicatorDatas[index][0], industryClassifyItems)

        indicatorDatas = np.insert(indicatorDatas, 0,industryNames, axis=1)
        # newIndicatorDatas = sorted(indicatorDatas, key=lambda indicatorDatas: indicatorDatas[2], reverse = True)
        data = {}
        data["data"]=indicatorDatas.tolist()

        with open('frontEnd/templates/assets/data/industryIndicator.json', 'w') as fp:
            fp.write(json.dumps(data, indent=4))
            # fp.write(json.dumps(data, indent=4, ensure_ascii=False))


