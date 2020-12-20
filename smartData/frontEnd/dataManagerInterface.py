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
from django.db import connection, migrations, models
from django.db.migrations.executor import MigrationExecutor
from django.apps import apps
from collections import OrderedDict
from django.db.models import Q
import talib as ta
from talib import MA_Type

ts.set_token('abc23dc1908af03d82e14f830e52e28300ef5ac69bb5fe14e2ba8630')
pro = ts.pro_api()

def storeStockLimitUp(data):
    item = StockLimitUp()
    item.trade_date = data[0]
    item.ts_code = data[1]
    item.ts_name = data[2]
    item.close = data[3]
    item.pct_chg = data[4]
    item.amp = data[5]
    item.fc_ratio = data[6]
    item.fl_ratio = data[7]
    item.fd_amount = data[8]
    if(""!=data[9]):
        item.first_time = data[9]
    if(""!=data[10]):
        item.last_time = data[10]
    item.open_times = data[11]
    item.strth = data[12]
    item.save()

def storeStockLimitDown(data):
    item = StockLimitDown()
    item.trade_date = data[0]
    item.ts_code = data[1]
    item.ts_name = data[2]
    item.close = data[3]
    item.pct_chg = data[4]
    item.amp = data[5]
    item.fc_ratio = data[6]
    item.fl_ratio = data[7]
    item.fd_amount = data[8]
    if(""!=data[9]):
        item.first_time = data[9]
    if(""!=data[10]):
        item.last_time = data[10]
    item.open_times = data[11]
    item.strth = data[12]
    item.save()

def numOfStockLimitUpDown(data):
    item = NumOfStockLimitUpDown()
    item.trade_date = data[0]
    item.NumOfLimitUp = data[1]
    item.NumOfLimitDown = data[2]
    item.save()

def industryClassify(data):
    item = IndustryClassify()
    item.industryCode = data[0]
    item.industryName = data[1]
    item.industryLevel = data[2]
    item.save()

def getIndustryClassify():
    items = IndustryClassify.objects.filter(industryLevel="L3")
    #items = IndustryClassify.objects.filter(id__gte=342)
    return items.values()

def stockListOfdustryClassify(data):
    item = StockListOfdustryClassify()
    item.industryCode = data[0];
    item.stockCode = data[1];
    item.inDate = data[2];
    item.outDate = data[3];
    item.save()

def getStockListOfdustryClassify(industryCode):
    items = StockListOfdustryClassify.objects.filter(industryCode=industryCode)
    return items.values()

def getRecordsTitleOfFinanceIndicator():
    # return ['ts_code','ann_date','end_date','eps','dt_eps','total_revenue_ps','revenue_ps','capital_rese_ps','surplus_rese_ps','undist_profit_ps','extra_item','profit_dedt','gross_margin',
    #         'current_ratio','quick_ratio','cash_ratio','ar_turn','ca_turn','fa_turn','assets_turn','op_income','ebit','ebitda','fcff','fcfe','current_exint','noncurrent_exint','interestdebt',
    #         'netdebt','tangible_asset','working_capital','networking_capital','invest_capital','retained_earnings','diluted2_eps','bps','ocfps','retainedps','cfps','ebit_ps','fcff_ps','fcfe_ps',
    #         'netprofit_margin','grossprofit_margin','cogs_of_sales','expense_of_sales','profit_to_gr','saleexp_to_gr','adminexp_of_gr','finaexp_of_gr','impai_ttm','gc_of_gr','op_of_gr',
    #         'ebit_of_gr','roe','roe_waa','roe_dt','roa','npta','roic','roe_yearly','roa2_yearly','debt_to_assets','assets_to_eqt','dp_assets_to_eqt','ca_to_assets','nca_to_assets','tbassets_to_totalassets',
    #         'int_to_talcap','eqt_to_talcapital','currentdebt_to_debt','longdeb_to_debt','ocf_to_shortdebt','debt_to_eqt','eqt_to_debt','eqt_to_interestdebt','tangibleasset_to_debt','tangasset_to_intdebt',
    #         'tangibleasset_to_netdebt','ocf_to_debt','turn_days','roa_yearly','roa_dp','fixed_assets','profit_to_op','q_saleexp_to_gr','q_gc_to_gr','q_roe','q_dt_roe','q_npta','q_ocf_to_sales','basic_eps_yoy',
    #         'dt_eps_yoy','cfps_yoy','op_yoy','ebt_yoy','netprofit_yoy','dt_netprofit_yoy','ocf_yoy','roe_yoy','bps_yoy','assets_yoy','eqt_yoy','tr_yoy','or_yoy','q_sales_yoy','q_op_qoq','equity_yoy']
    return ['ts_code','ann_date','end_date','eps','dt_eps','total_revenue_ps','revenue_ps','capital_rese_ps','surplus_rese_ps','undist_profit_ps','extra_item','profit_dedt','gross_margin','current_ratio','quick_ratio','cash_ratio','invturn_days','arturn_days','inv_turn','ar_turn','ca_turn','fa_turn','assets_turn','op_income','valuechange_income','interst_income','daa','ebit','ebitda','fcff','fcfe','current_exint','noncurrent_exint','interestdebt','netdebt','tangible_asset','working_capital','networking_capital','invest_capital','retained_earnings','diluted2_eps','bps','ocfps','retainedps','cfps','ebit_ps','fcff_ps','fcfe_ps','netprofit_margin','grossprofit_margin','cogs_of_sales','expense_of_sales','profit_to_gr','saleexp_to_gr','adminexp_of_gr','finaexp_of_gr','impai_ttm','gc_of_gr','op_of_gr','ebit_of_gr','roe','roe_waa','roe_dt','roa','npta','roic','roe_yearly','roa2_yearly','roe_avg','opincome_of_ebt','investincome_of_ebt','n_op_profit_of_ebt','tax_to_ebt','dtprofit_to_profit','salescash_to_or','ocf_to_or','ocf_to_opincome','capitalized_to_da','debt_to_assets','assets_to_eqt','dp_assets_to_eqt','ca_to_assets','nca_to_assets','tbassets_to_totalassets','int_to_talcap','eqt_to_talcapital','currentdebt_to_debt','longdeb_to_debt','ocf_to_shortdebt','debt_to_eqt','eqt_to_debt','eqt_to_interestdebt','tangibleasset_to_debt','tangasset_to_intdebt','tangibleasset_to_netdebt','ocf_to_debt','ocf_to_interestdebt','ocf_to_netdebt','ebit_to_interest','longdebt_to_workingcapital','ebitda_to_debt','turn_days','roa_yearly','roa_dp','fixed_assets','profit_prefin_exp','non_op_profit','op_to_ebt','nop_to_ebt','ocf_to_profit','cash_to_liqdebt','cash_to_liqdebt_withinterest','op_to_liqdebt','op_to_debt','roic_yearly','total_fa_trun','profit_to_op','q_opincome','q_investincome','q_dtprofit','q_eps','q_netprofit_margin','q_gsprofit_margin','q_exp_to_sales','q_profit_to_gr','q_saleexp_to_gr','q_adminexp_to_gr','q_finaexp_to_gr','q_impair_to_gr_ttm','q_gc_to_gr','q_op_to_gr','q_roe','q_dt_roe','q_npta','q_opincome_to_ebt','q_investincome_to_ebt','q_dtprofit_to_profit','q_salescash_to_or','q_ocf_to_sales','q_ocf_to_or','basic_eps_yoy','dt_eps_yoy','cfps_yoy','op_yoy','ebt_yoy','netprofit_yoy','dt_netprofit_yoy','ocf_yoy','roe_yoy','bps_yoy','assets_yoy','eqt_yoy','tr_yoy','or_yoy','q_gr_yoy','q_gr_qoq','q_sales_yoy','q_sales_qoq','q_op_yoy','q_op_qoq','q_profit_yoy','q_profit_qoq','q_netprofit_yoy','q_netprofit_qoq','equity_yoy','rd_exp']

