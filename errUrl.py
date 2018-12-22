#coding:utf-8

class UrlManager(object):
    def __init__(self):
        self.filePath = r'G:\\迅雷下载\\crawl\\unknow\\'
        self.count = 0      #已提取的文件数
        fileName = 'unknownHtml'+str(self.count)+'.txt'
        self.fileRead = open(self.filePath+fileName,'r',errors='ignore')
        self.url = self.ID = ''  #提取ID
        
    
    def has_new_url(self):
        line = self.fileRead.readline() 
        if(not line is None and not line == "\n"):
            self.ID = line.strip()
            self.url = r'https://www.amazon.com/dp/'+self.ID
            return True
        elif(self.count < 30):
            print("switch to next file" + str(self.count+1) + ".txt")
            self.count += 1
            fileName = 'unknownHtml'+str(self.count)+'.txt'
            self.fileRead = open(self.filePath+fileName,'r',errors='ignore')
            line = self.fileRead.readline() 
            self.ID = line.strip()
            self.url = r'https://www.amazon.com/dp/'+self.ID
            return True
        else:
            return False
                
        # if not line:
        #     return False
        # else:
        #     while(line):
        #         if(line == '\n'):      #just in case
        #             line = self.fileRead.readline()
        #             line = line.decode("utf-8")
        #         newID = line.split(': ')[1].strip()     #提取ID
        #         if(self.ID != newID):   #如果是新ID
        #             self.ID = newID
        #             self.url = r'https://www.amazon.com/dp/'+self.ID
        #             self.count = self.count+1
        #             self._get_next()    
        #             return True
        #         else:       #如果不是新ID
        #             line = self._get_next_item()  #找到下一个ID
        #     return False
                                  
        
                
    def get_new_url(self):
        return self.url
    
    def get_url_num(self):
        return self.count
    
if __name__=="__main__":
    um =  UrlManager()
    count = 0
    while(um.has_new_url() and count < 1000):
            try:
                #从URL管理器获取新的url
                count = count + 1
                new_url = um.get_new_url()
                print("link %d success: %s" %(count ,new_url))
            except Exception as e:
                print("link %d fail: %s\n" %(count ,new_url),e.args)
    
