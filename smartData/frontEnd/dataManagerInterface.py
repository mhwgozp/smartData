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

ts.set_token('abc23dc1908af03d82e14f830e52e28300ef5ac69bb5fe14e2ba8630')
pro = ts.pro_api()

def dataManagerStoreStockLimitUp(data):
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

def dataManagerStoreStockLimitDown(data):
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

def dataManagerNumOfStockLimitUpDown(data):
    item = NumOfStockLimitUpDown()
    item.trade_date = data[0]
    item.NumOfLimitUp = data[1]
    item.NumOfLimitDown = data[2]
    item.save()

def dataManagerIndustryClassify(data):
    item = IndustryClassify()
    item.industryCode = data[0]
    item.industryName = data[1]
    item.industryLevel = data[2]
    item.save()

def dataManagerGetIndustryClassify():
    #items = IndustryClassify.objects.filter(industryLevel="L3" and id )
    items = IndustryClassify.objects.filter(id__gte=342)
    return items.values()

def dataManagerStockListOfdustryClassify(data):
    item = StockListOfdustryClassify()
    item.industryCode = data[0];
    item.stockCode = data[1];
    item.inDate = data[2];
    item.outDate = data[3];
    item.save()

def dataManagerGetStockListOfdustryClassify(industryCode):
    items = StockListOfdustryClassify.objects.filter(industryCode=industryCode)
    return items.values()

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

def dataManagerUpdateIncomeTableForStock(stockCode, recordsTitle, values):
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

def dataManagerUpdateFinanceindicator(stockCode, recordsTitle, values):
    fields = OrderedDict()
    fields["ts_code"] = models.CharField('ts_code',max_length=10)
    fields["ann_date"] = models.CharField('ann_date', max_length=8,null=True,blank=True)
    fields["end_date"] = models.CharField('end_date', max_length=8, null=True, blank=True)
    colIndex=0;
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

    print("===== FinanceIndicator stockCode:%s**********************\n", stockCode)
    #isinstance(stockModel, custom_model(name=stockIncomeTableName, fields=fields, app_label='frontEnd',module='frontEnd.models', options=options))
    if not is_exists(stockFinanceIndicatorTableName):
        try:
            createTable(stockModel)
        except Exception as e:
            print(e)
    else:
        print(stockFinanceIndicatorTableName+" table is exists, don't need creat again")

    col = 0
    for record in recordsTitle:
        if values[col] is not None:
            setattr(stockModel, record, values[col])
        col += 1
    stockModel.save()

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

