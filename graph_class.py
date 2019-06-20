from members import *
import sys

class Graph:
    def __init__(self):
        self.residents = []
        self.hospitals = []
        self.edges = []
    
    def print_to_file(self, output_path):
        sys.stdout = open(output_path, 'w')
        print('@PartitionA')
        res = self.residents
        rlen = len(res)
        for i, r in enumerate(res):
            if(i != rlen-1):
                print(r.name + ', ', end='', flush=True)
            else:
                print(r.name + ' ;')
        print('@End\n')

        print('@PartitionB')
        hosp = self.hospitals
        hlen = len(hosp)
        for i, h in enumerate(hosp):
            if(i != hlen-1):
                print(h.name + ' (' + str(h.lq) + ',' + str(h.uq) + '), ', end='', flush=True)
            else:
                print(h.name + ' (' + str(h.lq) + ',' + str(h.uq) + ') ;')
        print('@End\n')

        print('@PreferenceListsA')
        for r in res:
            print(r.name + ' : ', end='', flush=True)
            for i, h in enumerate(r.pref):
                if(i != len(r.pref)-1):
                    print(h.name + ', ', end='', flush=True)
                else:
                    print(h.name + ' ;')
        print('@End\n')

        print('@PreferenceListsB')
        for h in hosp:
            print(h.name + ' : ', end='', flush=True)
            for i, r in enumerate(h.pref):
                if(i != len(h.pref)-1):
                    print(r.name + ', ', end='', flush=True)
                else:
                    print(r.name + ' ;')
        print('@End\n')

    def get_resident(self, name):
        for r in self.residents:
            if(r.name == name):
                return r
        return None

    def get_hospital(self, name):
        for h in self.hospitals:
            if(h.name == name):
                return h
        return None
