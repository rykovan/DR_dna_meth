#!/usr/bin/env python

import utils
import argparse
import numpy as np
import sys
import torch
import time


parser = argparse.ArgumentParser()
parser.add_argument("fntbl", help="table with merged methylation data")
parser.add_argument("--pc",
                    help="provide a number of components: 2, 4, 6, 12 or more",
                    type=int, default=2)
parser.add_argument("--matrix",
                    help="output file for the filtered matrix, with imputed positions",
                    default="")
parser.add_argument("--evalues",
                    help="output files for eigenvalues",
                    default = "")


args  = parser.parse_args()
fntbl = args.fntbl
pc    = args.pc
fnevalues = args.evalues
fnm = args.matrix


"""
for example
./pca.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --pc 2  
"""


m, tbl = utils.tensor_of_fntbl(fntbl)
#m = m.to('cuda')
#m = m.to('cpu')
#def print_device(name, v):
    #print(f"{name} is in device: {v.device}")
#print_device("m", m)

#start=time.time()

[u, s, v] = torch.pca_lowrank(m, q = pc, center = True, niter = 10)
proj = torch.matmul( torch.transpose(m, 0, 1), u[:, 0:pc])

#stop=time.time()
#print(f"elapsed:{stop-start:.3f}")

proj=proj.to('cpu')
nrow = proj.shape[0]
colnames = np.array([e for e in tbl.columns[3:]]).reshape((nrow, 1))
outm = np.concatenate([colnames,proj.numpy().reshape((len(proj),pc))],axis=1)
outm.dtype='<U36'
np.savetxt(sys.stdout, outm, fmt="%s", delimiter="\t")

if ( fnevalues != "" ):
    np.savetxt(fnevalues, s.numpy(), fmt="%.3e", delimiter="\t")

if (fnm != "" ):

    np.savetxt(fnm, m.numpy(), fmt="%.3e", delimiter="\t")
  
