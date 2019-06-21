def generate_max_card_lp(g, path, option):
    f = open(path, "w")
    f.write("maximize\nsize: ")
    for i, edge in enumerate(g.edges):
        f.write(edge.name + ' ')
        if(i != len(g.edges)-1):
            f.write('+ ')

    f.write('\n\nst\n')
    for r in g.residents:
        r_ind = r.name[1:]
        f.write(r.name + ': ')
        for i, h in enumerate(r.pref):
            h_ind = h.name[1:]
            f.write('x_' + r_ind + '_' + h_ind + ' ')
            if(i != len(r.pref)-1):
                f.write('+ ')
        f.write('<= 1\n')

    for h in g.hospitals:
        h_ind = h.name[1:]
        if(len(h.pref) > 0):
            f.write(h.name + '_uq: ')
            for i, r in enumerate(h.pref):
                r_ind = r.name[1:]
                f.write('x_' + r_ind + '_' + h_ind + ' ')
                if(i != len(h.pref)-1):
                    f.write('+ ')
            f.write('<= ' + str(h.uq) + '\n')

    if(option == 1):
        for h in g.hospitals:
            h_ind = h.name[1:]
            if(len(h.pref) > 0 and len(h.matched) > 0):
                f.write(h.name + '_lq: ')
                for i, r in enumerate(h.pref):
                    r_ind = r.name[1:]
                    f.write('x_' + r_ind + '_' + h_ind + ' ')
                    if(i != len(h.pref)-1):
                        f.write('+ ')
                f.write('>= ' + str(len(h.matched)) + '\n')

    f.write('\nbin\n')
    for i, edge in enumerate(g.edges):
        f.write(edge.name + ' ')
        if(i%31 == 0 and i != 0):
            f.write('\n')
    f.write('\n')

    f.write('\nend')
    f.close()
