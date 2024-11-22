#!/usr/bin/env python

from matplotlib import pyplot as plt



###########################################################
# First run testac.zsh and testac_natoms.zsh. They will   #
# generate the data this script uses to claculate errors. #
# Produces plots in four pdf-files and prints aggergated  #
# stats to the terminal.                                  #
###########################################################



def read_testdata(fname):
    with open(fname, 'r') as f:
        
        mse     = {'complex':[], 'real':[]}
        mse_rel = {'complex':[], 'real':[]}
        
        try:
            section = None
            for line in f:
                linesp = line.split('#%;')
                
                if len(linesp) == 1:
                    linebc = line
                else:
                    linebc = linesp[0]

                if not line:
                    continue

                sline = line.split()

                if sline[0] == '========':
                    section = sline[1]
                    continue

                if sline[0] == '---':
                    continue

                if sline[0] == 'mse':
                    mse[section].append(float(sline[2]))
                    continue
                
                if sline[0] == 'mse_rel':
                    mse_rel[section].append(float(sline[2]))
                    continue

        except IOError:
            print('Error when reading from file {f.name}:')
            print(line.rstrip())
            raise
        except KeyError:
            print('Key error at line:')
            print(line.rstrip())
            raise

    return mse, mse_rel


if __name__=='__main__':
    
    print(f"{' Repeats of random number of particles ':=^50}")

    mse, mse_rel = read_testdata('testac.log')
    
    mse_avg     = {'complex':0, 'real':0}
    mse_rel_avg = {'complex':0, 'real':0}

    for ver in mse.keys():
        for e in mse[ver]:
            mse_avg[ver] += e
        mse_avg[ver] /= len(mse[ver])

        for e in mse_rel[ver]:
            mse_rel_avg[ver] += e
        mse_rel_avg[ver] /= len(mse_rel[ver])

        print(f"<mse[{ver}]> = {mse_avg[ver]}")
        print(f"<mse_rel[{ver}]> = {mse_rel_avg[ver]}")

    print(f"Average mse lowered by factor {mse_avg['complex']/mse_avg['real']}")
    print(f"Average mse_rel lowered by factor {mse_rel_avg['complex']/mse_rel_avg['real']}")

    plt.scatter(range(len(mse['complex'])), mse['complex'], color='b', label='complex')
    plt.scatter(range(len(mse['real'])),    mse['real'],    color='r', label='master')
    plt.axhline(mse_avg['complex'], color='b')
    plt.axhline(mse_avg['real'],    color='r')
    plt.yscale('log')
    plt.ylabel('mse')
    plt.xlabel('run #')
    plt.legend()
    plt.savefig('mse.pdf')
    
    plt.clf()

    plt.scatter(range(len(mse_rel['complex'])), mse_rel['complex'], color='b', label='complex')
    plt.scatter(range(len(mse_rel['real'])),    mse_rel['real'],    color='r', label='master')
    plt.axhline(mse_rel_avg['complex'], color='b')
    plt.axhline(mse_rel_avg['real'],    color='r')
    plt.yscale('log')
    plt.ylabel('mse_rel')
    plt.xlabel('run #')
    plt.legend()
    plt.savefig('mse_rel.pdf')


    

    ##########################################
    # Now do for different numbers of atoms. #

    print()
    print(f"{' For increasing number of particles ':=^50}")

    
    mse, mse_rel = read_testdata('testac_natoms.log')

    E = []
    Erel = []
    Eavg = 0
    Erel_avg = 0
    for mc,mr in zip(mse['complex'],mse['real']):
        E.append(mc/mr)
        Eavg += E[-1]
    Eavg /= len(E)
    
    for mc,mr in zip(mse_rel['complex'],mse_rel['real']):
        Erel.append(mc/mr)
        Erel_avg += Erel[-1]
    Erel_avg /= len(Erel)
    
    print(f"mse lowered on average by factor {Eavg}")
    print(f"mse_rel lowered on average by factor {Erel_avg}")

    plt.clf()
    
    plt.scatter(range(2,len(mse['complex'])+2), mse['complex'], color='b', label='complex')
    plt.scatter(range(2,len(mse['real'])+2),    mse['real'],    color='r', label='master')
    plt.scatter(range(2,len(E)+2),              E,              color='k', label='xError')
    plt.axhline(mse_avg['complex'], color='b')
    plt.axhline(mse_avg['real'],    color='r')
    plt.yscale('log')
    plt.ylabel('mse')
    plt.xlabel('#atoms')
    plt.legend()
    plt.savefig('mse_natoms.pdf')
    
    plt.clf()

    plt.scatter(range(2,len(mse_rel['complex'])+2), mse_rel['complex'], color='b', label='complex')
    plt.scatter(range(2,len(mse_rel['real'])+2),    mse_rel['real'],    color='r', label='master')
    plt.scatter(range(2,len(Erel)+2),               Erel,               color='k', label='xError')
    plt.axhline(mse_rel_avg['complex'], color='b')
    plt.axhline(mse_rel_avg['real'],    color='r')
    plt.yscale('log')
    plt.ylabel('mse_rel')
    plt.xlabel('#atoms')
    plt.legend()
    plt.savefig('mse_rel_natoms.pdf')
