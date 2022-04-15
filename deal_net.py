import random

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import k_clique_communities
from networkx.drawing.nx_agraph import graphviz_layout



class deal_net:
  
    _filepath=''
    _G=nx.DiGraph()
    _MG = nx.MultiGraph()
    def __init__(self,filepath:str)->'None':
        self._filepath = filepath
        self._creat_net()

    def _creat_net(self):
        
        df = pd.read_csv(self._filepath, encoding='utf-8', engine='python')  
        data = df[['source', 'target', 'weight']]
        merge_result_tuples = [tuple(xi) for xi in data.values] 

        count = 0

        for i in merge_result_tuples:
            self._G.add_edge(str(i[0]), str(i[1]), weight=i[2])  
            count += 1
            if count>1500:
                break
        

    def get_net_features(self):
        num_nodes = nx.number_of_nodes(self._G)  
        num_edges = nx.number_of_edges(self._G)  
        density = nx.density(self._G)  
        clusterint_coefficient = nx.average_clustering(self._G)  
        transitivity = nx.transitivity(self._G) 
        reciprocity = nx.reciprocity(self._G)  

        print('节点个数: ', num_nodes)
        print('连接数: ', num_edges)
        print('密度: ', density)
        print('局部聚集系数: ', clusterint_coefficient)
        print('全局聚集系数: ', transitivity)
        print('互惠性: ', reciprocity)
        # 中心度计算
        out_degree = nx.out_degree_centrality(self._G)  
        in_degree = nx.in_degree_centrality(self._G)  
        out_closeness = nx.closeness_centrality(self._G.reverse())  
        in_closeness = nx.closeness_centrality(self._G) 
        betweenness = nx.betweenness_centrality(self._G)  

        print('出度中心度: ', out_degree)
        print('入度中心度: ', in_degree)
        print('出接近中心度: ', out_closeness)
        print('入接近中心度: ', in_closeness)
        print('中介中心度: ', betweenness)
       
        max_ = 0
        s = 0
        for out in out_degree.keys():
            if out_degree[out] > max_: max_ = out_degree[out]
            s = s + out_degree[out]
        print('出度中心势：', (num_nodes * max_ - s) / (num_nodes - 2))

        max_ = 0
        s = 0
        for in_ in in_degree.keys():
            if in_degree[in_] > max_: max_ = in_degree[in_]
            s = s + in_degree[in_]
        print('入度中心势：', (num_nodes * max_ - s) / (num_nodes - 2))

        max_ = 0
        s = 0
        for b in out_closeness.keys():
            if (out_closeness[b] > max_): max_ = out_closeness[b]
            s = s + out_closeness[b]
        print('出接近中心势：', (num_nodes * max_ - s) / (num_nodes - 1) / (num_nodes - 2) * (2 * num_nodes - 3))

        max_ = 0
        s = 0
        for b in in_closeness.keys():
            if (in_closeness[b] > max_): max_ = in_closeness[b]
            s = s + in_closeness[b]
        print('入接近中心势：', (num_nodes * max_ - s) / (num_nodes - 1) / (num_nodes - 2) * (2 * num_nodes - 3))

        max_ = 0
        s = 0
        for b in betweenness.keys():
            if (betweenness[b] > max_): max_ = betweenness[b]
            s = s + betweenness[b]
        print('中介中心势：', (num_nodes * max_ - s) / (num_nodes - 1))


    def clique(self,k):
        '''寻找网络中的社团，最好能着色,有向图Label Propagation，无向图clique'''

        
        G=self._G.to_undirected()
        c_G=list(k_clique_communities(G,k))

        
        pos = nx.spring_layout(G)  
        nx.draw_networkx_nodes(G, pos,node_size=10)
        count = 0
        color = ['m', 'g', 'c', 'b', 'y', 'k', 'w']*3
        for i in range(100):
            hex_color='#{:06x}'.format(random.randint(0, 256**3))
            color.append(hex_color)
       
        for com in c_G:
            count = count + 1
            list_nodes = list(com)
            nx.draw_networkx_nodes(G, pos, list_nodes, node_size=50,node_color=color[count - 1])
            print("Community", count, "is:", list_nodes)
        nx.draw_networkx_edges(G, pos,style='dotted',edge_color='green')
        
        plt.axis("off")
        plt.show()
        print("-"*20)


    def GN(self):
        pass

    def louvain(self):
        pass


    def edge_predict(self):
       
        pass

    def draw(self):
        nx.draw(self._G, with_labels=False,font_weight='bold',)
        elarge = [(u, v) for (u, v, d) in self._G.edges(data=True) if d["weight"] > 0.5]
        esmall = [(u, v) for (u, v, d) in self._G.edges(data=True) if d["weight"] <= 0.5]

        pos = nx.spring_layout(self._G, seed=7) 

        
        nx.draw_networkx_nodes(self._G, pos, node_size=30)

        
        nx.draw_networkx_edges(self._G, pos, edgelist=elarge, node_size=20)
        nx.draw_networkx_edges(
            self._G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color="b", style="dashed",node_size=20
        )

       

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.show()


if __name__=='__main__':
    file_path= r"../source/追溯网络数据/实体追溯网络/溯源三层网络/cluster_tracefrom_df_news.csv"
    bitcoin_net=deal_net(file_path)

    bitcoin_net.clique(3)
