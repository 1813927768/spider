#coding:utf-8

#import csv
#import threading


class DataOutput(object):

    def __init__(self):
        self.fout = open('output.txt','w')
        self.ferr = open('err.txt','w')
        # csv输出
        # fileheader = ["title","rating","imdb","url"]
        # self.csvfile = open("output.csv","a",encoding='utf-8')   #result file
        # self.writer = csv.writer(self.csvfile)
        # self.writer.writerow(fileheader)
        # errheader = ["url","errmsg"] 
        # self.errfile = open("err.csv","a",encoding='utf-8')      #err file
        # self.errhandle = csv.writer(self.errfile)
        # self.errhandle.writerow(errheader)

    def write_line(self,data,file):
        if file==True:
            self.fout.write(data)
            self.fout.write("\n")
        else:
            self.ferr.write(data)
            self.ferr.write("\n")

    
    def store_data(self,data):
        if data is None:
            return
        # row = []
        # if(data['title'] is None):
        #     row.append('none')
        # else:
        #     row.append(data['title'])
        # if(data['rating'] is None):
        #     row.append('none')
        # else:
        #     row.append(data['rating'])
        # if(data['imdb'] is None):
        #     row.append('none')
        # else:
        #     row.append(data['imdb'])
        # if(data['url'] is None):
        #     row.append('none') 
        # else:
        #     row.append(data['url'])      
        # self.writer.writerow(row)
        self.write_line("title: "+str(data["title"]),True)
        self.write_line("director: "+str(data["director"]),True)
        self.write_line("actor: "+str(data["actor"]),True)
        self.write_line("release-date: "+str(data["date"]),True)
        self.write_line("catagory: "+str(data["catagory"]),True)
        self.write_line("customer-number: "+str(data["count"]),True)
        self.write_line("url: "+str(data["url"]),True)
        self.write_line("",True)


    def store_err(self,err):
        if err is None:
            return
        # self.errhandle.writerow(err)
        self.write_line(err[0],False)
        self.write_line(str(err[1]),False)
        self.write_line("",False)

    def quit_safely(self):
        # self.errfile.close()
        # self.csvfile.close()
        pass

    def flush(self):
        # self.errfile.flush()
        # self.csvfile.flush()
        self.ferr.flush()
        self.fout.flush()


if __name__=="__main__":
    do =  DataOutput()
    test = {'title':'123','url':'https://www.baidu.com','imdb':True,'rating':False}
    # do.store_data(test)
    err =  ["url","errmsg"] 
    #do.store_err(err)