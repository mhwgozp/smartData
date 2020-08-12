from django.db import models
from django.db import connection, migrations, models
from django.db.migrations.executor import MigrationExecutor
# Create your models here.

class ReserveRequirementManager(models.Model):
    date = models.DateField('date', primary_key=True)
    bigFinancialInstitutionsValue = models.FloatField('bigFinancialInstitutionsValue')
    smallMediumFinancialInstitutionsValue = models.FloatField('smallMediumFinancialInstitutionsValue')
    publicDate = models.DateField('publicDate',null=True,blank=True)

    class Meta:
        db_table = 'reserveRequirement'

class CpiManager(models.Model):
    date = models.DateField('date', primary_key=True)
    value = models.FloatField('value')

    publicDate = models.DateField('publicDate',null=True,blank=True)

    class Meta:
        db_table = 'cpi'

class PpiManager(models.Model):
    date = models.DateField('date', primary_key=True)
    value = models.FloatField('value')
    publicDate = models.DateField('publicDate',null=True,blank=True)

    class Meta:
        db_table = 'ppi'

class PmiManager(models.Model):
    date = models.DateField('date', primary_key=True)
    manufacturingValue = models.FloatField('manufacturingValue')
    nonManufacturingValue = models.FloatField('nonManufacturingValue')
    publicDate = models.DateField('publicDate',null=True,blank=True)

    class Meta:
        db_table = 'pmi'

class MoneySupplyDb(models.Model):
    #货币和准货币(M2) 供应量 期末值(亿元)
    #货币和准货币(M2) 供应量 同比增长( %)
    #货币(M1) 供应量 期末值(亿元)
    #货币(M1) 供应量 同比增长( %)    5.0
    #流通中现金(M0) 供应量 期末值(亿元)
    #流通中现金(M0) 供应量 同比增长( %)
    time = models.CharField('time',max_length=8, primary_key=True)
    m2Value = models.FloatField('m2Value')
    m2YOY = models.FloatField('m2YOY')
    m1Value = models.FloatField('m1Value')
    m1YOY = models.FloatField('m1YOY')
    m0Value = models.FloatField('m0Value')
    m0YOY = models.FloatField('m0YOY')
    publicDate = models.DateField('publicDate', null=True, blank=True)

    class Meta:
        db_table = 'MoneySupply'

class StockLimitUp(models.Model):
    #交易日期
    #trade_date = models.DateField('date', primary_key=True)
    id = models.AutoField(primary_key=True)
    trade_date = models.CharField('date',max_length=8)
    ts_code = models.CharField('ts_code',max_length=10)
    ts_name = models.CharField('ts_name', max_length=10)

    #收盘价
    close = models.FloatField('close')

    #涨跌幅
    pct_chg = models.FloatField('pct_chg',blank=True,null=True)

    #振幅
    amp = models.FloatField('amp',blank=True,null=True)

    #封单金额 / 日成交金额
    fc_ratio = models.FloatField('fc_ratio',blank=True,null=True)

    # 封单手数 / 流通股本
    fl_ratio = models.FloatField('fl_ratio',blank=True,null=True)

    # 封单金额
    fd_amount = models.FloatField('fd_amount',blank=True,null=True)

    # 首次涨停时间
    first_time = models.TimeField('first_time',blank=True,null=True)

    # 最后封板时间
    last_time = models.TimeField('last_time',blank=True,null=True)

    # 打开次数
    open_times = models.IntegerField('open_times',blank=True,null=True)

    # 涨跌停强度
    strth = models.FloatField('strth',blank=True,null=True)

    class Meta:
        db_table = 'stockLimitUp'

