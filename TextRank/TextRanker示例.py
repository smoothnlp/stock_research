import TextRanker as TR
In = ["我/w","爱/v","中国/n","中国/n","爱/v","我/w"]
SI = TR.RandomScoreInitializer(In)
Score = SI.Unit()
Graph = TR.CooccurenceConstructor(dict_weight = Score,list_relation = SI.object,span = 1)
Ranker = TR.TextRanker(d = 0.8,graph = Graph.graph)
Ranker.Rank(args = 10)
out = Ranker.get_token_score("我")
print(out)
