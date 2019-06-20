class Resident:
    # constructor
    def __init__(self, name):
        self.name = name
        self.pref = []
        self.matched = None
        self.prefPtr = 0
        self.worstRankHosp = None

    def get_index(self):
        return self.name[1:]

    def get_pref_size(self):
        return len(self.pref)

    def get_rank(self, hosp_name):
        for i, h in enumerate(self.pref):
            if(h.name == hosp_name):
                return i+1
        return 9999999999

    # returns true if resident prefers h1 over h2
    def is_better_preferred(self, h1, h2):
        return self.get_rank(h1) < self.get_rank(h2)

    def compute_worst_rank_hosp(self):
        worstRank = -1
        worstRankHospital = None
        for h in self.matched:
            curRank = self.get_rank(h.name)
            if(curRank > worstRank):
                worstRank = curRank
                worstRankHospital = h
        self.worstRankHosp = worstRankHospital

    # returns true if resident is matched to hosp
    def is_matched_to(self, hosp):
        for h in self.matched:
            if(h.name == hosp.name):
                return True
        return False

class Hospital:
    # constructor
    def __init__(self, name, lq, uq):
        self.name = name
        self.pref = []
        self.lq = lq
        self.uq = uq
        self.matched = []
        self.worstRankRes = None

    def is_feasible_matching(self):
        return len(self.matched) <= self.uq

    def get_index(self):
        return self.name[1:]

    def get_pref_size(self):
        return len(self.pref)

    def get_rank(self, res_name):
        for i, r in enumerate(self.pref):
            if(r.name == res_name):
                return i+1

    def is_better_preferred(self, r1, r2):
        return self.get_rank(r1) < self.get_rank(r2)

    def compute_worst_rank_res(self):
        worstRank = -1
        worstRankResident = None
        for r in self.matched:
            curRank = self.get_rank(r.name)
            if(curRank > worstRank):
                worstRank = curRank
                worstRankResident = r
        self.worstRankRes = worstRankResident

class Edge:
    def __init__(self, r_ind, h_ind):
        self.name = 'x_' + r_ind + '_' + h_ind
        self.r_ind = r_ind
        self.h_ind = h_ind
