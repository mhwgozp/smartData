# Generated by Django 3.0.7 on 2020-10-31 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontEnd', '0017_delete_stocklistofdustryclassify'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockListOfdustryClassify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industryCode', models.CharField(max_length=10, verbose_name='industryCode')),
                ('stockCode', models.CharField(max_length=10, unique=True, verbose_name='stockCode')),
                ('inDate', models.CharField(max_length=8, verbose_name='in_date')),
                ('outDate', models.CharField(blank=True, max_length=8, null=True, verbose_name='out_date')),
            ],
            options={
                'db_table': 'stockListOfdustryClassify',
            },
        ),
    ]
