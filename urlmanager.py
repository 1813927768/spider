#coding:utf-8

class UrlManager(object):
    def __init__(self):
        filePath = r'E:\课程\数据仓库\movies.txt'
        self.count = 0      #已提取的链接数
        self.fileRead =  open(filePath,'r',errors='ignore')
        self.url = self.ID = ''  #提取ID
        
    
    def has_new_url(self):
        line = self.fileRead.readline()       
        while(not line is None):    
            #line = line.decode("utf-8") 
            parts = line.split(': ')
            if(len(parts) != 0):                #如果不是空行
                title = parts[0]
                if(title == "product/productId"):  #如果是包含id的行
                    newID = parts[1].strip()       #提取ID
                    if(self.ID != newID):          #如果是新ID
                        self.ID = newID
                        self.url = r'https://www.amazon.com/dp/'+self.ID
                        self.count = self.count+1
                        return True
            line =  self.fileRead.readline()  #下一行
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
                                  
        
    def _get_next_item(self):  #跳到下一条记录
        self._get_next()
        line = self.fileRead.readline()
        line = line.decode("utf-8")
        return line
    
    def _get_next(self):       #跳过无用信息
        for i in range(8):  
                self.fileRead.readline()
                
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
    
