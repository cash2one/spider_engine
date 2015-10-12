from target_urls import Urls
import multiprocessing
import logging

class SpiderEngine(object):
    def __init__(self, urls, spider_cls=None):
        self.spider_cls = spider_cls
        if not self.spider_cls:
            self.spider_cls = Spider
        self.url_obj = Urls(urls)
        self.processes = []
        logging.basicConfig(level=logging.INFO,
                            format='[%(levelname)s] %(filename)s [%(lineno)d] %(threadName)s: %(message)s - %(asctime)s',
                            datefmt='[%d/%b/%Y %H:%M:%S]')

    def _get_spider(self):
        return self.spider_cls(url_obj=self.url_obj)

    def start(self, max_worker):
        for i in range(max_worker):
            p = multiprocessing.Process(target=self.spider_work)
            p.start()
            self.processes.append(p)
        for p in self.processes:
            p.join()

    def spider_work(self):
        spider = self._get_spider()
        if spider:
            while True:
                status = spider.crawl()
                if not status:
                    return

