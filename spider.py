import requests
import multiprocessing
import logging

class Spider(object):
    def __init__(self, **kwargs):
        self.session = requests.session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'}
        self.enable_reborn = kwargs.get('enable_reborn')
        self.enable_proxy = kwargs.get('enable_proxy')
        if self.enable_proxy:
            self.ips_obj = kwargs.get('ips_obj')
            self.cur_ip = self.ips_obj.get_ip()
        self.timeout = kwargs.get('timeout', 8)
        self.url_obj = kwargs.get('url_obj')
        self.parent_url = ''
        self.max_login_tries = kwargs.get('max_login_tries', 3)
        for i in range(self.max_login_tries):
            if self.login():
                break

    def login(self, post_data, url):
        logging.info('spider login start...')
        if not post_data:
            return

        if self.enable_proxy:
            if not self.cur_ip:
                return
            proxy_dict = { 
                    "http"  : 'http://' + self.cur_ip,
                    "https" : 'https://' + self.cur_ip,
                    }
        else:
            proxy_dict = None

        resp = self.session.post(url, proxies=proxy_dict, data=post_data, timeout=self.timeout)
        return self.check_login(resp)

    def check_login(resp):
        return True

    def crawl(self, url=''):
        logging.info('spider crawl start...')
        if self.enable_proxy:
            if not self.cur_ip:
                return
            proxy_dict = { 
                    "http"  : 'http://' + self.cur_ip,
                    "https" : 'https://' + self.cur_ip,
                    }
        else:
            proxy_dict = None

        if not url:
            url = self.parent_url = self.url_obj.get_url()
            if not url:
                logging.info('spider has no work to do.')
                return
        try:
            resp = self.session.get(url, proxies=proxy_dict, timeout=self.timeout)
        except:
            self.url_obj.put_url(self.parent_url)
            self.close()
            if self.enable_reborn:
                self.reborn(ip)
                self.crawl(self.url_obj)
        else:
            new_urls = self.parse(resp)
            logging.info('spider get new urls: %s' %new_urls)
            if new_urls:
                for url in new_urls:
                    self.crawl(url)

    def close(self):
        logging.info('spider finish...')
        self.session.close()

    def reborn(self, ip=None):
        self.session.close()
        logging.info('spider reborn...')
        self.session = requests.session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'}
        if self.enable_proxy:
            self.cur_ip = self.ips_obj.get_ip()

    def parse(self, response):
        pass



