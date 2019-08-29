import json,os
import codecs
import sys
from collections import defaultdict
import re


class Dealer():

    def __init__(self):
        self.size = 0
        
    def PairReader(self,key,background,encode = "gbk"):


        DictOut = defaultdict(int)
        st = ""
        key_word = re.sub(["0-9\!\%\[\]\,\。\……\.\，\|","",key[0]])
        
        with open("Data/{}/{}.txt".format(key[1],key_word),"r",encoding = encode) as f:
            for line in f:
                st += line

        DictIn = eval(st)

                

        for k,v in DictIn.items():

            DictOut[k] = v[background]
            

        return DictOut

    #针对defaultdict使用
    def PairSaver(self,DictIn,key,background,encode = "gbk"):

        DictOut = {}
        key_word = re.sub(["0-9\!\%\[\]\,\。\……\.\，\|","",key[0]])

        for k ,v in DictIn.items():
            
            DictOut[k] = v

        with open("Data/{}/{}.txt".format(key[1],key_word),"w",encoding = encode)as f:
            f.write(str(DictOut))
            f.write("\n")

        return "Done"
    

    

    def VectorRenewer(self,add,key,background):
        st = ""
        key_word = re.sub("[0-9\!\%\[\]\,\。\……\.\，\|\>\<\^\%\*\(\)\@\#\$\&\[\]\{\}\~\`]","",key[0])
        if key_word == "":
            return False
        else:
            try:
                with open ("Data/{}/{}.txt".format(key[1],key_word),"r",encoding = "gbk") as f:
                    for line in f:
                        st += line
                old = eval(st)
                for k,v in add.items():
                    if k in old:
                        if background in old[k]:
                            old[k][background] += v
                        else:
                            old[k][background] == v
                    else:
                        old[k] = {}
                        old[k][background] = v

                with open ("Data/{}/{}.txt".format(key[1],key_word),"w",encoding = "gbk") as f:
                    f.write(str(old))
                    f.write("\n")

            except FileNotFoundError:
                add_new = {}
                for k,v in add.items():
                    add_new[k] = {}
                    add_new[k][background] = v
                if os.path.exists("Data/{}".format(key[1])):
                    with open ("Data/{}/{}.txt".format(key[1],key_word),"w",encoding = "gbk") as f:
                        f.write(str(add_new))
                        f.write("\n")
                else:
                    path = r'E:\量化\ONE\Data\{}'.format(key[1])
                    os.makedirs(path)
                    with open ("Data/{}/{}.txt".format(key[1],key_word),"w",encoding = "gbk") as f:
                        f.write(str(add_new))
                        f.write("\n")
                    
                    
                
                
                    
                    
                
        

    
                
        
        
