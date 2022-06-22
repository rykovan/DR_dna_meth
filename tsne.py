#!/usr/bin/env python

import utils 
import argparse
import numpy as np
from sklearn.manifold import TSNE
import sys
import torch
import time

parser = argparse.ArgumentParser()
parser.add_argument("fntbl",
                    help="table with merged methylation data")
parser.add_argument("--pc", help="number of PCs",
                    type=int, default=2)

parser.add_argument("--per", help="number of perplexity",
                    type=int, default=30)                    
args = parser.parse_args()
fntbl = args.fntbl
pc = args.pc
per = args.per

"""
for example
./tsne.py /scratch2/emanuele/data-nrykova/chr14-merged-1350.txt  --pc 2  
"""
m, tbl = utils.tensor_of_fntbl(fntbl)
m = m.to('cuda')
#m = m.to('cpu')
#def print_device(name, v):
    ##print(f"{name} is in device: {v.device}")
#print_device("m", m)

#start=time.time()

##m=m.T
[u, s, v] = torch.pca_lowrank(m, q = pc, center = True, niter = 10)
proj = torch.matmul(torch.transpose(m, 0, 1), u[:, 0:args.pc])
print(f"{proj.shape}", file=sys.stderr)
proj=proj.to('cpu')
RS = 200
m_embedded = TSNE(random_state=RS, perplexity = per, n_iter=1000, init='pca').fit_transform(proj)

#stop=time.time()
#print(f"elapsed:{stop-start:.3f}")

nrow = m_embedded.shape[0]
colnames = np.array([e for e in tbl.columns[3:]]).reshape((nrow, 1))
outm = np.concatenate([colnames, m_embedded],axis=1)
outm.dtype='<U36'

np.savetxt(sys.stdout, outm, fmt="%s",delimiter = '\t') 


