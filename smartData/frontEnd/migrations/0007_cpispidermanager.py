# Generated by Django 3.0.1 on 2020-05-02 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontEnd', '0006_pmimanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='CpiSpiderManager',
            fields=[
                ('date', models.CharField(max_length=10, primary_key=True, serialize=False, verbose_name='time')),
                ('value', models.FloatField(verbose_name='value')),
            ],
            options={
                'db_table': 'cpidatatable',
            },
        ),
    ]