def getFinanceIndicatorNameCN(indicator):
    indicatorNameList ={'ts_code':'TS代码',    'ann_date': '公告日期',    'end_date': '报告期',    'eps': '基本每股收益',    'dt_eps': '稀释每股收益',    'total_revenue_ps': '每股营业总收入',    'revenue_ps': '每股营业收入',
    'capital_rese_ps': '每股资本公积',    'surplus_rese_ps': '每股盈余公积',    'undist_profit_ps': '每股未分配利润',    'extra_item': '非经常性损益',    'profit_dedt': '扣除非经常性损益后的净利润',    'gross_margin': '毛利',
    'current_ratio': '流动比率',    'quick_ratio': '速动比率',    'cash_ratio': '保守速动比率',    'invturn_days': '存货周转天数',    'arturn_days': '应收账款周转天数',    'inv_turn': '存货周转率',    'ar_turn': '应收账款周转率',
    'ca_turn': '流动资产周转率',    'fa_turn': '固定资产周转率',    'assets_turn': '总资产周转率',    'op_income': '经营活动净收益',    'valuechange_income': '价值变动净收益',    'interst_income': '利息费用',    'daa': '折旧与摊销',
    'ebit': '息税前利润',    'ebitda': '息税折旧摊销前利润',    'fcff': '企业自由现金流量',    'fcfe': '股权自由现金流量',    'current_exint': '无息流动负债',    'noncurrent_exint': '无息非流动负债',    'interestdebt': '带息债务',
    'netdebt': '净债务',    'tangible_asset': '有形资产',    'working_capital': '营运资金',    'networking_capital': '营运流动资本',    'invest_capital': '全部投入资本',    'retained_earnings': '留存收益',    'diluted2_eps': '期末摊薄每股收益',
    'bps': '每股净资产',    'ocfps': '每股经营活动产生的现金流量净额',    'retainedps': '每股留存收益',    'cfps': '每股现金流量净额',    'ebit_ps': '每股息税前利润',    'fcff_ps': '每股企业自由现金流量',    'fcfe_ps': '每股股东自由现金流量',
    'netprofit_margin': '销售净利率',    'grossprofit_margin': '销售毛利率',    'cogs_of_sales': '销售成本率',    'expense_of_sales': '销售期间费用率',    'profit_to_gr': '净利润/营业总收入',    'saleexp_to_gr': '销售费用/营业总收入',
    'adminexp_of_gr': '管理费用/营业总收入',    'finaexp_of_gr': '财务费用/营业总收入',    'impai_ttm': '资产减值损失/营业总收入',    'gc_of_gr': '营业总成本/营业总收入',    'op_of_gr': '营业利润/营业总收入',    'ebit_of_gr': '息税前利润/营业总收入',
    'roe': '净资产收益率',    'roe_waa': '加权平均净资产收益率',    'roe_dt': '净资产收益率(扣除非经常损益)',    'roa': '总资产报酬率',    'npta': '总资产净利润',    'roic': '投入资本回报率',    'roe_yearly': '年化净资产收益率',
    'roa2_yearly': '年化总资产报酬率',    'roe_avg': '平均净资产收益率(增发条件)',    'opincome_of_ebt': '经营活动净收益/利润总额',    'investincome_of_ebt': '价值变动净收益/利润总额',    'n_op_profit_of_ebt': '营业外收支净额/利润总额',
    'tax_to_ebt': '所得税/利润总额',    'dtprofit_to_profit': '扣除非经常损益后的净利润/净利润',    'salescash_to_or': '销售商品提供劳务收到的现金/营业收入',    'ocf_to_or': '经营活动产生的现金流量净额/营业收入',    'ocf_to_opincome': '经营活动产生的现金流量净额/经营活动净收益',
    'capitalized_to_da': '资本支出/折旧和摊销',    'debt_to_assets': '资产负债率',    'assets_to_eqt': '权益乘数',    'dp_assets_to_eqt': '权益乘数(杜邦分析)',    'ca_to_assets': '流动资产/总资产',    'nca_to_assets': '非流动资产/总资产',
    'tbassets_to_totalassets': '有形资产/总资产',    'int_to_talcap': '带息债务/全部投入资本',    'eqt_to_talcapital': '归属于母公司的股东权益/全部投入资本',    'currentdebt_to_debt': '流动负债/负债合计',    'longdeb_to_debt': '非流动负债/负债合计',
    'ocf_to_shortdebt': '经营活动产生的现金流量净额/流动负债',    'debt_to_eqt': '产权比率',    'eqt_to_debt': '归属于母公司的股东权益/负债合计',    'eqt_to_interestdebt': '归属于母公司的股东权益/带息债务',    'tangibleasset_to_debt': '有形资产/负债合计',
    'tangasset_to_intdebt': '有形资产/带息债务',    'tangibleasset_to_netdebt': '有形资产/净债务',    'ocf_to_debt': '经营活动产生的现金流量净额/负债合计',    'ocf_to_interestdebt': '经营活动产生的现金流量净额/带息债务',
    'ocf_to_netdebt': '经营活动产生的现金流量净额/净债务',    'ebit_to_interest': '已获利息倍数(EBIT/利息费用)',    'longdebt_to_workingcapital': '长期债务与营运资金比率',    'ebitda_to_debt': '息税折旧摊销前利润/负债合计',
    'turn_days': '营业周期',    'roa_yearly': '年化总资产净利率',    'roa_dp': '总资产净利率(杜邦分析)',    'fixed_assets': '固定资产合计',    'profit_prefin_exp': '扣除财务费用前营业利润',    'non_op_profit': '非营业利润',
    'op_to_ebt': '营业利润／利润总额',    'nop_to_ebt': '非营业利润／利润总额',    'ocf_to_profit': '经营活动产生的现金流量净额／营业利润',    'cash_to_liqdebt': '货币资金／流动负债',    'cash_to_liqdebt_withinterest': '货币资金／带息流动负债',
    'op_to_liqdebt': '营业利润／流动负债',    'op_to_debt': '营业利润／负债合计',    'roic_yearly': '年化投入资本回报率',    'total_fa_trun': '固定资产合计周转率',    'profit_to_op': '利润总额／营业收入',    'q_opincome': '经营活动单季度净收益',
    'q_investincome': '价值变动单季度净收益',    'q_dtprofit': '扣除非经常损益后的单季度净利润',    'q_eps': '每股收益(单季度)',    'q_netprofit_margin': '销售净利率(单季度)',    'q_gsprofit_margin': '销售毛利率(单季度)',
    'q_exp_to_sales': '销售期间费用率(单季度)',    'q_profit_to_gr': '净利润／营业总收入(单季度)',    'q_saleexp_to_gr': '销售费用／营业总收入 (单季度)',    'q_adminexp_to_gr': '管理费用／营业总收入 (单季度)',    'q_finaexp_to_gr': '财务费用／营业总收入 (单季度)',
    'q_impair_to_gr_ttm': '资产减值损失／营业总收入(单季度)',    'q_gc_to_gr': '营业总成本／营业总收入 (单季度)',    'q_op_to_gr': '营业利润／营业总收入(单季度)',    'q_roe': '净资产收益率(单季度)',    'q_dt_roe': '净资产单季度收益率(扣除非经常损益)',
    'q_npta': '总资产净利润(单季度)',    'q_opincome_to_ebt': '经营活动净收益／利润总额(单季度)',    'q_investincome_to_ebt': '价值变动净收益／利润总额(单季度)',    'q_dtprofit_to_profit': '扣除非经常损益后的净利润／净利润(单季度)',
    'q_salescash_to_or': '销售商品提供劳务收到的现金／营业收入(单季度)',    'q_ocf_to_sales': '经营活动产生的现金流量净额／营业收入(单季度)',    'q_ocf_to_or': '经营活动产生的现金流量净额／经营活动净收益(单季度)',    'basic_eps_yoy': '基本每股收益同比增长率(%)',
    'dt_eps_yoy': '稀释每股收益同比增长率(%)',    'cfps_yoy': '每股经营活动产生的现金流量净额同比增长率(%)',    'op_yoy': '营业利润同比增长率(%)',    'ebt_yoy': '利润总额同比增长率(%)',    'netprofit_yoy': '归属母公司股东的净利润同比增长率(%)',
    'dt_netprofit_yoy': '归属母公司股东的净利润-扣除非经常损益同比增长率(%)',    'ocf_yoy': '经营活动产生的现金流量净额同比增长率(%)',    'roe_yoy': '净资产收益率(摊薄)同比增长率(%)',    'bps_yoy': '每股净资产相对年初增长率(%)',
    'assets_yoy': '资产总计相对年初增长率(%)',    'eqt_yoy': '归属母公司的股东权益相对年初增长率(%)',    'tr_yoy': '营业总收入同比增长率(%)',    'or_yoy': '营业收入同比增长率(%)',    'q_gr_yoy': '营业总收入同比增长率(%)(单季度)',
    'q_gr_qoq': '营业总收入环比增长率(%)(单季度)',    'q_sales_yoy': '营业收入同比增长率(%)(单季度)',    'q_sales_qoq': '营业收入环比增长率(%)(单季度)',    'q_op_yoy': '营业利润同比增长率(%)(单季度)',
    'q_op_qoq': '营业利润环比增长率(%)(单季度)',    'q_profit_yoy': '净利润同比增长率(%)(单季度)',    'q_profit_qoq': '净利润环比增长率(%)(单季度)',    'q_netprofit_yoy': '归属母公司股东的净利润同比增长率(%)(单季度)',
    'q_netprofit_qoq': '归属母公司股东的净利润环比增长率(%)(单季度)',    'equity_yoy': '净资产同比增长率',    'rd_exp': '研发费用'}
    return indicatorNameList[indicator]

