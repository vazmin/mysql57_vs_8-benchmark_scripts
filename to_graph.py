import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import csv
import os, sys

def inno_ops_line(ax_array, ops, inp):
    x = ops[1:,0]
    for idx, lab in enumerate(ops[0][1:]):
        y = [float(v) for v in ops[1:, idx + 1]]
        ax_array[idx].set_title(lab)
        if idx == len(ax_array) - 1:
            ax_array[idx].set_ylabel('Number of Rows', fontsize='small')
            ax_array[idx].set_xlabel('Number of Thread', fontsize='small')
        ax_array[idx].plot(x, y, marker='o', label= inp['source'] + '_' + lab)
        # ax_array[idx].legend(bbox_to_anchor=(1.05, 1), mode='expand', loc='upper left', borderaxespad=0.)
        ax_array[idx].legend(bbox_to_anchor=(1.05, 1), fontsize='x-small', loc='upper left', borderaxespad=0.)

def inno_ops(infos):
    
    fig, (ax_d, ax_i, ax_r, ax_u) = plt.subplots(4, 1)
    
    ax_array = [ax_d, ax_i, ax_r, ax_u]

    for ax in ax_array:
        ax.grid(True)

    for inp in infos:
        ops = np.genfromtxt('%s-%s-%s' % (inp['ip'], inp['port'], 'inno-ops.csv'), delimiter=',', encoding='utf8', dtype=np.str_)
        print(ops)
        inno_ops_line(ax_array, ops, inp)

    # fig.suptitle('InnoDB Row Operations', fontsize=14)
 
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)

    plt.savefig("inno-ops.png")

    return

def read_write_sysbench(infos):
    processAxis(infos, 'read-write-sysbench', 'Transactions Processed')
    return


def tps_sysbench(infos):
    processAxis(infos, 'tps-sysbench', 'Transactions Processed(in sec)')
    return

def transactions_sysbench(infos):
    processAxis(infos, 'transactions-sysbench', 'Transactions Processed')
    return

def cpu(infos):
    processAxis(infos, 'cpu', 'CPU % util')
    return

def processAxis(infos, name, y_label):
    fig, ax = plt.subplots(1, 1)
    # for inp in info:
    for inp in infos:
        ops = getfromtxt(inp, name + '.csv')
        maker = ['o', 's', 'p', '*']
        for idx, lab in enumerate(ops[0][1:]):
            y = [float(v) for v in ops[1:, idx + 1]]
            x = ops[1:,0]
            ax.plot(x, y, marker=maker[idx], label= inp['source'] + '_' + lab)
    ax.set_xlabel('Number of Thread')
    ax.set_ylabel(y_label)
    ax.legend(bbox_to_anchor=(1.05, 1), fontsize='x-small', loc='upper left', borderaxespad=0.)
    plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    ax.grid(True)
    plt.savefig(name + '.png')

    return

def getfromtxt(inp, buffix):
    return np.genfromtxt('%s-%s-%s' % (inp['ip'], inp['port'], buffix), delimiter=',', encoding='utf8', dtype=np.str_)

def main(infos):
    inno_ops(infos)
    read_write_sysbench(infos)
    tps_sysbench(infos)
    transactions_sysbench(infos)
    cpu(infos)

def getPort(host_port):
    hp = host_port.split('-')
    return {'ip': hp[0], 'port': hp[1], 'source': hp[2]} 

if __name__ == "__main__": 

    infos = [getPort(sys.argv[1]), getPort(sys.argv[2])]
    main(infos)