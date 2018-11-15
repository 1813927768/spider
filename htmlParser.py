#coding:utf-8

from bs4 import BeautifulSoup
# from lxml import etree
import lxml
import re
from htmlDownloader import HtmlDownloader

class HtmlParser(object):
    
    def parser(self,page_url,html_cont):
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont,'lxml')
        new_data = self._get_new_data(page_url,soup)
        # content = etree.HTML(html_cont)
        # new_data = self._get_data(page_url,content)
        return new_data
    
    def test(self):
        url = "https://www.amazon.com/dp/B0042AGNA0"
        soup = BeautifulSoup(open(r'test.txt'),"lxml")
        #print(soup.find_all('span'))
        new_data = self._get_new_data(url,soup)


            
    def _get_new_data(self,page_url,soup):   #使用beautifulsoup查询
        data={}
        data['url']=page_url
        catag = date = actor = director = None
        title = soup.find('span',id="productTitle")
        if title is None: #一类网页
            #获取标题
            title = soup.find('h1',attrs={"class": "DigitalVideoUI_spacing__base dv-node-dp-title avu-full-width"})
            if title is None:
                raise Exception("robot check")
            data['title'] = title.get_text().strip()
            #获取日期
            date = soup.find("span",attrs={"data-automation-id":"release-year-badge"})
            if not date is None:
                date = date.get_text().strip()
            data['date'] = date
            table = soup.find('table')      #第一个table一般都是详细信息
            #table = soup.find('table',attrs={"class": "a-keyvalue a-horizontal-stripes  a-align-top product-details-meta avu-text-small"})
            tableTitle = table.find_all("th")
            for items in tableTitle:
                title = items.get_text().strip()
                #获取类型
                if title == "Genres":
                    catag = items.find_next("td")
                    if not catag is None:
                        catag = catag.get_text().strip()
                #获取导演
                elif title == "Director":
                    director = items.find_next("td")
                    if not director is None:
                        director = director.get_text().strip()
                #获取演员
                elif title == "Starring":
                    actor = items.find_next("td")
                    if not actor is None:
                        actor = actor.get_text().strip()
                
        else:            #二类网页    
            #获取标题        
            data['title']=title.get_text().strip()
            table = soup.find('div',id='detail-bullets').find_all("b")
            for items in table:
                itemName = items.get_text()
                #获取演员
                if itemName.strip() == "Actors:":  
                    actor = items.find_next_sibling('a')
                    if not actor is None:
                        actor = actor.get_text().strip() 
                #获取导演
                elif itemName.strip() == "Directors:":  
                    director = items.find_next_sibling('a')
                    if not director is None:
                        director = director.get_text().strip()
                #获取发行日期
                elif itemName.strip() == "DVD Release Date:": 
                    date = items.nextSibling.strip()
                #获取类型
                elif itemName.strip() == "Amazon Best Sellers Rank:": 
                    catag = items.find_next('b')
                    if not catag is None:
                        catag = catag.get_text().strip()
        
        #获取评价数目（两种网页一个格式）
        cus_count = soup.find("h2",attrs={"data-hook": "total-review-count"})
        if not cus_count is None:
            cus_count = cus_count.get_text()  
        data['actor'] = actor
        data['date']=date
        data['director']=director
        data['count']=cus_count
        data['catagory']=catag
        return data

    def _get_data(self,page_url,content):       #使用XPATH查询
        data = {}
        data['url']=page_url

        # imdb = content.xpath(".//*[@data-automation-id='imdb-rating-badge']")  #imdb
        # if(len(imdb)==0):           #检查网站是否有imdb评分
        #     data['imdb'] = False
        # else:
        #     data['imdb'] = True
        title = content.xpath(".//*[@id='a-page']/div[4]/div/div/section/h1")  #标题3or4
        if(len(title)==0):
            #一类网页
            title = content.xpath(".//*[@id='productTitle']")    
            data['title'] = title[0].text.strip()
            data['rating'] = False
            table = content.xpath(".//*[@id='detail-bullets']//b") #详细信息表
            for items in table:                             #扫描详细信息表
                if(items.text and items.text.strip()=='Rated:'):      #检查是否有rating项目
                    data['rating'] = True
                    break
        else:
            #二类网页
            data['title'] = title[0].text.strip()
            data['rating'] = False
            table = content.xpath(".//*[@id='btf-product-details']/following-sibling::*//th") #详细信息表
            for items in table:                             #扫描详细信息表
                if(items.text.strip()=='MPAA rating'):      #检查是否有rating项目
                    data['rating'] = True
                    break
        return data


if __name__=="__main__":
    hp =  HtmlParser()
    downloader = HtmlDownloader()
    url = "https://www.amazon.com/dp/B002PT1D1E"
    pro = None
    hp.test()
    # html = downloader.download(url,pro)
    # with open("test.txt","w",errors='ignore') as w:
    #     w.write(html)
    # hp.parser(url,html)