def getFinanceIndicatorList():
    return {'eps': '基本每股收益',    'dt_eps': '稀释每股收益',    'total_revenue_ps': '每股营业总收入',    'revenue_ps': '每股营业收入',
    'capital_rese_ps': '每股资本公积',    'surplus_rese_ps': '每股盈余公积',    'undist_profit_ps': '每股未分配利润',    'extra_item': '非经常性损益',    'profit_dedt': '扣除非经常性损益后的净利润',    'gross_margin': '毛利',
    'current_ratio': '流动比率',    'quick_ratio': '速动比率',    'cash_ratio': '保守速动比率',    'invturn_days': '存货周转天数',    'arturn_days': '应收账款周转天数',    'inv_turn': '存货周转率',    'ar_turn': '应收账款周转率',
    'ca_turn': '流动资产周转率',    'fa_turn': '固定资产周转率',    'assets_turn': '总资产周转率',    'op_income': '经营活动净收益',    'valuechange_income': '价值变动净收益',    'interst_income': '利息费用',    'daa': '折旧与摊销',
    'ebit': '息税前利润',    'ebitda': '息税折旧摊销前利润',    'fcff': '企业自由现金流量',    'fcfe': '股权自由现金流量',    'current_exint': '无息流动负债',    'noncurrent_exint': '无息非流动负债',    'interestdebt': '带息债务',
    'netdebt': '净债务',    'tangible_asset': '有形资产',    'working_capital': '营运资金',    'networking_capital': '营运流动资本',    'invest_capital': '全部投入资本',    'retained_earnings': '留存收益',    'diluted2_eps': '期末摊薄每股收益',
    'bps': '每股净资产',    'ocfps': '每股经营活动产生的现金流量净额',    'retainedps': '每股留存收益',    'cfps': '每股现金流量净额',    'ebit_ps': '每股息税前利润',    'fcff_ps': '每股企业自由现金流量',    'fcfe_ps': '每股股东自由现金流量',
    'netprofit_margin': '销售净利率',    'grossprofit_margin': '销售毛利率',    'cogs_of_sales': '销售成本率',    'expense_of_sales': '销售期间费用率',    'profit_to_gr': '净利润/营业总收入',    'saleexp_to_gr': '销售费用/营业总收入',
    'adminexp_of_gr': '管理费用/营业总收入',    'finaexp_of_gr': '财务费用/营业总收入',    'impai_ttm': '资产减值损失/营业总收入',    'gc_of_gr': '营业总成本/营业总收入',    'op_of_gr': '营业利润/营业总收入',    'ebit_of_gr': '息税前利润/营业总收入',
    'roe': '净资产收益率',    'roe_waa': '加权平均净资产收益率',    'roe_dt': '净资产收益率(扣除非经常损益)',    'roa': '总资产报酬率',    'npta': '总资产净利润',    'roic': '投入资本回报率',    'roe_yearly': '年化净资产收益率',
    'roa2_yearly': '年化总资产报酬率',    'roe_avg': '平均净资产收益率(增发条件)',    'opincome_of_ebt': '经营活动净收益/利润总额',    'investincome_of_ebt': '价值变动净收益/利润总额',    'n_op_profit_of_ebt': '营业外收支净额/利润总额',
    'tax_to_ebt': '所得税/利润总额',    'dtprofit_to_profit': '扣除非经常损益后的净利润/净利润',    'salescash_to_or': '销售商品提供劳务收到的现金/营业收入',    'ocf_to_or': '经营活动产生的现金流量净额/营业收入',    'ocf_to_opincome': '经营活动产生的现金流量净额/经营活动净收益',
    'capitalized_to_da': '资本支出/折旧和摊销',    'debt_to_assets': '资产负债率',    'assets_to_eqt': '权益乘数',    'dp_assets_to_eqt': '权益乘数(杜邦分析)',    'ca_to_assets': '流动资产/总资产',    'nca_to_assets': '非流动资产/总资产',
    'tbassets_to_totalassets': '有形资产/总资产',    'int_to_talcap': '带息债务/全部投入资本',    'eqt_to_talcapital': '归属于母公司的股东权益/全部投入资本',    'currentdebt_to_debt': '流动负债/负债合计',    'longdeb_to_debt': '非流动负债/负债合计',
    'ocf_to_shortdebt': '经营活动产生的现金流量净额/流动负债',    'debt_to_eqt': '产权比率',    'eqt_to_debt': '归属于母公司的股东权益/负债合计',    'eqt_to_interestdebt': '归属于母公司的股东权益/带息债务',    'tangibleasset_to_debt': '有形资产/负债合计',
    'tangasset_to_intdebt': '有形资产/带息债务',    'tangibleasset_to_netdebt': '有形资产/净债务',    'ocf_to_debt': '经营活动产生的现金流量净额/负债合计',    'ocf_to_interestdebt': '经营活动产生的现金流量净额/带息债务',
    'ocf_to_netdebt': '经营活动产生的现金流量净额/净债务',    'ebit_to_interest': '已获利息倍数(EBIT/利息费用)',    'longdebt_to_workingcapital': '长期债务与营运资金比率',    'ebitda_to_debt': '息税折旧摊销前利润/负债合计',
    'turn_days': '营业周期',    'roa_yearly': '年化总资产净利率',    'roa_dp': '总资产净利率(杜邦分析)',    'fixed_assets': '固定资产合计',    'profit_prefin_exp': '扣除财务费用前营业利润',    'non_op_profit': '非营业利润',
    'op_to_ebt': '营业利润／利润总额',    'nop_to_ebt': '非营业利润／利润总额',    'ocf_to_profit': '经营活动产生的现金流量净额／营业利润',    'cash_to_liqdebt': '货币资金／流动负债',    'cash_to_liqdebt_withinterest': '货币资金／带息流动负债',
    'op_to_liqdebt': '营业利润／流动负债',    'op_to_debt': '营业利润／负债合计',    'roic_yearly': '年化投入资本回报率',    'total_fa_trun': '固定资产合计周转率',    'profit_to_op': '利润总额／营业收入',    'q_opincome': '经营活动单季度净收益',
    'q_investincome': '价值变动单季度净收益',    'q_dtprofit': '扣除非经常损益后的单季度净利润',    'q_eps': '每股收益(单季度)',    'q_netprofit_margin': '销售净利率(单季度)',    'q_gsprofit_margin': '销售毛利率(单季度)',
    'q_exp_to_sales': '销售期间费用率(单季度)',    'q_profit_to_gr': '净利润／营业总收入(单季度)',    'q_saleexp_to_gr': '销售费用／营业总收入 (单季度)',    'q_adminexp_to_gr': '管理费用／营业总收入 (单季度)',    'q_finaexp_to_gr': '财务费用／营业总收入 (单季度)',
    'q_impair_to_gr_ttm': '资产减值损失／营业总收入(单季度)',    'q_gc_to_gr': '营业总成本／营业总收入 (单季度)',    'q_op_to_gr': '营业利润／营业总收入(单季度)',    'q_roe': '净资产收益率(单季度)',    'q_dt_roe': '净资产单季度收益率(扣除非经常损益)',
    'q_npta': '总资产净利润(单季度)',    'q_opincome_to_ebt': '经营活动净收益／利润总额(单季度)',    'q_investincome_to_ebt': '价值变动净收益／利润总额(单季度)',    'q_dtprofit_to_profit': '扣除非经常损益后的净利润／净利润(单季度)',
    'q_salescash_to_or': '销售商品提供劳务收到的现金／营业收入(单季度)',    'q_ocf_to_sales': '经营活动产生的现金流量净额／营业收入(单季度)',    'q_ocf_to_or': '经营活动产生的现金流量净额／经营活动净收益(单季度)',    'basic_eps_yoy': '基本每股收益同比增长率(%)',
    'dt_eps_yoy': '稀释每股收益同比增长率(%)',    'cfps_yoy': '每股经营活动产生的现金流量净额同比增长率(%)',    'op_yoy': '营业利润同比增长率(%)',    'ebt_yoy': '利润总额同比增长率(%)',    'netprofit_yoy': '归属母公司股东的净利润同比增长率(%)',
    'dt_netprofit_yoy': '归属母公司股东的净利润-扣除非经常损益同比增长率(%)',    'ocf_yoy': '经营活动产生的现金流量净额同比增长率(%)',    'roe_yoy': '净资产收益率(摊薄)同比增长率(%)',    'bps_yoy': '每股净资产相对年初增长率(%)',
    'assets_yoy': '资产总计相对年初增长率(%)',    'eqt_yoy': '归属母公司的股东权益相对年初增长率(%)',    'tr_yoy': '营业总收入同比增长率(%)',    'or_yoy': '营业收入同比增长率(%)',    'q_gr_yoy': '营业总收入同比增长率(%)(单季度)',
    'q_gr_qoq': '营业总收入环比增长率(%)(单季度)',    'q_sales_yoy': '营业收入同比增长率(%)(单季度)',    'q_sales_qoq': '营业收入环比增长率(%)(单季度)',    'q_op_yoy': '营业利润同比增长率(%)(单季度)',
    'q_op_qoq': '营业利润环比增长率(%)(单季度)',    'q_profit_yoy': '净利润同比增长率(%)(单季度)',    'q_profit_qoq': '净利润环比增长率(%)(单季度)',    'q_netprofit_yoy': '归属母公司股东的净利润同比增长率(%)(单季度)',
    'q_netprofit_qoq': '归属母公司股东的净利润环比增长率(%)(单季度)',    'equity_yoy': '净资产同比增长率',    'rd_exp': '研发费用'}