class StockLimitDown(models.Model):
    #交易日期
    #trade_date = models.DateField('date', primary_key=True)
    id = models.AutoField(primary_key=True)
    trade_date = models.CharField('date', max_length=8)
    ts_code = models.CharField('ts_code',max_length=10)
    ts_name = models.CharField('ts_name', max_length=10)

    # 收盘价
    close = models.FloatField('close')

    # 涨跌幅
    pct_chg = models.FloatField('pct_chg', blank=True, null=True)

    # 振幅
    amp = models.FloatField('amp', blank=True, null=True)

    # 封单金额 / 日成交金额
    fc_ratio = models.FloatField('fc_ratio', blank=True, null=True)

    # 封单手数 / 流通股本
    fl_ratio = models.FloatField('fl_ratio', blank=True, null=True)

    # 封单金额
    fd_amount = models.FloatField('fd_amount', blank=True, null=True)

    # 首次涨停时间
    first_time = models.TimeField('first_time', blank=True, null=True)

    # 最后封板时间
    last_time = models.TimeField('last_time', blank=True, null=True)

    # 打开次数
    open_times = models.IntegerField('open_times', blank=True, null=True)

    # 涨跌停强度
    strth = models.FloatField('strth', blank=True, null=True)

    class Meta:
        db_table = 'stockLimitDown'

class NumOfStockLimitUpDown(models.Model):
    #交易日期
    trade_date = models.CharField('date', max_length=8, primary_key=True)
    NumOfLimitUp = models.IntegerField('NumOfLimitUp', blank=True, null=True)
    NumOfLimitDown = models.IntegerField('NumOfLimitDown', blank=True, null=True)
    class Meta:
        db_table = 'numOfStockLimitUpDown'

class IndustryClassify(models.Model):
    industryCode = models.CharField('industryCode', max_length=10, unique=True)
    industryName = models.CharField('industryName', blank=True, null=True, max_length=16)
    industryLevel = models.CharField('industryLevel', blank=True, null=True, max_length=2)
    class Meta:
        db_table = 'industryClassify'

class StockListOfdustryClassify(models.Model):
    industryCode = models.CharField('industryCode', max_length=10)
    stockCode = models.CharField('stockCode', blank=False, null=False, max_length=10, unique=True)
    inDate = models.CharField('in_date', blank=False, null=False, max_length=8)
    outDate = models.CharField('out_date', blank=True, null=True, max_length=8)
    class Meta:
        db_table = 'stockListOfdustryClassify'


