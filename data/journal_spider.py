import re
import time
import requests

headers = {
    "Host": "dblp.uni-trier.de",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cookie": "dblp-view=y; dblp-search-mode=c"
}

main_page_pattern = re.compile('http://dblp.uni-trier.de/db/journals/[/a-z0-9\.]+')


# 需要抓取的主页
main_url_list =['http://dblp.uni-trier.de/db/journals/tiis/',
                'http://dblp.uni-trier.de/db/journals/tist/',
                'http://dblp.uni-trier.de/db/journals/tkdd/',
                'http://dblp.uni-trier.de/db/journals/tois/',
                'http://dblp.uni-trier.de/db/journals/toit/',
                'http://dblp.uni-trier.de/db/journals/tweb/']

# 获取主页的 所有列表链接
def get_list_page():
    with open('list_page.url','w') as f:
        for url in main_url_list:
            f.write('Referer: '+url+'\n'+'-'*30+'\n')
            resp = requests.get(url,headers=headers, proxies={'http':'http://127.0.0.1:1087'})
            page_urls = re.findall(main_page_pattern, resp.content)
            for purl in page_urls:
                f.write(purl+'\n')
            f.write('*'*30+'\n')
            print page_urls
            time.sleep(0.5)

xml_pattern = re.compile('http://dblp.uni-trier.de/rec/xml/journals/[\.\w/d/]+.xml')
# 获取列表页里面, 所有简介的链接, 并进行抓取
def get_xml_url():
    with open("xml_page.url",'w') as of:
        with open('list_page.url') as f:
            journal_list = filter(None, f.read().split('*'*30))
            for journal in journal_list:
                refer = journal.split('-'*30+'\n')[0]
                urls = journal.split('-'*30+'\n')[1]
                headers['Referer'] = refer.split(': ')[1].replace('\n','')
                
                urls = filter(None, urls.split('\n'))

                for url in urls:
                    resp = requests.get(url, headers=headers, proxies={'http':'http://127.0.0.1:1087'})
                    xml_urls = re.findall(xml_pattern, resp.content)
                    for xurl in xml_urls:
                        of.write(xurl+'\n')
                    print xml_urls
                    time.sleep(0.5)
                

get_list_page()
get_xml_url()