##########################################################################
def getAllModels():
    all_models = apps.get_models();
    for model in all_models:
        print(model)

    #all_models = apps.get_app_config('blog').get_models()

    # name是表名，fields是字段，app_label是你的应用名(如：flow)，module是应用下的模型（如:flow.models）,options是元类选项
def custom_model(name, fields=None, app_label='', module='', options=None):
    class Meta:  # 模型类的Meta类
        db_table = name

    if app_label:  # 必须在元类中设置app_label，相关属性可参考https://www.cnblogs.com/lcchuguo/p/4754485.html
        setattr(Meta, 'app_label', app_label)  # 更新元类的选项

    if options is not None:
        for key, value in options.items():
            setattr(Meta, key, value)  # 设置模型的属性
        attrs = {'__module__': module, 'Meta': Meta}  # 添加字段属性
    if fields:
        attrs.update(fields)  # 创建模型类对象

    return type(name, (models.Model,), attrs)  # 用type动态创建类

#@staticmethod
def is_exists(db_table):
        return db_table in connection.introspection.table_names()

def createTable(custom_model):
    from django.db import connection
    from django.db.backends.base.schema import BaseDatabaseSchemaEditor
    with BaseDatabaseSchemaEditor(connection) as editor:
        editor.create_model(model=custom_model)