def get_incomeTable_model(stockCode):
    table_name = 'incomeTable_%s' % str(stockCode)

    class IncomeTableMetaclass(models.base.ModelBase):
        def __new__(cls, name, bases, attrs):
            name += '_incomeTable'+stockCode  # 这是Model的name.
            print("aaaaaaaa new module:"+name+"\n")
            return models.base.ModelBase.__new__(cls, name, bases, attrs)

    class IncomeTableModel(models.Model):
        __metaclass__ = IncomeTableMetaclass
        id = models.AutoField('id',primary_key=True)
        ts_code = models.CharField('ts_code', max_length=10,null=True,blank=True)
        ann_date = models.CharField('ann_date', max_length=8)
        f_ann_date = models.CharField('f_ann_date', max_length=8)
        end_date = models.CharField('end_date', max_length=8)
        report_type = models.CharField('report_type', max_length=2)
        comp_type = models.CharField('comp_type', max_length=1)
        basic_eps = models.FloatField('basic_eps', null=True, blank=True)
        diluted_eps = models.FloatField('diluted_eps', null=True, blank=True)
        total_revenue = models.FloatField('total_revenue', null=True, blank=True)
        revenue = models.FloatField('revenue', null=True, blank=True)
        int_income = models.FloatField('int_income', null=True, blank=True)
        prem_earned = models.FloatField('prem_earned', null=True, blank=True)
        comm_income = models.FloatField('comm_income', null=True, blank=True)
        n_commis_income = models.FloatField('n_commis_income', null=True, blank=True)
        n_oth_income = models.FloatField('n_oth_income', null=True, blank=True)
        n_oth_b_income = models.FloatField('n_oth_b_income', null=True, blank=True)
        prem_income = models.FloatField('prem_income', null=True, blank=True)
        out_prem = models.FloatField('out_prem', null=True, blank=True)
        une_prem_reser = models.FloatField('une_prem_reser', null=True, blank=True)
        reins_income = models.FloatField('reins_income', null=True, blank=True)
        n_sec_tb_income = models.FloatField('n_sec_tb_income', null=True, blank=True)
        n_sec_uw_income = models.FloatField('n_sec_uw_income', null=True, blank=True)
        n_asset_mg_income = models.FloatField('n_asset_mg_income', null=True, blank=True)
        oth_b_income = models.FloatField('oth_b_income', null=True, blank=True)
        fv_value_chg_gain = models.FloatField('fv_value_chg_gain', null=True, blank=True)
        invest_income = models.FloatField('invest_income', null=True, blank=True)
        ass_invest_income = models.FloatField('ass_invest_income', null=True, blank=True)
        forex_gain = models.FloatField('forex_gain', null=True, blank=True)
        total_cogs = models.FloatField('total_cogs', null=True, blank=True)
        oper_cost = models.FloatField('oper_cost', null=True, blank=True)
        int_exp = models.FloatField('int_exp', null=True, blank=True)
        comm_exp = models.FloatField('comm_exp', null=True, blank=True)
        biz_tax_surchg = models.FloatField('biz_tax_surchg', null=True, blank=True)
        sell_exp = models.FloatField('sell_exp', null=True, blank=True)
        admin_exp = models.FloatField('admin_exp', null=True, blank=True)
        fin_exp = models.FloatField('fin_exp', null=True, blank=True)
        assets_impair_loss = models.FloatField('assets_impair_loss', null=True, blank=True)
        prem_refund = models.FloatField('prem_refund', null=True, blank=True)
        compens_payout = models.FloatField('compens_payout', null=True, blank=True)
        reser_insur_liab = models.FloatField('reser_insur_liab', null=True, blank=True)
        div_payt = models.FloatField('div_payt', null=True, blank=True)
        reins_exp = models.FloatField('reins_exp', null=True, blank=True)
        oper_exp = models.FloatField('oper_exp', null=True, blank=True)
        compens_payout_refu = models.FloatField('compens_payout_refu', null=True, blank=True)
        insur_reser_refu = models.FloatField('insur_reser_refu', null=True, blank=True)
        reins_cost_refund = models.FloatField('reins_cost_refund', null=True, blank=True)
        other_bus_cost = models.FloatField('other_bus_cost', null=True, blank=True)
        operate_profit = models.FloatField('operate_profit', null=True, blank=True)
        non_oper_income = models.FloatField('non_oper_income', null=True, blank=True)
        non_oper_exp = models.FloatField('non_oper_exp', null=True, blank=True)
        nca_disploss = models.FloatField('nca_disploss', null=True, blank=True)
        total_profit = models.FloatField('total_profit', null=True, blank=True)
        income_tax = models.FloatField('income_tax', null=True, blank=True)
        n_income = models.FloatField('n_income', null=True, blank=True)
        n_income_attr_p = models.FloatField('n_income_attr_p', null=True, blank=True)
        minority_gain = models.FloatField('minority_gain', null=True, blank=True)
        oth_compr_income = models.FloatField('oth_compr_income', null=True, blank=True)
        t_compr_income = models.FloatField('t_compr_income', null=True, blank=True)
        compr_inc_attr_p = models.FloatField('compr_inc_attr_p', null=True, blank=True)
        compr_inc_attr_m_s = models.FloatField('compr_inc_attr_m_s', null=True, blank=True)
        ebit = models.FloatField('ebit', null=True, blank=True)
        ebitda = models.FloatField('ebitda', null=True, blank=True)
        insurance_exp = models.FloatField('insurance_exp', null=True, blank=True)
        undist_profit = models.FloatField('undist_profit', null=True, blank=True)
        distable_profit = models.FloatField('distable_profit', null=True, blank=True)

        @staticmethod
        def is_exists():
            return table_name in connection.introspection.table_names()

        class Meta:
            db_table = table_name

    return IncomeTableModel