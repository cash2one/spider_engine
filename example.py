from spider import Spider
from engine import SpiderEngine
from proxy_ip import IPS

urls = ['http://hangzhou.bitauto.com/?WT.mc_id=bdlogo']
test_url = 'http://hangzhou.bitauto.com/?WT.mc_id=bdlogo'

class MySpider(Spider):
    ips_obj = IPS(test_url)
    def __init__(self, **kwargs):
        kwargs['enable_reborn'] = True
        kwargs['enable_proxy'] = True
        kwargs['ips_obj'] = self.ips_obj
        Spider.__init__(self, **kwargs)

    def login(self):
        pass

    def parse(self, response):
        # print(response.text)
        pass

SpiderEngine(urls=urls, spider_cls=MySpider).start(2)