def updateIncomeTableForStock(stockCode, recordsTitle, values):
    getAllModels()
    fields = {
        "ts_code" : models.CharField('ts_code',max_length=10),
        "ann_date" : models.CharField('ann_date', max_length=8,null=True,blank=True),
        "f_ann_date" : models.CharField('f_ann_date', max_length=8,null=True,blank=True),
        "end_date" : models.CharField('end_date', max_length=8,null=True,blank=True),
        "report_type" : models.CharField('report_type', max_length=2,null=True,blank=True),
        "comp_type" : models.CharField('comp_type', max_length=1,null=True,blank=True),
        "basic_eps" : models.FloatField('basic_eps',null=True,blank=True),
        "diluted_eps" : models.FloatField('diluted_eps',null=True,blank=True),
        "total_revenue" : models.FloatField('total_revenue',null=True,blank=True),
        "revenue" : models.FloatField('revenue',null=True,blank=True),
        "int_income" : models.FloatField('int_income',null=True,blank=True),
        "prem_earned" : models.FloatField('prem_earned',null=True,blank=True),
        "comm_income" : models.FloatField('comm_income',null=True,blank=True),
        "n_commis_income" : models.FloatField('n_commis_income',null=True,blank=True),
        "n_oth_income" : models.FloatField('n_oth_income',null=True,blank=True),
        "n_oth_b_income" : models.FloatField('n_oth_b_income',null=True,blank=True),
        "prem_income" : models.FloatField('prem_income',null=True,blank=True),
        "out_prem" : models.FloatField('out_prem',null=True,blank=True),
        "une_prem_reser" : models.FloatField('une_prem_reser',null=True,blank=True),
        "reins_income" : models.FloatField('reins_income',null=True,blank=True),
        "n_sec_tb_income" : models.FloatField('n_sec_tb_income',null=True,blank=True),
        "n_sec_uw_income" : models.FloatField('n_sec_uw_income',null=True,blank=True),
        "n_asset_mg_income" : models.FloatField('n_asset_mg_income',null=True,blank=True),
        "oth_b_income" : models.FloatField('oth_b_income',null=True,blank=True),
        "fv_value_chg_gain" : models.FloatField('fv_value_chg_gain',null=True,blank=True),
        "invest_income" : models.FloatField('invest_income',null=True,blank=True),
        "ass_invest_income" : models.FloatField('ass_invest_income',null=True,blank=True),
        "forex_gain" : models.FloatField('forex_gain',null=True,blank=True),
        "total_cogs" : models.FloatField('total_cogs',null=True,blank=True),
        "oper_cost" : models.FloatField('oper_cost',null=True,blank=True),
        "int_exp" : models.FloatField('int_exp',null=True,blank=True),
        "comm_exp" : models.FloatField('comm_exp',null=True,blank=True),
        "biz_tax_surchg" : models.FloatField('biz_tax_surchg',null=True,blank=True),
        "sell_exp" : models.FloatField('sell_exp',null=True,blank=True),
        "admin_exp" : models.FloatField('admin_exp',null=True,blank=True),
        "fin_exp" : models.FloatField('fin_exp',null=True,blank=True),
        "assets_impair_loss" : models.FloatField('assets_impair_loss',null=True,blank=True),
        "prem_refund" : models.FloatField('prem_refund',null=True,blank=True),
        "compens_payout" : models.FloatField('compens_payout',null=True,blank=True),
        "reser_insur_liab" : models.FloatField('reser_insur_liab',null=True,blank=True),
        "div_payt" : models.FloatField('div_payt',null=True,blank=True),
        "reins_exp" : models.FloatField('reins_exp',null=True,blank=True),
        "oper_exp" : models.FloatField('oper_exp',null=True,blank=True),
        "compens_payout_refu" : models.FloatField('compens_payout_refu',null=True,blank=True),
        "insur_reser_refu" : models.FloatField('insur_reser_refu',null=True,blank=True),
        "reins_cost_refund" : models.FloatField('reins_cost_refund',null=True,blank=True),
        "other_bus_cost" : models.FloatField('other_bus_cost',null=True,blank=True),
        "operate_profit" : models.FloatField('operate_profit',null=True,blank=True),
        "non_oper_income" : models.FloatField('non_oper_income',null=True,blank=True),
        "non_oper_exp" : models.FloatField('non_oper_exp',null=True,blank=True),
        "nca_disploss" : models.FloatField('nca_disploss',null=True,blank=True),
        "total_profit" : models.FloatField('total_profit',null=True,blank=True),
        "income_tax" : models.FloatField('income_tax',null=True,blank=True),
        "n_income" : models.FloatField('n_income',null=True,blank=True),
        "n_income_attr_p" : models.FloatField('n_income_attr_p',null=True,blank=True),
        "minority_gain" : models.FloatField('minority_gain',null=True,blank=True),
        "oth_compr_income" : models.FloatField('oth_compr_income',null=True,blank=True),
        "t_compr_income" : models.FloatField('t_compr_income',null=True,blank=True),
        "compr_inc_attr_p" : models.FloatField('compr_inc_attr_p',null=True,blank=True),
        "compr_inc_attr_m_s" : models.FloatField('compr_inc_attr_m_s',null=True,blank=True),
        "ebit" : models.FloatField('ebit',null=True,blank=True),
        "ebitda" : models.FloatField('ebitda',null=True,blank=True),
        "insurance_exp" : models.FloatField('insurance_exp',null=True,blank=True),
        "undist_profit" : models.FloatField('undist_profit',null=True,blank=True),
        "distable_profit" : models.FloatField('distable_profit',null=True,blank=True),
        '__str__': lambda self: '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s '
                                '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s'
                                % (self.ts_code, self.ann_date, self.f_ann_date, self.end_date, self.report_type, self.comp_type, self.basic_eps,
                                   self.diluted_eps, self.total_revenue, self.revenue,self.int_income,self.prem_earned,self.comm_income,
                                   self.n_commis_income,self.n_oth_income,self.n_oth_b_income,self.prem_income,self.out_prem,self.une_prem_reser,self.reins_income,
                                   self.n_sec_tb_income,self.n_sec_uw_income,self.n_asset_mg_income,self.oth_b_income,self.fv_value_chg_gain,self.invest_income,
                                   self.ass_invest_income,self.forex_gain,self.total_cogs,self.oper_cost,self.int_exp,self.comm_exp,self.biz_tax_surchg,self.sell_exp,
                                   self.admin_exp,self.fin_exp,self.assets_impair_loss,self.prem_refund,self.compens_payout,self.reser_insur_liab,self.div_payt,
                                   self.reins_exp,self.oper_exp,self.compens_payout_refu,self.insur_reser_refu,self.reins_cost_refund,self.other_bus_cost,
                                   self.operate_profit,self.non_oper_income,self.non_oper_exp,self.nca_disploss,self.total_profit,self.income_tax,self.n_income,
                                   self.n_income_attr_p,self.minority_gain,self.oth_compr_income,self.t_compr_income,self.compr_inc_attr_p,self.compr_inc_attr_m_s,
                                   self.ebit,self.ebitda,self.insurance_exp,self.undist_profit,self.distable_profit)
    }
    stockIncomeTableName = 'incomeTable_%s' % str(stockCode)
    options = {
    #     'ordering': [
    #     "ann_date",
    #     "f_ann_date",
    #     "end_date",
    #     "report_type"
    # ],
        'verbose_name': stockIncomeTableName, }

    stockModel = custom_model(name=stockIncomeTableName, fields=fields, app_label='frontEnd',module='frontEnd.models', options=options)()

    print("===== stockCode:%s**********************\n", stockCode)
    #isinstance(stockModel, custom_model(name=stockIncomeTableName, fields=fields, app_label='frontEnd',module='frontEnd.models', options=options))
    if not is_exists(stockIncomeTableName):
        try:
            createTable(stockModel)
        except Exception as e:
            print(e)
    else:
        print("table is exists, don't need creat again")


    # print("=========================================\n")
    # print(df)
    # print("=========================================\n")
    # print(values)
    # print(type(stockModel))
    # print(stockModel)

    #for row in range(len(values)):
    col = 0
    for record in recordsTitle:
        if values[col] is not None:
            setattr(stockModel, record, values[col])
        col += 1
    stockModel.save()

