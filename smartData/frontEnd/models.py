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