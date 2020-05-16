from django.db import models

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