def updateFinanceindicator(stockCode, values):
    fields = OrderedDict()
    fields["ts_code"] = models.CharField('ts_code',max_length=10)
    fields["ann_date"] = models.CharField('ann_date', max_length=8,null=True,blank=True)
    fields["end_date"] = models.CharField('end_date', max_length=8, null=True, blank=True)
    colIndex=0;
    recordsTitle = getRecordsTitleOfFinanceIndicator()
    for record in recordsTitle:
        colIndex += 1
        if colIndex  > 3:
         fields[record] = models.FloatField(record, null=True, blank=True)
    fields["__str__"] = "FinanceIndicator"
        # lambda self: '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s '
        #                         '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s'
        #                         '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s'
        #                         '%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s'
        #                         %(self.ts_code,self.ann_date,self.end_date,self.eps,self.dt_eps,self.total_revenue_ps,self.revenue_ps,self.capital_rese_ps,
        #                            self.surplus_rese_ps,self.undist_profit_ps,self.extra_item,self.profit_dedt,self.gross_margin,self.current_ratio,self.quick_ratio,
        #                            self.cash_ratio,self.invturn_days,self.arturn_days,self.inv_turn,self.ar_turn,self.ca_turn,self.fa_turn,self.assets_turn,self.op_income,
        #                            self.valuechange_income,self.interst_income,self.daa,self.ebit,self.ebitda,self.fcff,self.fcfe,self.current_exint,self.noncurrent_exint,
        #                            self.interestdebt,self.netdebt,self.tangible_asset,self.working_capital,self.networking_capital,self.invest_capital,self.retained_earnings,
        #                            self.diluted2_eps,self.bps,self.ocfps,self.retainedps,self.cfps,self.ebit_ps,self.fcff_ps,self.fcfe_ps,self.netprofit_margin,self.grossprofit_margin,
        #                            self.cogs_of_sales,self.expense_of_sales,self.profit_to_gr,self.saleexp_to_gr,self.adminexp_of_gr,self.finaexp_of_gr,self.impai_ttm,self.gc_of_gr,
        #                            self.op_of_gr,self.ebit_of_gr,self.roe,self.roe_waa,self.roe_dt,self.roa,self.npta,self.roic,self.roe_yearly,self.roa2_yearly,self.roe_avg,
        #                            self.opincome_of_ebt,self.investincome_of_ebt,self.n_op_profit_of_ebt,self.tax_to_ebt,self.dtprofit_to_profit,self.salescash_to_or,self.ocf_to_or,
        #                            self.ocf_to_opincome,self.capitalized_to_da,self.debt_to_assets,self.assets_to_eqt,self.dp_assets_to_eqt,self.ca_to_assets,self.nca_to_assets,
        #                            self.tbassets_to_totalassets,self.int_to_talcap,self.eqt_to_talcapital,self.currentdebt_to_debt,self.longdeb_to_debt,self.ocf_to_shortdebt,
        #                            self.debt_to_eqt,self.eqt_to_debt,self.eqt_to_interestdebt,self.tangibleasset_to_debt,self.tangasset_to_intdebt,self.tangibleasset_to_netdebt,
        #                            self.ocf_to_debt,self.ocf_to_interestdebt,self.ocf_to_netdebt,self.ebit_to_interest,self.longdebt_to_workingcapital,self.ebitda_to_debt,self.turn_days,
        #                            self.roa_yearly,self.roa_dp,self.fixed_assets,self.profit_prefin_exp,self.non_op_profit,self.op_to_ebt,self.nop_to_ebt,self.ocf_to_profit,
        #                            self.cash_to_liqdebt,self.cash_to_liqdebt_withinterest,self.op_to_liqdebt,self.op_to_debt,self.roic_yearly,self.total_fa_trun,self.profit_to_op,
        #                            self.q_opincome,self.q_investincome,self.q_dtprofit,self.q_eps,self.q_netprofit_margin,self.q_gsprofit_margin,self.q_exp_to_sales,self.q_profit_to_gr,
        #                            self.q_saleexp_to_gr,self.q_adminexp_to_gr,self.q_finaexp_to_gr,self.q_impair_to_gr_ttm,self.q_gc_to_gr,self.q_op_to_gr,self.q_roe,self.q_dt_roe,
        #                            self.q_npta,self.q_opincome_to_ebt,self.q_investincome_to_ebt,self.q_dtprofit_to_profit,self.q_salescash_to_or,self.q_ocf_to_sales,self.q_ocf_to_or,
        #                            self.basic_eps_yoy,self.dt_eps_yoy,self.cfps_yoy,self.op_yoy,self.ebt_yoy,self.netprofit_yoy,self.dt_netprofit_yoy,self.ocf_yoy,self.roe_yoy,self.bps_yoy,
        #                            self.assets_yoy,self.eqt_yoy,self.tr_yoy,self.or_yoy,self.q_gr_yoy,self.q_gr_qoq,self.q_sales_yoy,self.q_sales_qoq,self.q_op_yoy,self.q_op_qoq,
        #                            self.q_profit_yoy,self.q_profit_qoq,self.q_netprofit_yoy,self.q_netprofit_qoq,self.equity_yoy,self.rd_exp)

    stockFinanceIndicatorTableName = 'financeIndicatorTable_%s' % str(stockCode)
    options = {
    #     'ordering': [
    #     "ann_date",
    #     "f_ann_date",
    #     "end_date",
    #     "report_type"
    # ],
        'verbose_name': stockFinanceIndicatorTableName, }

    stockModel = custom_model(name=stockFinanceIndicatorTableName, fields=fields, app_label='frontEnd',module='frontEnd.models', options=options)()

    print("===== FinanceIndicator stockCode:", stockCode)
    #isinstance(stockModel, custom_model(name=stockIncomeTableName, fields=fields, app_label='frontEnd',module='frontEnd.models', options=options))
    if not is_exists(stockFinanceIndicatorTableName):
        try:
            createTable(stockModel)
        except Exception as e:
            print(e)
    else:
        print(stockFinanceIndicatorTableName+" table is exists, don't need creat again")

    dataByEndDate = custom_model(name=stockFinanceIndicatorTableName, fields=fields, app_label='frontEnd', module='frontEnd.models',
                 options=options).objects.filter(end_date=values[2])
    # print(len(list(dataByEndDate.values())))
    dataByEndDateList = list(dataByEndDate.values())
    if 0<len(dataByEndDateList):
        # print(values[0] + " already exist for" +  values[2])
        setattr(stockModel, 'id', dataByEndDateList[0]['id'])

    col = 0
    for record in recordsTitle:
        if values[col] is not None:
            setattr(stockModel, record, values[col])
        col += 1
    stockModel.save()

def queryFinancialIndicatorOneQuarter(stockCode, endDate):
    stockFinanceIndicatorTableName = 'financeIndicatorTable_%s' % str(stockCode)
    fields = OrderedDict()
    fields["ts_code"] = models.CharField('ts_code', max_length=10)
    fields["ann_date"] = models.CharField('ann_date', max_length=8, null=True, blank=True)
    fields["end_date"] = models.CharField('end_date', max_length=8, null=True, blank=True)
    colIndex = 0;
    recordsTitle = getRecordsTitleOfFinanceIndicator()
    for record in recordsTitle:
        colIndex += 1
        if colIndex > 3:
            fields[record] = models.FloatField(record, null=True, blank=True)
    fields["__str__"] = "FinanceIndicator"

    options = {
        #     'ordering': [
        #     "ann_date",
        #     "f_ann_date",
        #     "end_date",
        #     "report_type"
        # ],
        'verbose_name': stockFinanceIndicatorTableName, }

    items = custom_model(name=stockFinanceIndicatorTableName, fields=fields, app_label='frontEnd', module='frontEnd.models', options=options).objects.filter(end_date=endDate)

    dbData = list(items.values())
    return dbData

