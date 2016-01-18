from spider import Spider
from engine import SpiderEngine
from proxy_ip import IPS
import baiduocr
import base64
import time
import re
import random

test_url = "http://zzxh.zjsgat.gov.cn:6081/zjwwzzxh"
urls = []
for i in range(2082,3064):
    urls.append("http://zzxh.zjsgat.gov.cn:6081/zjwwzzxh/tscreenquery.do?act=query&status=doQueryInputVehInfo&pageNo=%d" %i)

class MySpider(Spider):
    #ips_obj = IPS(test_url)
    def __init__(self, **kwargs):
        kwargs['enable_reborn'] = True
        kwargs['enable_proxy'] = False
        kwargs['max_login_tries'] = 8
        #kwargs['ips_obj'] = self.ips_obj
        self.out = open('out.txt', 'w+')
        self.login_status = False
        Spider.__init__(self, **kwargs)

    def login(self):
        img_url = "http://zzxh.zjsgat.gov.cn:6081/zjwwzzxh/include/chineseVal.jsp"
        self.request_get(img_url, callback=self.login_post)

    def login_post(self, response):
        jpg_data = response.content
        jpg_data = base64.b64encode(jpg_data)
        textjsp = baiduocr.get_words_from_img(jpg_data)
 
        post_data = {
                'act':'shownumselectquerypage',
                'flags':'5',
                'fzjg':'浙A',
                'hdid':'999',
                'hphm':'A*****',
                'jyw': textjsp,
                'num':'0',
                }
        post_data = str(post_data).encode('gbk')
        # print(post_data)
        url = 'http://zzxh.zjsgat.gov.cn:6081/zjwwzzxh/tscreenquery.do?act=query&status=doQueryInputVehInfo'
        self.request_post(url, post_data=post_data, callback=self.get_login_status)

    def _get_car_plate(self, content):
        za = r'<li><input type="button" value="(.*)"  /></li>'
        value = re.findall(za, content)
        return value

    def get_login_status(self, response):
        plate_cnt = len(self._get_car_plate(response.text))
        self.login_status = True if plate_cnt > 0 else False

    def check_login(self):
        return self.login_status

    def parse(self, response):
        plates = self._get_car_plate(response.text)
        for plate in plates:
            self.out.write(plate + '\n')
        self.out.flush()

        delay = random.uniform(3, 11)
        time.sleep(delay)

SpiderEngine(urls=urls, spider_cls=MySpider).start(1)

