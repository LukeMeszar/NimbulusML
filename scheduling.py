import networkx as nx
import matplotlib.pyplot as plt


def build_graph(H,W,T,Aw,At,S,L,A):
    G = nx.DiGraph()
    TxH = [(a,b) for a in T for b in H]
    WxH = [(a,b) for a in W for b in H]
    nodes_list = ["source"] + T + TxH + WxH + W + ["sink"]
    G.add_nodes_from(nodes_list)
    print(len(nodes_list), G.number_of_nodes())
    #add edges from source to Task layer
    for i in range(len(T)):
        G.add_edge("source", T[i], weight=S[i])
    #add edges from Task layer to Task x Hour layer
    i=0
    for i in range(len(T)):
        for j in range(len(TxH)):
            if TxH[j][0] == T[i]:
                w = 0
                if TxH[j][1] in At[i]:
                    w = 1
                G.add_edge(T[i], TxH[j], weight=w)
    #add edges from TxH to WxH
    i=0
    j=0
    for i in range(len(TxH)):
        for j in range(len(WxH)):
            if TxH[i][1] == WxH[j][1]:
                current_task = TxH[i][0]
                current_worker = WxH[j][0]
                task_number = T.index(current_task)
                worker_number = W.index(current_worker)
                if A[task_number][worker_number] == True and TxH[i][1] in At[task_number] and \
                WxH[j][1] in Aw[worker_number]:
                    G.add_edge(TxH[i], WxH[j], weight=1)

    #add edges from WxH to W
    i=0
    j=0
    for i in range(len(W)):
        for j in range(len(WxH)):
            if WxH[j][0] == W[i]:
                w = 0
                if WxH[j][1] in Aw[i]:
                    w = 1
                G.add_edge(WxH[j], W[i], weight=w)
    #add edges from W to sink
    i=0
    for i in range(len(W)):
        G.add_edge(W[i], "sink", weight=L[i])


    pos=nx.circular_layout(G)
    nx.draw(G,pos)
    nx.draw_networkx(G,pos)
    nx.draw_networkx_edge_labels(G,pos)
    plt.draw()
    plt.show()


if __name__ == '__main__':
    H = ["h1", "h2", "h3"]
    W = ["w1", "w2", "w3", "w4"]
    T = ["t1", "t2", "t3", "t4"]
    Aw1 = ["h1", "h2", "h3"]
    Aw2 = ["h1", "h2", "h3"]
    Aw3 = ["h1", "h2", "h3"]
    Aw4 = ["h2", "h3"]
    Aw = [Aw1,Aw2,Aw3,Aw4]
    At1 = ["h1", "h3"]
    At2 = ["h1", "h2", "h3"]
    At3 = ["h1", "h2", "h3"]
    At4 = ["h1", "h2", "h3"]
    At = [At1,At2,At3,At4]
    S = [2,3,3,3]
    L = [2,3,3,2],
    A = [[True,True,False,True], [True,False,True,True], [False,True,True,True], [True,True,True,True]] #TxW
    build_graph(H,W,T,Aw,At,S,L,A)
