# -*- coding:utf-8 -*-
# from urlmanager import UrlManager
from htmlDownloader import HtmlDownloader
from htmlParser import HtmlParser
from dataOutput import DataOutput
from ipPool import getProxy,getFromPool2,getFromPool1
#from multiprocessing import Pool
from errUrl import UrlManager
import time
import queue
import threading
import random
import requests



class SpiderMan(object):
    def __init__(self):
        #开启的线程数目
        self.pcount = 1
        #结果输出队列
        self.dqueue = queue.Queue()
        #错误信息输出队列
        self.equeue = queue.Queue()
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()
        # self.proxies = getProxy()
        self.proxies = getFromPool2()
        self.inactivepro = []
        self.count = 0
        self.sumSuccess = 0
        self.sumFail = 0
        self.updating = False
        #self.proxies = ['http://127.0.0.1:2740']

        
    def doCrawl(self,new_url):
        try:
            self.pcount += 1
            count = 1
            #随机选取代理IP
            pro = random.choice(self.proxies)
            #pro = 'http://127.0.0.1:2740'
            while(True):
                #HTML下载器下载网页
                html = self.downloader.download(new_url,pro)
                #HTML解析器抽取网页数据
                data = self.parser.parser(new_url,html)
                ## 数据存储器储存文件引起多线程写冲突而废弃
                # self.output.store_data(data)    
                #如果遇到机器人检测
                if data == "robot":
                    if count < 6:
                        count = count + 1
                        #加入淘汰机制
                        # self.proxies - self.inactivepro 表现良好
                        # self.proxies and self.inactivepro 一次被墙 待观察
                        # self.inactivepro - self.proxies 两次被墙 暂时退出
                        # none 复活失败，永久退出
                        if(count == 5 and len(self.proxies) > 100 ):
                            if(self.inactivepro.index(pro) < 0): #加入观察名单
                                self.inactivepro.append(pro)
                                pro = random.choice(self.proxies)
                            else: #暂时退出
                                print(str(pro)+" out\n")
                                if(self.proxies.index(pro) >= 0):
                                    self.proxies.remove(pro)
                        continue
                    else:
                        raise Exception("robot check")
                else:
                    break
            # 队列将输出存储起来
            self.dqueue.put(data)
        except Exception as e:
            self.sumFail = self.sumFail+1
            print("Fail: link %d fail %d times : %s\n" %(self.count ,self.sumFail,new_url),e.args)
            # 启动激活计划
            if( len(self.proxies) < 200 or len(self.inactivepro)>500):
                pro = random.choice(self.inactivepro)
                if(not pro is None and self.proxies.index(pro) < 0 and self.testIP(pro)):
                    self.proxies.append(pro)
                    print(str(pro)+" in!!!\n")
                # 不管结果如何，都要将pro移除，
                # 判断条件是为了防止多线程并发出现问题
                if(self.inactivepro.index(pro)>=0):
                    self.inactivepro.remove(pro)
            self.equeue.put([new_url,e.args])
        else:
            self.sumSuccess = self.sumSuccess+1
            print("Success: link %d success %d times : %s" %(self.count ,self.sumSuccess,new_url))         
        finally:
            self.pcount -= 1

    
    def setProxy(self):
        #self.proxies = getProxy()
        self.proxies = getFromPool2()
        self.updating = False

    #输出结果和错误信息
    def outPutData(self):
        while(not self.dqueue.empty()):
            data = self.dqueue.get()
            self.output.store_data(data)      
        while(not self.equeue.empty()):
            err = self.equeue.get()
            self.output.store_err(err) 

    def testIP(self,pro):
        url = 'https://www.douban.com'
        res = requests.get(url,proxies={'proxy':pro},timeout=20)
        if(res.status_code == 200):
            return True
        else:
            return False
    
    def crawl(self):
        threads = []
        preFail = 0
        #跳过之前的url
        for i in range(22350):
            self.manager.has_new_url()
        while(self.manager.has_new_url()):
            try:
                self.count = self.count + 1
                # 启动更新计划
                if self.sumFail-preFail > 46 and not self.updating:
                    self.updating = True
                    print("\n\nstart refreshing proxies\n\n")
                    t = threading.Thread(target=SpiderMan.setProxy, args=[self,])
                    t.start()
                    threads.append(t)                 
                    # p = Pool()
                    # result = p.apply_async(getFromPool2, args=())
                    # p.close()
                    #self.proxies = result.get()
                #每50条数据刷新缓冲区和成功率
                if(self.count % 50 == 0 and self.count != 0): 
                    preFail = self.sumFail
                    rate = float(self.sumSuccess)/float(self.count-1)
                    print("Success Rate: %f" %rate)
                    self.output.store_err([str(self.count),str(rate)])  
                    self.output.flush()                   
                #从URL管理器获取新的url
                new_url = self.manager.get_new_url()
                #爬虫主过程(多线程优化)
                if self.pcount < 0:
                    pcount = 0
                else:
                    pcount = self.pcount
                time.sleep(random.random()+pcount/10)   #随机时间间隔，根据线程数调整速度
                t = threading.Thread(target=SpiderMan.doCrawl, args=[self,new_url,])
                t.start()
                threads.append(t)               
                #输出结果和错误信息
                self.outPutData()
            except Exception as e:
                print("wired fail")
        [t.join() for t in threads]
        self.outPutData()


if __name__=="__main__":
    spider_man = SpiderMan()
    spider_man.crawl()