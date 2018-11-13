from multiprocessing import Pool
import time
import os
 
 
def task(name):
    print('Run task %s (%s)...'%(name,os.getpid()))
    print(time.time())
    #time.sleep(3)
    return name



if __name__=='__main__':
    print('Parent process %s'%os.getpid())
    #p=Pool()
    # for i in range(9):
    #     result = p.apply_async(task,args=(i,))
    #     #print(result.get())
    p = Pool(1)
    rslt = p.map(task,('i',))
    print(rslt)
    print('Waiting for all subprocess done ...')
    p.close()
    p.join()
    print('All subprocess done')