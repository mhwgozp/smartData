# Generated by Django 3.0.7 on 2020-10-31 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontEnd', '0013_auto_20200726_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_code', models.CharField(max_length=10, verbose_name='ts_code')),
                ('symbol', models.CharField(max_length=7, verbose_name='symbol')),
                ('name', models.CharField(max_length=10, verbose_name='symbol')),
                ('area', models.CharField(blank=True, max_length=10, null=True, verbose_name='area')),
                ('industry', models.CharField(blank=True, max_length=10, null=True, verbose_name='industry')),
                ('fullname', models.CharField(blank=True, max_length=30, null=True, verbose_name='fullname')),
                ('enname', models.CharField(blank=True, max_length=100, null=True, verbose_name='enname')),
                ('market', models.CharField(blank=True, max_length=6, null=True, verbose_name='market')),
                ('exchange', models.CharField(blank=True, max_length=10, null=True, verbose_name='exchange')),
                ('curr_type', models.CharField(blank=True, max_length=6, null=True, verbose_name='curr_type')),
                ('list_status', models.CharField(blank=True, max_length=6, null=True, verbose_name='list_status')),
                ('list_date', models.CharField(blank=True, max_length=8, null=True, verbose_name='list_date')),
                ('delist_date', models.CharField(blank=True, max_length=8, null=True, verbose_name='delist_date')),
                ('is_hs', models.CharField(blank=True, max_length=2, null=True, verbose_name='is_hs')),
            ],
            options={
                'db_table': 'StockList',
            },
        ),
    ]
