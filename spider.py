import requests
import logging

class Spider(object):
    def __init__(self, **kwargs):
        self.session = requests.session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'}
        self.enable_reborn = kwargs.get('enable_reborn')
        self.enable_proxy = kwargs.get('enable_proxy')
        self.proxy_dict = None
        if self.enable_proxy:
            self.ips_obj = kwargs.get('ips_obj')
            self.cur_ip = self.ips_obj.get_ip()
            if self.cur_ip:
                self.proxy_dict = { 
                    "http"  : 'http://' + self.cur_ip,
                    "https" : 'https://' + self.cur_ip,
                    }
            else:
                logging.warn('spider has no proxy ip')
        self.timeout = kwargs.get('timeout', 8)
        self.url_obj = kwargs.get('url_obj')
        self.parent_url = ''
        self.max_login_tries = kwargs.get('max_login_tries', 3)
        for i in range(self.max_login_tries):
            self.login()
            if self.check_login():
                break

    def request_get(self, url, callback=None):
        resp = self.session.get(url, proxies=self.proxy_dict, timeout=self.timeout)
        if callback:
            callback(resp)

    def request_post(self, url, post_data=None, callback=None):
        resp = self.session.post(url, proxies=self.proxy_dict, data=post_data, timeout=self.timeout)
        if callback:
            callback(resp)

    def login(self):
        pass

    def check_login(self):
        return True

    def crawl(self, url=''):
        logging.info('spider crawl start...')

        if not url:
            url = self.parent_url = self.url_obj.get_url()
            if not url:
                logging.info('spider has no work to do.')
                return
        try:
            resp = self.session.get(url, proxies=self.proxy_dict, timeout=self.timeout)
        except:
            logging.warn('spider crawl exception.')
            self.url_obj.put_url(self.parent_url)
            self.close()
            if self.enable_reborn:
                if not self.reborn():
                    logging.warn('spider reborn failed.')
                    return False
                logging.warn('spider reborn success.')
                return self.crawl()
            else:
                return False
        else:
            new_urls = self.parse(resp)
            logging.info('spider get new urls: %s' %new_urls)
            if new_urls:
                for url in new_urls:
                    self.crawl(url)
            return True

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
            if self.cur_ip:
                self.proxy_dict = { 
                    "http"  : 'http://' + self.cur_ip,
                    "https" : 'https://' + self.cur_ip,
                    }
            else:
                logging.warn('spider has no proxy ip')
                return False
        for i in range(self.max_login_tries):
            self.login()
            if self.check_login():
                break
        return True

    def parse(self, response):
        pass



