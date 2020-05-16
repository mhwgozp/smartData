from scrapy.spiders import Spider
import sys

sys.path.append("C:\smartData\smartData\dataSpider\spiders")
#sys.path.append(r"C:\smartData\smartData\dataSpider\dataSpider\spiders\")

#from scrapy.selector import Selector
#from scrapyspider.items import CninfoItem

from scrapy.http import Request
from scrapy.http import FormRequest
import json
import datetime
import time
import os


def gettime():
    return int(round(time.time() * 1000))
  
class cpiSpider(Spider):
    name = "moneySupplySpider"
    allowed_domains = ["stats.gov.cn"]
    start_urls = ['http://data.stats.gov.cn/easyquery.htm?cn=A01']
    #start_urls = ['http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgjd&rowcode=zb&colcode=sj&wds=%5B%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0101%22%7D%5D']

    def parse(self, response):
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
            queryStep1 = {'m': 'QueryData', 'dbcode': 'hgyd', 'rowcode': 'sj', 'colcode': 'zb', 'wds': '[]',
                         'dfwds': '[{"wdcode":"zb", "valuecode":"A0D01"}]', 'k1': k1str, 'h': '1'}  # k1 h=1
            queryStep2 = {'m': 'QueryData', 'dbcode': 'hgyd', 'rowcode': 'sj', 'colcode': 'zb', 'wds': '[]', 'dfwds': '[{"wdcode":"sj", "valuecode":"1949-,last10"}]', 'k1': k1str}

            if 0 < response.url.find('data.stats.gov.cn/easyquery.htm?cn=A01'):
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
                    formdata=queryStep1,
                    method='GET',
                    callback=self.parse,
                    meta={'Cookie':heads['Cookie']}
                )

            if 0 < response.url.find('A0D01'):
                heads['Cookie'] = response.meta['Cookie']
                # cpiData = json.loads(response.body)["returndata"]
                # print(cpiData)
                # print(heads)
                yield FormRequest(url='http://data.stats.gov.cn/easyquery.htm',
                                  headers=heads,
                                  formdata=queryStep2,
                                  method='GET',
                                  callback=self.parse,
                                  meta={'Cookie': heads['Cookie']}
                                  )

            elif 0 < response.url.find('1949'):
                print("******************* finally data responsed******************")
                heads['Cookie'] = response.meta['Cookie']
                returndata = json.loads(response.body)["returndata"]

                sjNum = len(returndata['wdnodes'][1]['nodes'])
                zbNum = len(returndata['wdnodes'][0]['nodes'])
                print(
                    "********************trigger insert Data into db in pipelines.py*************************")
                for i in range(sjNum):
                    timeStr = returndata['datanodes'][i]['wds'][1]['valuecode']
                    Debug_rowstr = timeStr+", "

                    dataItems = {'type': 'moneysupplyData', 'data': {'time': timeStr}}
                    #print (returndata['datanodes'][i]['data']['hasdata'])
                    if True==returndata['datanodes'][i]['data']['hasdata']:
                        for j in range(zbNum):
                            # gdbData['datanodes'][j]['data']['strdata']
                            Debug_rowstr += returndata['datanodes'][i + j * sjNum]['data']['strdata']
                            Debug_rowstr += ', '
                            # print(gdbData['datanodes'][j+i*sjNum]['data']['strdata'])
                            dataItems['data'][returndata['datanodes'][i + j * sjNum]['wds'][0]['valuecode']] = \
                            returndata['datanodes'][i + j * sjNum]['data']['strdata']
                        print(Debug_rowstr)
                        print(dataItems)
                        yield dataItems
