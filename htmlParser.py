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
        # with open(r'test/test.txt','r',encoding='utf-8') as fileReader:
        #     html = fileReader.read()
        url = "https://www.amazon.com/dp/B0042AGNA0"
        soup = BeautifulSoup(open(r'test/test.txt'),"lxml")
        #print(soup.find_all('span'))
        new_data = self._get_new_data(url,soup)


            
    def _get_new_data(self,page_url,soup):   #使用beautifulsoup查询
        data={}
        data['url']=page_url
        title = soup.find('span',id="productTitle")
        data['title']=title.get_text().strip()
        table = soup.find('div',id='detail-bullets').find_all("b")
        catag = date = actor = director = ""
        for items in table:
            itemName = items.get_text()
            if itemName.strip() == "Actors:":  #获取演员
                actor = items.find_next_sibling('a')
                if not actor is None:
                    actor = actor.get_text().strip() 
            elif itemName.strip() == "Directors:":  #获取导演
                director = items.find_next_sibling('a')
                if not director is None:
                    director = director.get_text().strip()
            elif itemName.strip() == "DVD Release Date:": #获取发行日期
                date = items.nextSibling.strip()
            elif itemName.strip() == "Amazon Best Sellers Rank:": #获取类型
                catag = items.find_next('b')
                if not catag is None:
                    catag = catag.get_text().strip()
        cus_count = soup.find("h2",attrs={"data-hook": "total-review-count"})
        if not cus_count is None:
            cus_count = cus_count.get_text()  #获取评价数目
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
    url = "https://www.amazon.com/dp/B0042AGNA0"
    pro = None
    hp.test()
    #html = downloader.download(url,pro)
    #hp.parser(url,html)