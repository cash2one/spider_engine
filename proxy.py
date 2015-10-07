import requests
from bs4 import BeautifulSoup
import sys

class ProxyBase(object):
    @classmethod
    def get_proxy_ips(cls):
        pass

class ProxyUltra(ProxyBase):
    @classmethod
    def get_proxy_ips(cls):
        s = requests.session()
        r = s.get('http://www.ultraproxies.com/high-anonymous.html')
        s.close()
        soup = BeautifulSoup(r.text, 'lxml')
    
        '''
        print(soup.title)
        with open('hh', 'w') as f:
            print(soup.prettify(), file=f)
        '''
        def process_port(s):
            port = ''
            for c in s.split('-'):
                port += chr(int(c) - 17)
            return port
    
        proxy_ips = []
        for tr in soup.find_all('tr', class_='row0'):
            ip = port = ''
            for td in tr.children:
                if td.get('class'):
                    if td['class'][0] == 'ip':
                        ip = td.string
                    elif td['class'][0] == 'port':
                        port = process_port(td.string)
            if ip and port:
                proxy_ip = ip + port
                proxy_ips.append(proxy_ip)
    
        return proxy_ips
    
class ProxyManager(object):
    def __init__(self, proxy_objs):
        self.proxy_objs = proxy_objs

    def get_proxy_ips(self):
        ips = []
        for obj in self.proxy_objs:
            ips.extend(obj.get_proxy_ips())
        return ips

    def get_valid_ips(self, ips, url):
        valid_ips = []
        for ip in ips:
            proxyDict = { 
                            "http"  : 'http://' + ip,
                            "https" : 'https://' + ip,
                        }
            s = requests.session()
            s.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'}
            try:
                s.get(url, proxies=proxyDict, timeout=8)
                valid_ips.append(ip)
                print('%s valid.' %ip)
            except requests.exceptions.Timeout as e:
                exc_type, exc_value, traceback = sys.exc_info()
                print('%s %s, value: %s' %(ip, exc_type, exc_value))
            except Exception as e:
                exc_type, exc_value, traceback = sys.exc_info()
                print('%s %s, value: %s' %(ip, exc_type, exc_value))
            s.close()
    
        return valid_ips


'''
manager = ProxyManager([ProxyUltra])
ips = manager.get_proxy_ips()
print(ips)
valid_ips = manager.get_valid_ips(ips, 'http://stackoverflow.com')
print(valid_ips)
'''

