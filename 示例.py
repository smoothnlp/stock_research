from TextReader import NewsReader
import time
import random as rd

Reader = NewsReader(start_page = 29,end_page = 20,Type = "THS")
while Reader.end > 0:
    for i in range(1,26):
        start = time.time()
        time.sleep(3)
        Reader.ListClicker(i)
        time.sleep(rd.randint(15,20))
        Reader.THSTextDealer(Learner = True,PairBuilder = True)
        Reader.WindowsChanger()
        end = time.time()
        print("用时{}秒".format(end-start))
    Reader.Turner()

    
