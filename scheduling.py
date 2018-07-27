import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.flow import edmonds_karp

def build_graph(H,W,T,Aw,At,S,L,A):
    G = nx.DiGraph()
    TxH = [(a,b) for a in T for b in H]
    WxH = [(a,b) for a in W for b in H]
    nodes_list = ["source"] + T + TxH + WxH + W + ["sink"]
    G.add_nodes_from(nodes_list)
    #add edges from source to Task layer
    for i in range(len(T)):
        G.add_edge("source", T[i], capacity=S[i])
    #add edges from Task layer to Task x Hour layer
    for i in range(len(T)):
        for j in range(len(TxH)):
            if TxH[j][0] == T[i]:
                w = 0
                if TxH[j][1] in At[i]:
                    w = 1
                G.add_edge(T[i], TxH[j], capacity=w)
    #add edges from TxH to WxH
    for i in range(len(TxH)):
        for j in range(len(WxH)):
            if TxH[i][1] == WxH[j][1]:
                current_task = TxH[i][0]
                current_worker = WxH[j][0]
                task_number = T.index(current_task)
                worker_number = W.index(current_worker)
                if A[task_number][worker_number] == True and TxH[i][1] in At[task_number] and \
                WxH[j][1] in Aw[worker_number]:
                    G.add_edge(TxH[i], WxH[j], capacity=1)

    #add edges from WxH to W
    for i in range(len(W)):
        for j in range(len(WxH)):
            if WxH[j][0] == W[i]:
                w = 0
                if WxH[j][1] in Aw[i]:
                    w = 1
                G.add_edge(WxH[j], W[i], capacity=w)
    #add edges from W to sink
    for i in range(len(W)):
        G.add_edge(W[i], "sink", capacity=L[i])
    return G

def max_flow(G):
    flow_value, flow_dict = nx.maximum_flow(G, 'source', 'sink')
    return flow_dict

def build_timetable(G,flow_dict, H,W,T):
    timetable = {}
    for worker in W:
        for task in T:
            for hour in H:
                if ((task,hour),(worker,hour)) in G.edges():
                    if flow_dict[(task,hour)][(worker,hour)] == 1:
                        timetable[(worker,task,hour)] = 1
    for key, value in timetable.items():
        if value == 1:
            print(key, value)

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
    At2 = ["h1" ]
    At3 = ["h1", "h2", "h3"]
    At4 = ["h1", "h2", "h3"]
    At = [At1,At2,At3,At4]
    S = [2,3,3,3]
    L = [2,3,3,2]
    A = [[True,True,False,True], [True,False,True,True], [False,True,True,True], [True,True,True,True]] #TxW
    G = build_graph(H,W,T,Aw,At,S,L,A)
    flow_dict = max_flow(G)
    build_timetable(G, flow_dict,H,W,T)
