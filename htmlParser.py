#coding:utf-8

#from bs4 import BeautifulSoup
from lxml import etree

class HtmlParser(object):
    
    def parser(self,page_url,html_cont):
        if page_url is None or html_cont is None:
            return
        #soup = BeautifulSoup(html_cont,'html.parser')
        #new_data = self._get_new_data(page_url,soup)
        content = etree.HTML(html_cont)
        new_data = self._get_data(page_url,content)
        return new_data
    
    def test(self):
        with open('test1.txt','r',encoding='utf-8') as fileReader:
            html = fileReader.read()
        content = etree.HTML(html)
        data = {}
        title = content.xpath(".//*[@id='productTitle']")    
        data['title'] = title[0].text.strip()
        data['rating'] = False
        table = content.xpath(".//*[@id='detail-bullets']//b") #详细信息表
        for items in table:                             #扫描详细信息表
            if(items.text and items.text.strip()=='Rated:'):      #检查是否有rating项目
                data['rating'] = True
                print("success")
                break


            
    # def _get_new_data(self,page_url,soup):   #使用beautifulsoup查询
    #             data={}
    #             data['url']=page_url
    #             title = soup.find('span',id="productTitle").find('h1')
    #             data['title']=title.get_text()
    #             summary = soup.find('div',id='detail-bullets').find('div',class_='a-box a-box-thumbnail')
    #             summary = summary.next_sibling
    #             data['rated']=summary.get_text()
    #             return data

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
    hp.test()