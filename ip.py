import requests
import random
import time
import threading
from bs4 import BeautifulSoup

class IPmanager(object):

    def getIP(self):
        headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'}
        url = 'http://www.xicidaili.com/nn/1'
        s = requests.get(url,headers = headers)
        soup = BeautifulSoup(s.text,'lxml')
        ips = soup.select('#ip_list tr')
        fp = open('host.txt','w')
        for i in ips:
            try:
                ipp = i.select('td')
                ip = ipp[1].text
                host = ipp[2].text
                fp.write(ip)
                fp.write('\t')
                fp.write(host)
                fp.write('\n')
            except Exception as e :
                print ('no ip !')
        fp.close()

    def getIPFromPool(self):
        try :
            fp = open('pool.txt','r')
            ips = fp.readlines()
            proxys = []
            threads = []
            for p in ips:
                proxy = p.strip('\n')
                t = threading.Thread(target=testIP, args=[proxy, proxys])
                t.start()
                time.sleep(0.2)
                threads.append(t)
            [t.join() for t in threads]
        except Exception as e:
                print (e)
                pass
        finally:
            print(len(proxys))
            return proxys



    def getUsableIP(self):
        proxy = {
            'http':'127.0.0.1:2740',
            'https':'127.0.0.1:2740',
        }
        user_agents = [
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
]
        headers = {'User-Agent':random.choice(user_agents)}
        url = 'http://www.xicidaili.com/nn/1'
        testurl = 'https://www.baidu.com'
        s = requests.get(url,headers = headers,proxies=proxy)
        soup = BeautifulSoup(s.text,'lxml')
        ips = soup.select('#ip_list tr')
        proxys = list()
        usableIP = []
        for i in ips:
            try:
                ipp = i.select('td')
                ip = ipp[1].text
                host = ipp[2].text
                proxy = 'http://' +  ip + ':' + host
                proxies = {'proxy':proxy}
                proxys.append(proxies)
            except Exception as e :
                print ('no ip !')
        for pro in proxys:
            try :
                s = requests.get(testurl,proxies = pro)
                if s.status_code==200:
                    usableIP.append(pro)
            except Exception as e:
                    print (e)
        return usableIP

# def static_vars(**kwargs):
#     def decorate(func):
#         for k in kwargs:
#             setattr(func, k, kwargs[k])
#         return func
#     return decorate

def testIP(ip,good_proxies):
        try:
            pro = {'proxy':ip}
            # print(pro)
            url = 'https://www.amazon.com/dp/B00004Y7GZ'
            r = requests.get(url, proxies=pro,timeout=3)
            r.raise_for_status()
            #print(r.status_code, ip)
        except Exception as e:
            #print(e)
            pass
        else:
            #print(ip,"succ",len(good_proxies))
            good_proxies.append(ip)    


if __name__=="__main__":
    im = IPmanager()
    #im.getUsableIP()
    im.getIPFromPool()
