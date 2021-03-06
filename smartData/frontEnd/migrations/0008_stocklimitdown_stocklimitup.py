# Generated by Django 3.0.7 on 2020-07-12 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontEnd', '0007_auto_20200712_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='stockLimitDown',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('trade_date', models.CharField(max_length=8, verbose_name='date')),
                ('ts_code', models.CharField(max_length=10, verbose_name='ts_code')),
                ('ts_name', models.CharField(max_length=10, verbose_name='ts_name')),
                ('close', models.FloatField(verbose_name='close')),
                ('pct_chg', models.FloatField(verbose_name='pct_chg')),
                ('amp', models.FloatField(verbose_name='amp')),
                ('fc_ratio', models.FloatField(verbose_name='fc_ratio')),
                ('fl_ratio', models.FloatField(verbose_name='fl_ratio')),
                ('fd_amount', models.FloatField(verbose_name='fd_amount')),
                ('first_time', models.TimeField(verbose_name='first_time')),
                ('last_time', models.TimeField(verbose_name='last_time')),
                ('open_times', models.IntegerField(verbose_name='open_times')),
                ('strth', models.FloatField(verbose_name='strth')),
            ],
            options={
                'db_table': 'stockLimitDown',
            },
        ),
        migrations.CreateModel(
            name='StockLimitUp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('trade_date', models.CharField(max_length=8, verbose_name='date')),
                ('ts_code', models.CharField(max_length=10, verbose_name='ts_code')),
                ('ts_name', models.CharField(max_length=10, verbose_name='ts_name')),
                ('close', models.FloatField(verbose_name='close')),
                ('pct_chg', models.FloatField(verbose_name='pct_chg')),
                ('amp', models.FloatField(verbose_name='amp')),
                ('fc_ratio', models.FloatField(verbose_name='fc_ratio')),
                ('fl_ratio', models.FloatField(verbose_name='fl_ratio')),
                ('fd_amount', models.FloatField(verbose_name='fd_amount')),
                ('first_time', models.TimeField(verbose_name='first_time')),
                ('last_time', models.TimeField(verbose_name='last_time')),
                ('open_times', models.IntegerField(verbose_name='open_times')),
                ('strth', models.FloatField(verbose_name='strth')),
            ],
            options={
                'db_table': 'stockLimitUp',
            },
        ),
    ]
