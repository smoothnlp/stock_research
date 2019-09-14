# -*- encoding: gbk -*-
# By Begoenix


from __future__ import absolute_import, unicode_literals
from operator import itemgetter
import networkx as nx
import random as rd
from collections import defaultdict




#-------------------------------ScoreInitializer--------------------------------
#===============================================================================



class VertexInitializer():
    """以Hanlp给出的分词结果为标准形态，即"word/wp"并以list的形式展示，

    即word_list = ['word1/wp1','word2/wp2'......]

    类内中介形态为词与词性的元组组成的list，

    即self.word_list = [word1, word2,......]
    
    输出的结果为一个以以上元组为key的字典，值为权重,

    即self.score = {word1:weight1, word2:weight2......}

    """
    
    def __init__(self, word_list):
        self.word_list = []
        self.score = defaultdict(float)
        
        for token in word_list:
            tem = token.split("/")
            self.word_list += [tem[0]]
            
        

        
class RandomScoreInitializer(VertexInitializer):
    """基于random函数对字权重进行初始化"""
    class_type = "RANDOM"
    

    def __init__(self, word_list):
        
        super(RandomScoreInitializer, self).__init__(word_list)

    def scored_by_unit(self):
        """初始化权重在0-1之间"""

        for token in self.word_list:
            self.score[token] = rd.random()

        return self.score

    def scored_by_radint(self, start, end):
        """初始化权重为给定的整数之间取随机整值"""

        for token in self.word_list:
            self.score[token] = rd.randint(start, end)

        return self.socre

    def scored_by_uniform(self, start, end):
        """初始化权重为给定的数之间取随机浮点值"""

        for token in self.word_list:
            self.score[token] = rd.uniform(start, end)

        return self.score

        

        


class AverageScoreInitializer(VertexInitializer):
    """平均数初始化"""
    class_type = "AVERAGE"


    def __init__(self, word_list):
        
        super(AverageScoreInitializer, self).__init__(word_list)

    def scored_by_simple(self):
        for token in self.word_list:
            self.score[token] = 1/len(self.word_list)

        for token,value in self.score.items():
            self.score[token] = 1/len(self.score)

        return self.score



class CustomeInitializer(VertexInitializer):
    """使用已有的字典进行赋权，字典的格式为{word1:weight1,word2:weight2......}"""
    class_type = "CUSTOM"


    def __init__(self, word_list, reference):
        self.reference = reference
        super(CustomeInitializer,self).__init__(word_list)
        
    def scored_by_dict(self):
        for token in self.word_list:
            if token in self.reference:
                self.score[token] = self.reference[token]
            else:
                self.score[token] = 1 / len(sel.word_list)

        return self.score


#===============================================================================







#-------------------------------GraphConstructor--------------------------------
#===============================================================================


class BaseGraph():
    """节点为词语，边缘为两个词语按照某种要求

    （使用者自定义或使用当前版本初始化的函数）前后出现的次数

    节点的初始属性有“权重”与“该词出现的次数”，

    边缘的属性只有“两词共同出现的次数”

    该类支持自定义属性，详见下文
                  
    使用的图表依赖networkx包
    
    """


    def __init__(self, dict_weight, list_relation):
        self.graph = nx.Graph(weight = float, occur_times = int)
        self.dict_weight = dict_weight
        self.list_relation = list_relation

        for token,value in self.dict_weight.items():
            self.graph.add_node(token, weight = value, occur_times = 0)


    def set_word_tag(self, token_name, tag, new_value):
        """更改词语节点属性"""
        
        if self.graph.has_node(token_name):
            self.graph.nodes[token_name][tag] = new_value
        else:
            self.graph.add_node(token_name,
                            weight = 1/len(self.graph.nodes),
                            occur_times = 1, tag = new_value)

    def set_edge_tag(self, token1, token2, tag, new_value):
        """更改边缘属性"""
        
        if self.graph.has_edge(token1, token2):
            self.graph.edges[token1, token2][tag] = new_value
        else:
            self.graph.add_edge(token1, token2, co_times = 1, tag = new_value)
            self.graph.nodes[token1]["occur_times"] += 1
            self.graph.nodes[token2]["occur_times"] += 1

    def delete_word_tag(self, token_name, tag):
        """删除节点属性"""
        
        if self.graph.has_node(token_name):
            del self.graph.nodes[token_name][tag]
        else:
            raise KeyError

    def delete_edge_tag(self, token1, token2, tag):
        """删除边缘属性"""

        if self.graph.has_edge(token1, token2):
            del self.graph[token1][token2][tag]
        else:
            raise KeyError
        
    def delete_word(self, token_name):
        """删除节点"""

        if self.graph.has_node(token_name):
            self.graph.remove_node(token_name)
        else:
            raise KeyError

    def delete_edge(self, token1, token2):
        """删除边缘"""

        if self.graph.has_edge(token1, token2):
            self.graph.remove_edge(token1, token2)
        else:
            raise KeyError


    def cooccurence_constructor(self, span):
        """通过词语前后连接的顺序构建图表

        参数

        span --向后搜寻的次数，

        例如span为2时，word1与其后两个词都存在连接关系，以此类推。

        """

        for n in range(len(self.list_relation)):
            word_now = self.list_relation[n]
            num_now = n
            
            for w in range(num_now+1, num_now+1+span):
                if w >= len(self.list_relation):
                    break
                else:
                    word_next = self.list_relation[w]
                    if (word_now, word_next) in self.graph.edges():
                        self.graph[word_now][word_next]["co_times"] += 1
                    else:
                        self.graph.add_edge(word_now, word_next, co_times = 1)
                    self.graph.nodes[word_now]["occur_times"] += 1
                    self.graph.nodes[word_next]["occur_times"] += 1
                    






