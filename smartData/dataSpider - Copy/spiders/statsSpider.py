from scrapy.spiders import Spider
import sys

sys.path.append("C:\smartData\smartData\dataSpider\spiders")
#sys.path.append(r"C:\smartData\smartData\dataSpider\dataSpider\spiders\")

#from scrapy.selector import Selector
#from scrapyspider.items import CninfoItem

from scrapy.http import Request
#from scrapy.http import FormRequest
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
#import urllib2
import json
import datetime
import time
import os

def gettime():
    return int(round(time.time() * 1000))
  
class statsSpider(Spider):
    name = "statsSpider"
    allowed_domains = ["stats.gov.cn"]
    #start_urls = ['http://data.stats.gov.cn/easyquery.htm?cn=B01']
    start_urls = ['http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgjd&rowcode=zb&colcode=sj&wds=%5B%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0101%22%7D%5D']

    def parse(self, response):
            #print(response.body)

            print(response.headers)
            if 0 < response.url.find('valuecode%22%3A%22A0101'):
                print("******************* to query all data ******************")
                setCookie = response.headers['Set-Cookie'].decode('ascii');
                jsessionIdStartPos = setCookie.find('=')
                jsessionIdEndPos = setCookie.find(';')
                jsessionId = setCookie[jsessionIdStartPos+1:jsessionIdEndPos]
                url = "http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgjd&rowcode=sj&colcode=zb&wds=%5B%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%221949-%2Clast10%22%7D%5D&k1=" + str(
                    gettime())

                #yield Request(url, callback=self.parse, headers=heads)
                yield Request(url, callback=self.parse, meta={'jsessionId':jsessionId})
            else:
                print("******************* all data responsed******************")
                gdbData = json.loads(response.body)["returndata"]
                for i in gdbData['wdnodes'][0]['nodes']:
                    print(i['cname'])




                #yield Request()

      
