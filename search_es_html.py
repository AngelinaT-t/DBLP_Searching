#!/usr/bin/env python
# -- coding: utf-8 --

import sys
import os
import web
import json
import traceback
import requests
import ConfigParser
import codecs
from datetime import date, timedelta

urls = (
    '/hello', 'Hello',
    '/query', 'Query',
    '/index', 'Index'
)

CUR_DIR = os.path.split(os.path.realpath(__file__))[0]
app = web.application(urls, globals())
ES_SERVER_PRE = "http://10.194.6.49/ESProxyService/queryTable?table="
ES_SERVER_END = "&user=qaMonitor&logid=web_query"

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')  

render=web.template.render("templates")


class Hello:
    def GET(self):
        a = { 'p1':'v1',
              'p2':{'c2':'v2'}
            }
        return render.test(json.dumps(a),"123")

class Index:
    def GET(self):
        return render.index()

class Query:
    def GET(self):
        input_data = web.input()
        
        domain_type = input_data.get('type')
        keyword = input_data.get("keyword")
        keyword = keyword.encode("utf-8")
        print keyword
        web.header('Content-Type','text/html; charset=utf-8', unique=True)
        keyword = keyword.replace(" ",'\ ')

        java_process = os.popen("java DblpIR %s %s"%(domain_type, keyword))
        java_resp = java_process.read()
        print "java-resp"+java_resp
        try:
            raw_list = java_resp.split('*'*30)
            ten_result = raw_list[0]
            five_more = raw_list[1]

            ten_list = filter(None, ten_result.split('\n'))
            five_list = filter(None, five_more.split('\n'))
        except:
            return '<h1>找不到匹配项,请重新输入</h1><a href="./index">点我返回</a>'
        
        if len(ten_list) == 0 or len(ten_list) == 0:
            return '<h1>找不到匹配项,请重新输入</h1><a href="./index">点我返回</a>'

        mjson = {'ten_list':[], 'five_list':[]}

        for item in ten_list:
            terms = item.split('#+*+#')
            tmp_dict = {}
            tmp_dict['journal'] = terms[0]
            tmp_dict['author'] = terms[1]
            tmp_dict['title'] = terms[2]
            tmp_dict['year'] = terms[3]
            tmp_dict['link'] = terms[4]
            mjson['ten_list'].append(tmp_dict)
        
        for item in five_list:
            terms = item.split('#+*+#')
            tmp_dict = {}
            tmp_dict['journal'] = terms[0]
            tmp_dict['author'] = terms[1]
            tmp_dict['title'] = terms[2]
            tmp_dict['year'] = terms[3]
            tmp_dict['link'] = terms[4]
            mjson['five_list'].append(tmp_dict)


        json_str = json.dumps(mjson)
        return render.result(json_str)







def main():
    app.run()    


if __name__ == '__main__':
    main()

