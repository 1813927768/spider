# -*- coding:utf-8 -*-
from urlmanager import UrlManager
from htmlDownloader import HtmlDownloader
from htmlParser import HtmlParser
from dataOutput import DataOutput
from ipPool import getProxy,getFromPool2
#from multiprocessing import Pool
import time
import queue
import threading
import random



class SpiderMan(object):
    def __init__(self):
        self.dqueue = queue.Queue()
        self.equeue = queue.Queue()
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()
        self.proxies = getProxy()
        #self.proxies = getFromPool2()
        self.count = 0
        self.sumSuccess = 0
        self.sumFail = 0
        #self.proxies = ['http://127.0.0.1:2740']

        
    def doCrawl(self,new_url):
        try:
            #HTML下载器下载网页
            pro = random.choice(self.proxies)
            #pro = 'http://127.0.0.1:2740'
            html = self.downloader.download(new_url,pro)
            #HTML解析器抽取网页数据
            data = self.parser.parser(new_url,html)
            # #数据存储器储存文件
            # self.output.store_data(data)    
            # 队列将输出存储起来
            self.dqueue.put(data)
        except Exception as e:
            self.sumFail = self.sumFail+1
            print("Fail: link %d fail %d times : %s\n" %(self.count ,self.sumFail,new_url),e.args)
            #self.output.store_err([new_url,e.args]) 
            self.equeue.put([new_url,e.args])
        else:
            self.sumSuccess = self.sumSuccess+1
            print("Success: link %d success %d times : %s" %(self.count ,self.sumSuccess,new_url))

    
    def setProxy(self):
        self.proxies = getProxy()
    
    def crawl(self):
        threads = []
        #跳过之前的url
        for i in range(0):
            self.manager.has_new_url()
        while(self.manager.has_new_url()):
            try:
                self.count = self.count + 1
                if self.sumFail % 1500 == 1499: 
                    print("\n\nstart refreshing proxies\n\n")
                    t = threading.Thread(target=SpiderMan.setProxy, args=[self,])
                    t.start()
                    threads.append(t)                 
                    # p = Pool()
                    # result = p.apply_async(getFromPool2, args=())
                    # p.close()
                    #self.proxies = result.get()
                #每20条数据刷新缓冲区和成功率
                if(self.count % 50 == 49): 
                    rate = float(self.sumSuccess)/float(self.count-1)
                    print("Success Rate: %f" %rate)
                    self.output.store_err([str(self.count),str(rate)])  
                    self.output.flush()                   
                #从URL管理器获取新的url
                new_url = self.manager.get_new_url()
                #爬虫主过程(多线程优化)
                time.sleep(random.random())   #随机时间间隔
                t = threading.Thread(target=SpiderMan.doCrawl, args=[self,new_url,])
                t.start()
                threads.append(t)               
                #time.sleep(random.uniform(0.3,0.6))
                #输出结果和错误信息
                while(not self.dqueue.empty()):
                    data = self.dqueue.get()
                    self.output.store_data(data)      
                while(not self.equeue.empty()):
                    err = self.equeue.get()
                    self.output.store_err(err)            
            except Exception as e:
                print("wired fail")
                #self.output.store_err([new_url,e.args])
                #time.sleep(random.uniform(0.5,0.7))
        [t.join() for t in threads]


if __name__=="__main__":
    spider_man = SpiderMan()
    spider_man.crawl()