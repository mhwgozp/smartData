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
import talib as ta
from talib import MA_Type

ts.set_token('abc23dc1908af03d82e14f830e52e28300ef5ac69bb5fe14e2ba8630')
pro = ts.pro_api()

def sectors(request):

    return render(request, "sectors.html", {})