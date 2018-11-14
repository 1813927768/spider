#coding:utf-8

import requests
import random
#from ip import IPmanager

class HtmlDownloader(object):

    def __init__(self):
        self.count = 0
        self.cookies = {} #cookie池
        # self.ipmanager = IPmanager()
        

    
    def download(self,url,pro):
        if url is None:
            return 
        # myproxies = {
        #     'http':'127.0.0.1:2740',
        #     'https':'127.0.0.1:2740',
        # }
        if(self.count % 200 == 0 ):     #一段时间更新所有cookie
            self.cookies.clear()
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
        user_agent = random.choice(user_agents)
        # user_agent = user_agents[0]
        cookie = self.cookies.get(user_agent)   #如果存在cookie则使用
        proxy = {'proxy':pro}      
        headers = {
            'User-Agent':user_agent   
        }
        r = requests.get(url,cookies = cookie,headers=headers,proxies=proxy,timeout=5)
        if cookie is None:                  #如果不存在cookie则添加
            self.cookies[user_agent] = r.cookies
        #print(r.request.headers)
        self.count = self.count+1
        r.raise_for_status()
        r.encoding='utf-8'
        return r.text
    

if __name__=="__main__":
    # myproxies = {
    #         'http':'127.0.0.1:2740',
    #         'https':'127.0.0.1:2740',
    #     }
    myproxies = None
    hd =  HtmlDownloader()
    for i in range(1,10):
        hd.download('https://www.amazon.com/dp/B003BUAP10',myproxies)