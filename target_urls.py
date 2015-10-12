import multiprocessing
import logging

class Urls(object):
    def __init__(self, urls):
        self.urls = urls
        self.queue = multiprocessing.Queue(len(urls))
        for url in self.urls:
            self.queue.put(url)
        self.lock = multiprocessing.Lock()

    def get_url(self):
        self.lock.acquire()
        if self.queue.empty():
            logging.warn('url empty')
            self.lock.release()
            return ''
        url = self.queue.get()
        self.lock.release()
        logging.debug('get_url: %s' %url)
        return url
    
    def put_url(self, url):
        logging.debug('put_url: %s' %url)
        self.lock.acquire()
        self.queue.put(url)
        self.lock.release()

