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
    """��Hanlp�����ķִʽ��Ϊ��׼��̬����"word/wp"����list����ʽչʾ��

    ��word_list = ['word1/wp1','word2/wp2'......]

    �����н���̬Ϊ������Ե�Ԫ����ɵ�list��

    ��self.word_list = [word1, word2,......]
    
    ����Ľ��Ϊһ��������Ԫ��Ϊkey���ֵ䣬ֵΪȨ��,

    ��self.score = {word1:weight1, word2:weight2......}

    """
    
    def __init__(self, word_list):
        self.word_list = []
        self.score = defaultdict(float)
        
        for token in word_list:
            tem = token.split("/")
            self.word_list += [tem[0]]
            
        

        
class RandomScoreInitializer(VertexInitializer):
    """����random��������Ȩ�ؽ��г�ʼ��"""
    class_type = "RANDOM"
    

    def __init__(self, word_list):
        
        super(RandomScoreInitializer, self).__init__(word_list)

    def scored_by_unit(self):
        """��ʼ��Ȩ����0-1֮��"""

        for token in self.word_list:
            self.score[token] = rd.random()

        return self.score

    def scored_by_radint(self, start, end):
        """��ʼ��Ȩ��Ϊ����������֮��ȡ�����ֵ"""

        for token in self.word_list:
            self.score[token] = rd.randint(start, end)

        return self.socre

    def scored_by_uniform(self, start, end):
        """��ʼ��Ȩ��Ϊ��������֮��ȡ�������ֵ"""

        for token in self.word_list:
            self.score[token] = rd.uniform(start, end)

        return self.score

        

        


class AverageScoreInitializer(VertexInitializer):
    """ƽ������ʼ��"""
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
    """ʹ�����е��ֵ���и�Ȩ���ֵ�ĸ�ʽΪ{word1:weight1,word2:weight2......}"""
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
    """�ڵ�Ϊ�����ԵΪ�������ﰴ��ĳ��Ҫ��

    ��ʹ�����Զ����ʹ�õ�ǰ�汾��ʼ���ĺ�����ǰ����ֵĴ���

    �ڵ�ĳ�ʼ�����С�Ȩ�ء��롰�ôʳ��ֵĴ�������

    ��Ե������ֻ�С����ʹ�ͬ���ֵĴ�����

    ����֧���Զ������ԣ��������
                  
    ʹ�õ�ͼ������networkx��
    
    """


    def __init__(self, dict_weight, list_relation):
        self.graph = nx.Graph(weight = float, occur_times = int)
        self.dict_weight = dict_weight
        self.list_relation = list_relation

        for token,value in self.dict_weight.items():
            self.graph.add_node(token, weight = value, occur_times = 0)


    def set_word_tag(self, token_name, tag, new_value):
        """���Ĵ���ڵ�����"""
        
        if self.graph.has_node(token_name):
            self.graph.nodes[token_name][tag] = new_value
        else:
            self.graph.add_node(token_name,
                            weight = 1/len(self.graph.nodes),
                            occur_times = 1, tag = new_value)

    def set_edge_tag(self, token1, token2, tag, new_value):
        """���ı�Ե����"""
        
        if self.graph.has_edge(token1, token2):
            self.graph.edges[token1, token2][tag] = new_value
        else:
            self.graph.add_edge(token1, token2, co_times = 1, tag = new_value)
            self.graph.nodes[token1]["occur_times"] += 1
            self.graph.nodes[token2]["occur_times"] += 1

    def delete_word_tag(self, token_name, tag):
        """ɾ���ڵ�����"""
        
        if self.graph.has_node(token_name):
            del self.graph.nodes[token_name][tag]
        else:
            raise KeyError

    def delete_edge_tag(self, token1, token2, tag):
        """ɾ����Ե����"""

        if self.graph.has_edge(token1, token2):
            del self.graph[token1][token2][tag]
        else:
            raise KeyError
        
    def delete_word(self, token_name):
        """ɾ���ڵ�"""

        if self.graph.has_node(token_name):
            self.graph.remove_node(token_name)
        else:
            raise KeyError

    def delete_edge(self, token1, token2):
        """ɾ����Ե"""

        if self.graph.has_edge(token1, token2):
            self.graph.remove_edge(token1, token2)
        else:
            raise KeyError


    def cooccurence_constructor(self, span):
        """ͨ������ǰ�����ӵ�˳�򹹽�ͼ��

        ����

        span --�����Ѱ�Ĵ�����

        ����spanΪ2ʱ��word1����������ʶ��������ӹ�ϵ���Դ����ơ�

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
    """��֧��ʹ��networkx���������޷���ͼ"""
    

    def __init__(self, d, allowed_list):
        """����

        dΪ����������

        allowed_listΪ���������ɸѡ��Ч�����б�

        """

        self.block = d
        self.weight = dict # Ȩ�شʵ�
        self.allowed = allowed_list

    def rank(self, graph, iter_time = int):
        """��Graph����Walk, ��������Vertex Score

        ����iter_timeΪ�����Ĵ���

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
        """��Ч����ɸѡ����δ�������Լ����������ص�ɸѡ"""

        if word not in self.allowed:
            return True


    def get_tokens(self, threshold, withScore = True):
        """����score����threshold������token

        ��withScoreΪTrue���򷵻�һ�������Ĵʵ䣬��Ϊ�ʣ�ֵΪȨ��
        
        ��withScoreΪFalse���򷵻�һ���������б�����Ԫ��Ϊ��

        ���᷵�ص�����

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
        """����topk������Ҫ��token

        ��withScoreΪTrue���򷵻�һ�������Ĵʵ䣬��Ϊ�ʣ�ֵΪȨ��
        
        ��withScoreΪFalse���򷵻�һ���������б�����Ԫ��Ϊ��
        
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
        """�����ض�token��score"""

        return self.weight[token]
            

        
        

        
        



    

    










    
