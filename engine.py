from target_urls import Urls
import multiprocessing

class SpiderEngine(object):
    def __init__(self, urls, spider_cls=None):
        self.spider_cls = spider_cls
        if not self.spider_cls:
            self.spider_cls = Spider
        self.url_obj = Urls(urls)

    def _get_spider(self):
        return self.spider_cls(url_obj=self.url_obj)

    def start(self, max_worker):
        for i in range(max_worker):
            p = multiprocessing.Process(target=self.spider_work)
            p.start()
    
    def spider_work(self):
        spider = self._get_spider()
        if spider:
            spider.crawl()