#===============================================================================







#----------------------------------TextRanker-----------------------------------
#===============================================================================

class TextRanker():
    """仅支持使用networkx包构建的无方向图"""
    

    def __init__(self, d, allowed_list):
        """参数

        d为阻塞参数；

        allowed_list为输入的用以筛选有效词语列表。

        """

        self.block = d
        self.weight = dict # 权重词典
        self.allowed = allowed_list

    def rank(self, graph, iter_time = int):
        """在Graph进行Walk, 迭代计算Vertex Score

        参数iter_time为迭代的次数

        """
        for i in range(iter_time):
            for token in graph.nodes():
                weight_sum = sum(graph.edges[token, e]["co_times"]
                                 * graph.nodes[e]["weight"]
                                 for e in graph.adj[token])
                
                occur_times = graph.nodes[token]["occur_times"]
                weight_final = weight_sum / occur_times
                                
                graph.nodes[token]["weight"] = \
                (1 - self.block) + self.block * weight_final

        self.weight = nx.get_node_attributes(graph, "weight")
        sorted_list = sorted(
                        self.weight.items(),
                        key = lambda x:x[1],
                        reverse = True)

        word_tem = {}
        for token in sorted_list:
            token = token[0]
            word_tem[token] = self.weight[token]

        self.weight = word_tem

    def word_selecter(self,word):
        """有效词语筛选器，未来还可以加入与词性相关的筛选"""

        if word not in self.allowed:
            return True


    def get_tokens(self, threshold, withScore = True):
        """返回score超过threshold的所有token

        若withScore为True，则返回一个排序后的词典，键为词，值为权重
        
        若withScore为False，则返回一个排序后的列表，表中元素为词

        不会返回单个字

        """

        list_out = []
        
        for token,value in self.weight.items():
            if value >= threshold and self.word_selecter(token):
                list_out += [token]
            elif value >= threshold and not self.word_selecter(token):
                continue            
            elif value <= threshold:
                break

        if withScore:
            dict_out = {}
            for token in list_out:
                dict_out[token] = self.weight[token]
                
            return dict_out

        else:
            
            return list_out

    def get_topk(self, topk = int, withScore = True):
        """返回topk个最重要的token

        若withScore为True，则返回一个排序后的词典，键为词，值为权重
        
        若withScore为False，则返回一个排序后的列表，表中元素为词
        
        """
        num_res = topk
        if withScore:
            dict_out = {}
            for token, value in self.weight.items():
                if num_res > 0 and self.word_selecter(token):
                    dict_out[token] = value
                    num_res -= 1
                elif num_res > 0 and not self.word_selecter(token):
                    continue
                elif num_res < 0:
                    break
                    
            return dict_out

        else:
            list_out = []
            for token, value in self.weight.items():
                if num_res > 0 and self.word_selecter(token):
                    list_out += [token]
                    num_res -= 1
                elif num_res > 0 and not self.word_selecter(token):
                    continue
                elif num_res < 0:
                    break

            return list_out


    def get_token_score(self, token):
        """返回特定token的score"""

        return self.weight[token]
            

        
        

        
        



    

    










    