def queryFinanceindicator(stockCode, startDate, endDate, indicatorsList):
    fields = OrderedDict()
    fields["ts_code"] = models.CharField('ts_code', max_length=10)
    fields["ann_date"] = models.CharField('ann_date', max_length=8, null=True, blank=True)
    fields["end_date"] = models.CharField('end_date', max_length=8, null=True, blank=True)
    colIndex = 0;
    recordsTitle = getRecordsTitleOfFinanceIndicator()
    for record in recordsTitle:
        colIndex += 1
        if colIndex > 3:
            fields[record] = models.FloatField(record, null=True, blank=True)
    fields["__str__"] = "FinanceIndicator"
    stockFinanceIndicatorTableName = 'financeIndicatorTable_%s' % str(stockCode)
    options = {
        #     'ordering': [
        #     "ann_date",
        #     "f_ann_date",
        #     "end_date",
        #     "report_type"
        # ],
        'verbose_name': stockFinanceIndicatorTableName, }

    stockModel = custom_model(name=stockFinanceIndicatorTableName, fields=fields, app_label='frontEnd',
                              module='frontEnd.models', options=options)()

    col = 0
    # items = custom_model(name=stockFinanceIndicatorTableName, fields=fields, app_label='frontEnd',
    #                           module='frontEnd.models', options=options).filter(ts_code=stockCode, pub_date__gte=startDate, end_date__lte=endDate)
    items = custom_model(name=stockFinanceIndicatorTableName, fields=fields, app_label='frontEnd', module='frontEnd.models', options=options).objects.filter(end_date__gte=startDate,end_date__lte=endDate).order_by('end_date')
    #items = custom_model(name=stockFinanceIndicatorTableName, fields=fields, app_label='frontEnd', module='frontEnd.models', options=options).objects.filter(id=1)
    # print("============================== len:")
    # print(len(items))
    # print("============================== items.values():")
    # print(items.values())
    # print("============================== list items.values():")
    dbData = list(items.values())
    result = [[0 for col in range(len(indicatorsList))] for row in range(len(dbData))]
    if 0< len(dbData):
        for row in range(len(dbData)):
            for col in range(len(indicatorsList)):
                if col < 1 or indicatorsList[col] =="end_date":
                    result[row][col] = dbData[row][indicatorsList[col]]
                elif dbData[row][indicatorsList[col]] is not None:
                    result[row][col] = round(dbData[row][indicatorsList[col]], 2)
                else:
                    result[row][col] = 0
    return result


def updateAvgFinancialIndicatorsForIndustries(industryCode, endDate, values):
    fields = OrderedDict()
    fields["industryCode"] = models.CharField('industryCode', max_length=10)
    fields["end_date"] = models.CharField('end_date', max_length=8)
    recordsTitle = getRecordsTitleOfFinanceIndicator()
    skipNum = 3;
    for rIndex in range(len(recordsTitle)):
        if rIndex >= skipNum:
            fields[recordsTitle[rIndex]] = models.FloatField(recordsTitle[rIndex], null=True, blank=True)
    fields["__str__"] = "AvgFinancialIndicator"
    avgFinancialIndicatorTableName = 'avgFinancialIndicatorTable'
    options = {
        #     'ordering': [
        #     "ann_date",
        #     "f_ann_date",
        #     "end_date",
        #     "report_type"
        # ],
        'verbose_name': avgFinancialIndicatorTableName, }

    stockModel = custom_model(name=avgFinancialIndicatorTableName, fields=fields, app_label='frontEnd',
                              module='frontEnd.models', options=options)()
    if not is_exists(avgFinancialIndicatorTableName):
        try:
            createTable(stockModel)
        except Exception as e:
            aaaaaaa=0
            #print(e)
    else:
        bbbbbbbb = 0
        #print(avgFinancialIndicatorTableName + " table is exists, don't need creat again")

    setattr(stockModel, "industryCode", industryCode)
    setattr(stockModel, "end_date", endDate)
    for rIndex in range(len(recordsTitle)):
        if rIndex >= skipNum and values[rIndex-skipNum] is not None:
            setattr(stockModel, recordsTitle[rIndex], values[rIndex-skipNum])
    stockModel.save()

def queryAvgFinanceindicaIndustriesForIndustries(endDate, indicatorsList):
        fields = OrderedDict()
        fields["industryCode"] = models.CharField('industryCode', max_length=10)
        fields["end_date"] = models.CharField('end_date', max_length=8)
        recordsTitle = getRecordsTitleOfFinanceIndicator()
        skipNum = 3;
        for rIndex in range(len(recordsTitle)):
            if rIndex >= skipNum:
                fields[recordsTitle[rIndex]] = models.FloatField(recordsTitle[rIndex], null=True, blank=True)
        fields["__str__"] = "AvgFinancialIndicator"
        avgFinancialIndicatorTableName = 'avgFinancialIndicatorTable'
        options = {
            #     'ordering': [
            #     "ann_date",
            #     "f_ann_date",
            #     "end_date",
            #     "report_type"
            # ],
            'verbose_name': avgFinancialIndicatorTableName, }

        stockModel = custom_model(name=avgFinancialIndicatorTableName, fields=fields, app_label='frontEnd',
                                  module='frontEnd.models', options=options)()
        if not is_exists(avgFinancialIndicatorTableName):
            try:
                createTable(stockModel)
            except Exception as e:
            #   aaaaaaa = 0
                print(e)
        else:
            #bbbbbbbb = 0
            print(avgFinancialIndicatorTableName + " table is exists, don't need creat again")
        resultFields ="";
        for i in range(len(indicatorsList)):
            resultFields= resultFields + "'" +indicatorsList[i]+"'"

            if(i!=(len(indicatorsList)-1)):
                resultFields = resultFields + ','
        print(resultFields)
        datasDb = list(custom_model(name=avgFinancialIndicatorTableName, fields=fields, app_label='frontEnd',
                             module='frontEnd.models', options=options).objects.filter(end_date=endDate).values())
        print(datasDb[0])
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(len(indicatorsList))
        print(len(datasDb))
        result = [[0 for col in range(len(indicatorsList))] for row in range(len(datasDb))]
        for row in range(len(datasDb)):
            for col in range(len(indicatorsList)):
                if col<2:
                    result[row][col] = datasDb[row][indicatorsList[col]]
                else:
                    result[row][col] = round(datasDb[row][indicatorsList[col]],2)
        print(result)
        return result


