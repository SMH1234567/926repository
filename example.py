'''
Function:
	测试程序
'''

import json
import pickle
import requests
from bs4 import BeautifulSoup
import pprint

'''携程旅游景点爬虫'''


class ctripSpider():
    def __init__(self):
        self.proxy = {'http': ''}
        self.count = 0

    '''运行爬虫'''

    def start(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
        }

        # 景点太多，选取北京的景点
        # url中的%s在程序中用page-i1替换
        url = 'https://you.ctrip.com/sight/beijing1/s0-p%s.html#sightname'
        # 测试程序爬取前10页数据
        max_pages = 10
        page_count = 1
        results = {}
        while True:
            try:
                self.__updateProxy()
                res = requests.get(url % page_count, headers=headers, proxies=self.proxy)
                soup = BeautifulSoup(res.text, features='lxml')
                list_wide_mod2 = soup.find_all('div', class_='list_wide_mod2')[0]
                for each1, each2 in zip(list_wide_mod2.find_all('dl'),
                                        list_wide_mod2.find_all('ul', class_='r_comment')):
                    name = each1.dt.a.text
                    addr = each1.find_all('dd')[0].text.strip()
                    level = each1.find_all('dd')[1].text.strip().split('|')[0].strip()
                    if '携程' in level:
                        level = 'unknow'
                    try:
                        price = each1.find_all('span', class_='price')[0].text.strip().replace('¥', '')
                    except:
                        price = 'unknow'
                    score = each2.find_all('a', class_='score')[0].text.strip().replace('\xa0分', '')
                    num_comments = each2.find_all('a', class_='recomment')[0].text.strip()[1: -3]
                    results[name] = [addr, level, price, score, num_comments]
                page_count += 1
                print('[INFO]:爬取进度: %s/%s...' % (page_count - 1, max_pages))
            except:
                self.__updateProxy()
            if page_count == max_pages:
                break
        print('[INFO]:数据爬取完毕, 将保存在data.pkl中...')
        with open('data.pkl', 'wb') as f:
            pickle.dump(results, f)

    '''更新代理'''

    def __updateProxy(self):
        url = "http://api.http.niumoyun.com/v1/http/ip/get?p_id=228&s_id=2&u=AmFVNwE5B2FSYwAuB0kHOA8gVWldZQsaBVJUUFNV&number=1&port=1&type=1&map=1&pro=0&city=0&pb=1&mr=2&cs=1"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'
        }
        if self.count > 10:
            res = requests.get(url, headers=headers)
            res_json = json.loads(res.text)
            self.proxy['http'] = 'http://%s:%s' % (res_json['data'][0]['ip'], res_json['data'][0]['port'])
            self.count = 1
        else:
            self.count += 1


if __name__ == '__main__':
    spider = ctripSpider()
    spider.start()

    # 输出爬取文件
    pkl_file = open('data.pkl', 'rb')
    data1 = pickle.load(pkl_file)
    pprint.pprint(data1)
    pkl_file.close()
