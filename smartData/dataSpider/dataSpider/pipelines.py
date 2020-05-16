# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class DataspiderPipeline(object):

    def __init__(self):
        # connection database
        self.connect = pymysql.connect(host='127.0.0.1', user='root', passwd='88888888',
                                       db='smartDataDb')
        # get cursor
        self.cursor = self.connect.cursor()
        print("�������ݿ�ɹ�")


    def process_item(self, item, spider):
        if 'gdpTitle'==item['type']:
            print("to create gdpDataTable:")
            self.cursor.execute("DROP TABLE IF EXISTS `gdptitletable`")
            self.cursor.execute("DROP TABLE IF EXISTS `gdpDataTable`")

            createGdpTitleTable_sql = "CREATE TABLE IF NOT EXISTS `gdptitletable` (`valuecode` varchar(10) NOT NULL, `cname` varchar(255) NOT NULL, PRIMARY KEY (`valuecode`))"
            self.cursor.execute(createGdpTitleTable_sql)


            createGdpDataTable_sql = "CREATE TABLE IF NOT EXISTS `gdpDataTable` ( `time` varchar(10) NOT NULL"

            for key in item['data'].keys():
                insert_sql = "insert into gdptitletable(valuecode, cname) VALUES (%s,%s)"
                self.cursor.execute(insert_sql, (key, item['data'][key]))

                createGdpDataTable_sql += ", `{}` varchar(10)".format(key)
            createGdpDataTable_sql += ", PRIMARY KEY (`time`))"
            self.cursor.execute(createGdpDataTable_sql)

        elif 'gdpData'==item['type']:
            print("to update gdpDataTable:")
            insert_sql = "insert into gdpDataTable values ("
            index=0
            for key in item['data'].keys():
                if index==0:
                    index+=1
                else:
                    insert_sql += ","
                insert_sql += "'"
                insert_sql += item['data'][key]
                insert_sql += "'"
            insert_sql +=")"
            print(insert_sql)
            self.cursor.execute(insert_sql)
        elif 'cpiTableCreate' == item['type']:
            print("to create cpiDataTable:")
            self.cursor.execute("DROP TABLE IF EXISTS `cpiDataTable`")
            createCpiDataTable_sql = "CREATE TABLE IF NOT EXISTS `cpiDataTable` ( `time` varchar(10) NOT NULL"
            for key in item['data'].keys():
                if key != 'time':
                    createCpiDataTable_sql += ", `{}` varchar(10)".format(key)
            createCpiDataTable_sql += ", PRIMARY KEY (`time`))"
            self.cursor.execute(createCpiDataTable_sql)

        elif 'cpiData' == item['type']:
            print("to update cpiDataTable:")
            insert_sql = "insert into cpiDataTable values ("
            index = 0
            for key in item['data'].keys():
                if index == 0:
                    index += 1
                else:
                    insert_sql += ","
                insert_sql += "'"
                insert_sql += item['data'][key]
                insert_sql += "'"
            insert_sql += ")"
            print(insert_sql)
            self.cursor.execute(insert_sql)
        elif 'moneysupplyData' == item['type']:
            print("to update moneysupply:")
            insert_sql = "insert into moneysupply values ("
            index = 0
            for key in item['data'].keys():
                if index == 0:
                    insert_sql += "'"
                    insert_sql += item['data'][key]
                    insert_sql += "'"
                    index += 1
                else:
                    insert_sql += ","
                    insert_sql += item['data'][key]
            insert_sql += ",null)"
            print(insert_sql)
            self.cursor.execute(insert_sql)

        self.connect.commit()
        #return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
