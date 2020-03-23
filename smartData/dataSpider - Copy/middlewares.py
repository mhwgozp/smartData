# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http.headers import Headers
from scrapy.utils.python import to_bytes

import urllib3
from scrapy.http import HtmlResponse
import json
import requests
import time


# 用来获取 时间戳
def gettime():
    return int(round(time.time() * 1000))

class DataspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DataspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        service_args = ['--load-image=false', '--disk-cache=true']
        startUrl = 'http://data.stats.gov.cn/easyquery.htm?cn=B01'

        heads = {
                         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                         'Accept-Encoding': 'gzip, deflate',
                         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                         'Cache-Control': 'max-age=0',
                         'Connection': 'keep - alive',
                #         'Cookie': 'JSESSIONID=7076131C4213071934E85BA117C49638; u=1',\
                         'Host':  'data.stats.gov.cn',
                         'Upgrade-Insecure-Requests': 1,
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
                         }

        # request.headers[
        #     'Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        # request.headers['Accept-Encoding'] = 'gzip, deflate'
        # request.headers['Accept-Language'] = 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        # request.headers['Cache-Control'] = 'max-age=0'
        # request.headers['Host'] = 'data.stats.gov.cn'
        # request.headers['Upgrade-Insecure-Requests'] = 1
        # request.headers[
        #     'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        #if 0 < request.url.find('data.stats.gov.cn/easyquery.htm?cn=B01'):

        if 0 < request.url.find('valuecode%22%3A%22A0101'):
            additionQueryStr = '&k1=' + str(gettime()) + '&h=1'
            request._set_url(request.url+additionQueryStr)
            request.method='GET'
            request.headers = Headers(heads, encoding='utf-8')

            print(request.url)
        else:
            request.method = 'GET'
            request.headers = Headers(heads, encoding='utf-8')
            cookieStr = 'JSESSIONID=' + request.meta['jsessionId']
            request.headers['Cookie'] = cookieStr

        print('**************** request headers')
        print(request.headers)
        #startUrl = 'http://www.cninfo.com.cn/cninfo-new/announcement/show'

        # heads = {
        #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #         'Accept-Encoding': 'gzip, deflate',
        #         'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        #         'Cache-Control': 'max-age=0',
        #         'Cookie': 'JSESSIONID=7076131C4213071934E85BA117C49638; u=1',
        #         'Host':  'data.stats.gov.cn',
        #         'Proxy-Connection': 'keep-alive',
        #         'Upgrade-Insecure-Requests': 1,
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        #         }
        # request.headers = heads;
        # try:
        #
        #     if (startUrl == request.url[0:len(startUrl)]):
        #         if (None == request.meta.get('jsonStockIndex', None)):
        #             jsonStockIndex = 0
        #         else:
        #             jsonStockIndex = request.meta['jsonStockIndex']
        #         content = 'jsonStockIndex=' + str(jsonStockIndex)
        #         return HtmlResponse(url, encoding='utf-8', status=200, body=content)
        #
        # request.headers['Referer']='http://data.stats.gov.cn/easyquery.htm?cn=B01'

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
