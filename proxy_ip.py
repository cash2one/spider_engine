import proxy
import multiprocessing

class IPS(object):
    def __init__(self, test_url):
        self.manager = proxy.ProxyManager([proxy.ProxyUltra])
        ips = self.manager.get_proxy_ips()
        self.valid_ips = self.manager.get_valid_ips(ips, test_url)
        self.lock = multiprocessing.Lock()

    def get_ip(self):
        self.lock.acquire()
        if len(self.valid_ips):
            ip = self.valid_ips.pop(0)
        else:
            ip = None
        self.lock.release()
        return ip

