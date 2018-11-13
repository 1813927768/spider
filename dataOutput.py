#coding:utf-8

#import codecs
import csv

class DataOutput(object):

    def __init__(self):
        #self.fout = codecs.open('output.txt','w',encoding='utf-8')
        fileheader = ["title","rating","imdb","url"]
        self.csvfile = open("output.csv","a",encoding='utf-8')   #result file
        self.writer = csv.writer(self.csvfile)
        # self.writer.writerow(fileheader)
        errheader = ["url","errmsg"] 
        self.errfile = open("err.csv","a",encoding='utf-8')      #err file
        self.errhandle = csv.writer(self.errfile)
        # self.errhandle.writerow(errheader)

        
    
    def store_data(self,data):
        if data is None:
            return
        row = []
        if(data['title'] is None):
            row.append('none')
        else:
            row.append(data['title'])
        if(data['rating'] is None):
            row.append('none')
        else:
            row.append(data['rating'])
        if(data['imdb'] is None):
            row.append('none')
        else:
            row.append(data['imdb'])
        if(data['url'] is None):
            row.append('none')
        else:
            row.append(data['url'])
        
        self.writer.writerow(row)

    def store_err(self,err):
        if err is None:
            return
        self.errhandle.writerow(err)

    def quit_safely(self):
        self.errfile.close()
        self.csvfile.close()

    def flush(self):
        self.errfile.flush()
        self.csvfile.flush()


if __name__=="__main__":
    do =  DataOutput()
    test = {'title':'123','url':'https://www.baidu.com','imdb':True,'rating':False}
    # do.store_data(test)
    err =  ["url","errmsg"] 
    do.store_err(err)