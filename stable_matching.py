from members import *

def compute_stable(g):
    q = []
    for r in g.residents:
        q.append(r)

    while(len(q) > 0):
        curRes = q.pop(0)
        hospToPropose = curRes.pref[curRes.prefPtr]
        curRes.prefPtr += 1
        if(len(hospToPropose.matched) < hospToPropose.uq):
            curRes.matched = hospToPropose
            hospToPropose.matched.append(curRes)
            if(hospToPropose.worstRankRes == None):
                hospToPropose.worstRankRes = curRes
            elif(hospToPropose.get_rank(curRes.name) > hospToPropose.get_rank(hospToPropose.worstRankRes.name)):
                hospToPropose.worstRankRes = curRes
        else:
            worstRankRes = hospToPropose.worstRankRes
            if(hospToPropose.get_rank(curRes.name) > hospToPropose.get_rank(worstRankRes.name)):
                if(curRes.prefPtr != len(curRes.pref)):
                    q.append(curRes)
            else:
                hospToPropose.matched.remove(worstRankRes)
                worstRankRes.matched = None
                if(worstRankRes.prefPtr != len(worstRankRes.pref)):
                    q.append(worstRankRes)
                curRes.matched = hospToPropose
                hospToPropose.matched.append(curRes)
                hospToPropose.compute_worst_rank_res()

def get_stable_matching(g):
    compute_stable(g)
    m = []
    for r in g.residents:
        r_ind = r.name[1:]
        h = r.matched
        if(h != None):
            h_ind = h.name[1:]
            m.append(Edge(r_ind, h_ind))
    
    return m
