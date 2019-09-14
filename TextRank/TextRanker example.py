import TextRanker as TR
word_in = ["我/w","爱/v","中国/n","中国/n","爱/v","我/w"]# 输入的分词结果示例

SI = TR.RandomScoreInitializer(word_in) # 调用权重初始化类
score = SI.scored_by_unit()# 调用类中的具体的初始化方法

Graph = TR.BaseGraph(
                    dict_weight = score,
                    list_relation = SI.word_list)
                    # 调用构图类并构图

Graph.cooccurence_constructor(span = 1)
#Graph.set_edge_tag("我", "爱", "use", 8)
#Graph.delete_edge_tag("我", "爱", "use")
#Graph.delete_word_tag("我", tag = "weight")
#Graph.set_word_tag("我", tag = "weight", new_value = 0.5)
#Graph.delete_edge("我","爱") # BaseGraph方法示例

allowed_list = []
Ranker = TR.TextRanker(d = 0.8, allowed_list = allowed_list)# 调用textrank工具
Ranker.rank(Graph.graph, iter_time = 10)# 迭代求权重，迭代次数自定义，此处为10
out1 = Ranker.get_topk(topk = 2)# 返回weight前二的词
print(out1)

