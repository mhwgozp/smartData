from scrapy.spiders import Spider
import sys

sys.path.append("C:\smartData\smartData\dataSpider\spiders")
#sys.path.append(r"C:\smartData\smartData\dataSpider\dataSpider\spiders\")

#from scrapy.selector import Selector
#from scrapyspider.items import CninfoItem

from scrapy.http import Request
from scrapy.http import FormRequest
#from dataSpider.items import GdbCurrentPriceItem
import json
import datetime
import time
import os


def gettime():
    return int(round(time.time() * 1000))
  
class statsSpider(Spider):
    name = "statsSpider"
    allowed_domains = ["stats.gov.cn"]
    start_urls = ['http://data.stats.gov.cn/easyquery.htm?cn=B01']
    #start_urls = ['http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgjd&rowcode=zb&colcode=sj&wds=%5B%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0101%22%7D%5D']

    def parse(self, response):    #parse GDB
            #print(response.body)
            #print('================= response start  =================')
            heads = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep - alive',
                'Cookie': '',
                'Host': 'data.stats.gov.cn',
                'Upgrade-Insecure-Requests': 1,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
            }

            k1str = str(gettime())
            # formdata0 = {'cn': 'B01'}
            # formdata1 = {'id': 'zb', 'dbcode': 'hgjd', 'wdcode': 'zb', 'm': 'getTree'}
            # formdata2 = {'m': 'getOtherWds', 'dbcode': 'hgjd', 'rowcode': 'zb', 'colcode': 'sj', 'wds': '[]',
            #              'k1': k1str}  # k1
            # formdata3 = {'m': 'QueryData', 'dbcode': 'hgjd', 'rowcode': 'zb', 'colcode': 'sj', 'wds': '[]',
            #              'dfwds': '[]', 'k1': k1str, 'h': '1'}  # k1 h=1
            # formdata4 = {'id': 'A01', 'dbcode': 'hgjd', 'wdcode': 'zb', 'm': 'getTree'}
            # formdata5 = {'id': 'A01', 'dbcode': 'hgjd', 'wdcode': 'zb', 'm': 'getTree'}
            gdp_step1 = {'m': 'QueryData', 'dbcode': 'hgjd', 'rowcode': 'sj', 'colcode': 'zb', 'wds': '[]',
                         'dfwds': '[{"wdcode":"zb", "valuecode":"A0101"}]', 'k1': k1str, 'h': '1'}  # k1 h=1
            gdp_step2 = {'m': 'QueryData', 'dbcode': 'hgjd', 'rowcode': 'sj', 'colcode': 'zb', 'wds': '[]',
                         'dfwds': '[{"wdcode":"sj","valuecode":"1949-,last4"}]', 'k1': k1str}  # k1

            if 0 < response.url.find('data.stats.gov.cn/easyquery.htm?cn=B01'):
                setCookie = response.headers.getlist('Set-Cookie')

                jsessionIdStartPos = setCookie[0].decode('ascii').find('JSESSIONID=')
                jsessionIdEndPos = setCookie[0].decode('ascii').find(';')
                jsessionId = setCookie[0].decode('ascii')[jsessionIdStartPos:jsessionIdEndPos]

                uStartPos = setCookie[1].decode('ascii').find('u=')
                uEndPos = setCookie[1].decode('ascii').find(';')
                uStr = setCookie[1].decode('ascii')[uStartPos:uEndPos]

                heads['Cookie'] = jsessionId + '; ' + uStr

                yield FormRequest(url='http://data.stats.gov.cn/easyquery.htm',
                    headers=heads,
                    formdata=gdp_step1,
                    method='GET',
                    callback=self.parse,
                    meta={'Cookie':heads['Cookie']}
                )

            elif 0 < response.url.find('valuecode%22%3A%22A0101'):
                #print("******************* to query all data ******************")
                #url = "http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgjd&rowcode=sj&colcode=zb&wds=%5B%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%221949-%2Clast10%22%7D%5D&k1=" + str(
                #     gettime())
                heads['Cookie'] = response.meta['Cookie']
                #print(heads)
                yield FormRequest(url='http://data.stats.gov.cn/easyquery.htm',
                                  headers=heads,
                                  formdata=gdp_step2,
                                  method='GET',
                                  callback=self.parse,
                                  meta={'Cookie': heads['Cookie']}
                                  )
            else:
                print("******************* finally data responsed******************")
                heads['Cookie'] = response.meta['Cookie']
                gdbData = json.loads(response.body)["returndata"]

                #print(gdbData)

                print("********************trigger create gdptitletable, gdpDataTable in pipelines.py*************************")
                colstr=''
                titleItems = {'type':'gdpTitle','data':{}}
                for i in gdbData['wdnodes'][0]['nodes']:
                    colstr += i['cname']
                    colstr += ', '
                    titleItems['data'][ i['code']] =  i['cname']
                yield titleItems
                #print(colstr)
                print("********************trigger insert gdbData to gdpDataTable in pipelines.py*************************")
                sjNum = len(gdbData['wdnodes'][1]['nodes'])
                zbNum = len(gdbData['wdnodes'][0]['nodes'])


                for i in range(sjNum):
                    timeStr=gdbData['datanodes'][i]['wds'][1]['valuecode']
                    rowstr=timeStr

                    dataItems = {'type':'gdpData','data':{'time':timeStr}}
                    for j in range(zbNum):
                        #gdbData['datanodes'][j]['data']['strdata']
                        rowstr +=gdbData['datanodes'][i+j*sjNum]['data']['strdata']
                        rowstr += ', '
                        #print(gdbData['datanodes'][j+i*sjNum]['data']['strdata'])
                        dataItems['data'][ gdbData['datanodes'][i+j*sjNum]['wds'][0]['valuecode'] ] = gdbData['datanodes'][i+j*sjNum]['data']['strdata']
                    #print(rowstr)
                    #print(item)
                    yield dataItems
            print('================= response end  =================')
