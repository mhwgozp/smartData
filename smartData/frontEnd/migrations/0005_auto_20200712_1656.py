# Generated by Django 3.0.7 on 2020-07-12 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontEnd', '0004_auto_20200712_1654'),
    ]

    operations = [
        migrations.DeleteModel(
            name='stockLimitDown',
        ),
        migrations.DeleteModel(
            name='StockLimitUp',
        ),
    ]