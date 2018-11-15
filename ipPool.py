from bs4 import BeautifulSoup as Soup
import requests
import json
import random
import time
import threading

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/64.0.3282.186 Safari/537.36'}


def parse_items(items):
    # 存放ip信息字典的列表
    ips = []
    for item in items:
        tds = item.find_all('td')
        # 从对应位置获取ip，端口，类型
        ip, port, _type = tds[1].text, int(tds[2].text), tds[5].text
        ips.append(_type.lower()+'://'+ip+':'+str(port))
    return ips

def check_ip(ip, good_proxies):
    try:
        pro = {'proxy':ip}
        # print(pro)
        urls = [
            'https://www.amazon.com/dp/0767026977',
            'https://www.amazon.com/dp/B00317IGCI',
            'https://www.amazon.com/dp/6301300416',
            'https://www.amazon.com/dp/B00006LPEF',
            'https://www.amazon.com/dp/B0000541WJ',
            'https://www.amazon.com/dp/B000GEIRLE',
            'https://www.amazon.com/dp/B0001611C4',
            'https://www.amazon.com/dp/B000HIVIP6',
            'https://www.amazon.com/dp/B00016XNR0',
            'https://www.amazon.com/dp/6302799074',
            'https://www.amazon.com/dp/6302030870',
        ]
        url = random.choice(urls)
        r = requests.get(url, headers=header, proxies=pro,timeout=3)
        r.raise_for_status()
        print(r.status_code, ip)
    except Exception as e:
        print(e)
        pass
    else:
        good_proxies.append(ip)

def get_proxies():           #另一个资源ip池
    url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
    r = requests.get(url, headers=header)
    r.raise_for_status()
    proxies = []
    threads = []
    for item in r.text.split('\n'):
        if(item == ''):
            continue
        tmp = json.loads(item)
        if(tmp['anonymity']=='high_anonymous' and tmp['response_time'] < 3):   #只获取高匿代理
            proxy = tmp['type'].lower()+'://'+str(tmp['host'])+':'+str(tmp['port'])
            t = threading.Thread(target=check_ip, args=[proxy, proxies])
            t.start()                    
            time.sleep(0.15)  #防止线程太多导致问题
            threads.append(t)
            # check_ip(proxy,proxies)
    [t.join() for t in threads]
        # print(tmp)
    return proxies


def write_to_json(ips):
    with open('proxies.json', 'a', encoding='utf-8') as f:
        json.dump(ips, f, indent=4)

def write_to_txt(ips):
    with open('pool.txt', 'a') as f:
        for ip in ips:
            f.write(ip+'\n')


class GetThread(threading.Thread):
    '''对Thread进行封装'''
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)
        self.good_proxies = []
        

    def run(self):
        url = 'http://www.xicidaili.com/nn/%d' % self._args[0]
        target_headers = {'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Referer':'http://www.xicidaili.com/',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'zh-CN,zh;q=0.8',
	}
        # 发起网络访问
        try:
            r = requests.get(url, headers=target_headers,timeout=3)
            r.encoding = r.apparent_encoding
            r.raise_for_status()
            soup = Soup(r.text, 'lxml')
            # 第一个是显示最上方的信息的，需要丢掉
            items = soup.find_all('tr')[1:]
            ips = parse_items(items)
            threads = []
            for ip in ips:
                # 开启多线程
                t = threading.Thread(target=check_ip, args=[ip, self.good_proxies])
                t.start()
                time.sleep(0.15)
                threads.append(t)
            [t.join() for t in threads]
        except Exception as e:
            print("fail for xici")
            pass

    def get_result(self):
        return self.good_proxies


def getFromPool1():
    proxies = []
    #获取第一个资源池http://www.xicidaili.com/nn/
    threads = []
    #起始页
    start = random.randint(1,1000)
    for i in range(start, start+10):
        t = GetThread(args=[i])
        t.start()
        time.sleep(10)
        threads.append(t)
    [t.join() for t in threads]
    for t in threads:
        proxy = t.get_result()
        proxies.extend(proxy)
        #write_to_txt(proxies)
    return proxies

def getFromPool2():
    #另一个资源池https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list
    return get_proxies()

def getProxy():
    time1 = time.time()
    proxy = getFromPool1()
    len1 = len(proxy)
    time2 = time.time()
    proxy.extend(getFromPool2())
    len2 = len(proxy)-len1
    time3 = time.time()
    print("\n\n pool1: %f s  %d \n pool2: %f s  %d\n\n"%(time2-time1,len1,time3-time2,len2))
    time.sleep(1)
    return proxy


if __name__ == '__main__':
    getFromPool1()