def queryAvgFinancialIndicatorForOneIndustry(startDate,endDate, industryClassify, indicatorsList):
    print("queryAvgFinancialIndicatorForOneIndustry:")
    fields = OrderedDict()
    fields["industryCode"] = models.CharField('industryCode', max_length=10)
    fields["end_date"] = models.CharField('end_date', max_length=8)
    recordsTitle = getRecordsTitleOfFinanceIndicator()
    skipNum = 3;
    for rIndex in range(len(recordsTitle)):
        if rIndex >= skipNum:
            fields[recordsTitle[rIndex]] = models.FloatField(recordsTitle[rIndex], null=True, blank=True)
    fields["__str__"] = "AvgFinancialIndicator"
    avgFinancialIndicatorTableName = 'avgFinancialIndicatorTable'
    options = {
        #     'ordering': [
        #     "ann_date",
        #     "f_ann_date",
        #     "end_date",
        #     "report_type"
        # ],
        'verbose_name': avgFinancialIndicatorTableName, }

    stockModel = custom_model(name=avgFinancialIndicatorTableName, fields=fields, app_label='frontEnd',
                              module='frontEnd.models', options=options)()
    if not is_exists(avgFinancialIndicatorTableName):
        try:
            createTable(stockModel)
        except Exception as e:
            #   aaaaaaa = 0
            print(e)
    else:
        # bbbbbbbb = 0
        print(avgFinancialIndicatorTableName + " table is exists, don't need creat again")
    print("sfsfsfsfsfsfsfsfsfsfsf")
    print(industryClassify)
    datasDb = list(custom_model(name=avgFinancialIndicatorTableName, fields=fields, app_label='frontEnd',
                                module='frontEnd.models', options=options).objects.filter(end_date__gte=startDate,end_date__lte=endDate,industryCode=industryClassify).values())
                                # module='frontEnd.models', options=options).objects.filter(end_date__gte=startDate,end_date__lte=endDate,industryCode=industryClassify).values())
    print(datasDb[0])

    print(len(indicatorsList))
    print(len(datasDb))
    result = [[0 for col in range(len(indicatorsList))] for row in range(len(datasDb))]
    for row in range(len(datasDb)):
        for col in range(len(indicatorsList)):
            result[row][col] = datasDb[row][indicatorsList[col]]
    print(result)
    return result

    #return stockModel.filter(ts_code=stockCode, pub_date__gte=startDate, end_date__lte=endDate)
######################################################################
# def getIncomeTableModel(stockCode):
#     try:
#         from django.apps import apps
#         IncomeTableModel = apps.get_model('__main__', '_incomeTable' + stockCode)
#     except LookupError:
#         IncomeTableModel = get_incomeTable_model(stockCode)
#
#     if not IncomeTableModel.is_exists():
#         with connection.schema_editor() as schema_editor:
#             try:
#                 schema_editor.create_model(IncomeTableModel)
#             except Exception as e:
#                 print(e)
#     return IncomeTableModel
#
# def dataManagerUpdateIncomeTableForStock(stockCode, df):
#     #获取各字段的名字
#     recordsTitle = list(df.columns.values)
#     values = df.values.tolist()
#
#     incomeTableModelType =  getIncomeTableModel(stockCode)
#     incomeTableModelObj = incomeTableModelType(stockCode)
#
#     for row in range(len(values)):
#         col = 0
#         setattr(incomeTableModelObj, "id", row)
#         for record in recordsTitle:
#             setattr(incomeTableModelObj, record, values[row][col])
#             mystr = "record:" + record + " value:" + str(getattr(incomeTableModelObj, record))
#             print(mystr)
#             col += 1
#         incomeTableModelObj.save()


# 股票行情管理 --获取k线所需数据
def getIndexOrStock(type,ts_code, startDate, endDate):
    #输出 trade_date      close       open       high        low    vol(成交量（手）)
    print(ts_code)
    print(startDate)
    print(endDate)
    print(type)
    df = ts.pro_bar(ts_code=ts_code, adj='qfq', asset=type, start_date=startDate,end_date=endDate)
    print("aaaaaaaaaaaaaaaaaaaaa\n")
    print(df)
    df.drop(columns=["ts_code",'pre_close','change','pct_chg','amount'], inplace=True)
    #if(type=='I'):#从tushare查询出的指数数据顺序与股票的交易数据不一样，需要通过下面的方法排一下序
    cols = ['trade_date','open','close','low','high','vol']
    df = df.loc[:, cols]
    datas = df.values.tolist()
    datas.reverse()
    return datas

# 股票行情管理 --获取k线Month
def getIndexOrStockWeekly(type,ts_code, startDate, endDate):
    #输出 trade_date      close       open       high        low    vol(成交量（手）)
    if (type == 'E'):
        df = pro.weekly(ts_code=ts_code, start_date=startDate, end_date=endDate,
                         fields='ts_code,trade_date,open,high,low,close,vol,amount')
    if (type == 'I'):
        df = pro.index_weekly(ts_code=ts_code, start_date=startDate, end_date=endDate,
                               fields='ts_code,trade_date,open,high,low,close,vol,amount')
    cols = ['trade_date','open','close','low','high','vol']
    df = df.loc[:, cols]
    datas = df.values.tolist()
    datas.reverse()
    return datas

# 股票行情管理 --获取k线Month
def getIndexOrStockMonthly(type,ts_code, startDate, endDate):
    #输出 trade_date      close       open       high        low    vol(成交量（手）)
    if (type == 'E'):
        df = pro.monthly(ts_code=ts_code, start_date=startDate, end_date=endDate,
                         fields='ts_code,trade_date,open,high,low,close,vol,amount')
    if (type == 'I'):
        df = pro.index_monthly(ts_code=ts_code, start_date=startDate, end_date=endDate,
                               fields='ts_code,trade_date,open,high,low,close,vol,amount')
    cols = ['trade_date','open','close','low','high','vol']
    df = df.loc[:, cols]
    datas = df.values.tolist()
    datas.reverse()
    return datas

def saveStockList(data):
    item = StockList()
    item.ts_code = data[0];
    item.symbol = data[1];
    item.name = data[2];
    item.area = data[3];
    item.industry = data[4];
    item.fullname = data[5];
    item.enname = data[6];
    item.market = data[7];
    item.exchange = data[8];
    item.curr_type = data[9];
    item.list_status = data[10];
    item.list_date = data[11];
    item.delist_date = data[12];
    item.is_hs = data[13];
    item.save()

def getStocksName():
    items = StockList.objects.all().values()
    stocksNameList={}
    for item in items:
        stocksNameList[item['ts_code']]=item['name']
    return stocksNameList

def getMACD(closes, tradingCalendar):
    #closes = df['close'].values
    #print("=====getMACD:\n")
    #macd【DIF】 = 12【fastperiod】天EMA - 26【slowperiod】天EMA
    #macdsignal【DEA或DEM】 = 计算macd的signalperiod天的EMA
    #macdhist【MACD柱状线】 = macd - macdsignal
    macd,macdsigna,macdhist = ta.MACD(np.array(closes), fastperiod=12, slowperiod=26, signalperiod=9)
    for i in range(len(macd)):
        if np.isnan(np.mean(macd[i])):
            macd[i] = 0
        macd[i] = format(macd[i], '.2f')


    for i in range(len(macdsigna)):
        if np.isnan(np.mean(macdsigna[i])):
            macdsigna[i] = 0
        macdsigna[i] = format(macdsigna[i], '.2f')
    #np.c_[tradingCalendar,macdsigna]

    for i in range(len(macdhist)):
        if np.isnan(np.mean(macdhist[i])):
            macdhist[i] = 0
        macdhist[i] = format(macdhist[i], '.2f')
    return np.c_[tradingCalendar, macd].tolist() ,np.c_[tradingCalendar, macdsigna].tolist(), np.c_[tradingCalendar, macdhist].tolist()

