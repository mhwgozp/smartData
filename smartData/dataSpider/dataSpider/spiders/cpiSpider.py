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
    name = "cpiSpider"
    allowed_domains = ["stats.gov.cn"]
    start_urls = ['http://data.stats.gov.cn/easyquery.htm?cn=A01']
    #start_urls = ['http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgjd&rowcode=zb&colcode=sj&wds=%5B%5D&dfwds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A0101%22%7D%5D']

    def parse(self, response):    #parse CPI
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
            cpi_step1 = {'m': 'QueryData', 'dbcode': 'hgyd', 'rowcode': 'sj', 'colcode': 'zb', 'wds': '[]',
                         'dfwds': '[{"wdcode":"zb", "valuecode":"A010101"}]', 'k1': k1str, 'h': '1'}  # k1 h=1
            cpi_step2 = {'m': 'QueryData', 'dbcode': 'hgyd', 'rowcode': 'sj', 'colcode': 'zb', 'wds': '[]', 'dfwds': '[{"wdcode":"sj", "valuecode":"2016-,last10"}]', 'k1': k1str}

            cpi_step3 = {'m': 'QueryData', 'dbcode': 'hgyd', 'rowcode': 'sj', 'colcode': 'zb', 'wds': '[]',
                         'dfwds': '[{"wdcode":"zb", "valuecode":"A010102"}]', 'k1': k1str, 'h': '1'}  # k1 h=1
            cpi_step4 = {'m': 'QueryData', 'dbcode': 'hgyd', 'rowcode': 'sj', 'colcode': 'zb', 'wds': '[]', 'dfwds': '[{"wdcode":"sj", "valuecode":"1987-,last10"}]', 'k1': k1str}

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
                    formdata=cpi_step1,
                    method='GET',
                    callback=self.parse,
                    meta={'Cookie':heads['Cookie']}
                )

            if 0 < response.url.find('A010101'):
                heads['Cookie'] = response.meta['Cookie']
                # cpiData = json.loads(response.body)["returndata"]
                # print(cpiData)
                # print(heads)
                yield FormRequest(url='http://data.stats.gov.cn/easyquery.htm',
                                  headers=heads,
                                  formdata=cpi_step2,
                                  method='GET',
                                  callback=self.parse,
                                  meta={'Cookie': heads['Cookie']}
                                  )

            elif 0 < response.url.find('2016'):
                print("******************* finally data responsed******************")
                heads['Cookie'] = response.meta['Cookie']
                cpiData = json.loads(response.body)["returndata"]
                #print(cpiData)

                # print("********************title*************************")
                # colstr=''
                # titleItems = {'type':'gdpTitle','data':{}}
                # for i in gdbData['wdnodes'][0]['nodes']:
                #     colstr += i['cname']
                #     colstr += ', '
                #     titleItems['data'][ i['code']] =  i['cname']
                # yield titleItems
                # #print(colstr)
                sjNum = len(cpiData['wdnodes'][1]['nodes'])
                zbNum = len(cpiData['wdnodes'][0]['nodes'])

                print("********************trigger create cpiDataTable in pipelines.py*************************")
                dataItems = {'type': 'cpiTableCreate', 'data': {'record1':'value'}}
                yield dataItems

                print("********************trigger insert data to cpiDataTable in pipelines.py*************************")
                for i in range(sjNum):
                    timeStr=cpiData['datanodes'][i]['wds'][1]['valuecode']
                    rowstr=timeStr

                    dataItems = {'type':'cpiData','data':{'time':timeStr}}
                    rowstr +=cpiData['datanodes'][i]['data']['strdata']
                    dataItems['data'][ cpiData['datanodes'][i]['wds'][0]['valuecode'] ] = cpiData['datanodes'][i]['data']['strdata']
                    #print(rowstr)
                    #print(dataItems)
                    yield dataItems

                yield FormRequest(url='http://data.stats.gov.cn/easyquery.htm',
                                  headers=heads,
                                  formdata=cpi_step3,
                                  method='GET',
                                  callback=self.parse,
                                  meta={'Cookie': heads['Cookie']}
                                  )
            if 0 < response.url.find('A010102'):
                heads['Cookie'] = response.meta['Cookie']
                yield FormRequest(url='http://data.stats.gov.cn/easyquery.htm',
                                  headers=heads,
                                  formdata=cpi_step4,
                                  method='GET',
                                  callback=self.parse,
                                  meta={'Cookie': heads['Cookie']}
                                  )
            elif 0 < response.url.find('1978'):
                cpiData = json.loads(response.body)["returndata"]
                sjNum = len(cpiData['wdnodes'][1]['nodes'])
                zbNum = len(cpiData['wdnodes'][0]['nodes'])
                print("********************trigger insert cpiData before 2016 to cpiDataTable in pipelines.py*************************")
                for i in range(sjNum):
                    timeStr = cpiData['datanodes'][i]['wds'][1]['valuecode']
                    rowstr = timeStr

                    dataItems = {'type': 'cpiData', 'data': {'time': timeStr}}
                    rowstr += cpiData['datanodes'][i]['data']['strdata']
                    dataItems['data'][cpiData['datanodes'][i]['wds'][0]['valuecode']] = cpiData['datanodes'][i]['data'][
                        'strdata']
                    # print(rowstr)
                    # print(dataItems)
                    yield dataItems
            print('================= response end  =================')

      
