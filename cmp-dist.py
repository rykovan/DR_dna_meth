#!/usr/bin/env python


import argparse
import numpy as np
import pandas as pd
import sys


parser = argparse.ArgumentParser()

parser.add_argument("out2d", help="2d output")
parser.add_argument("matrix", help="filtered matrix, with imputed positions")

args  = parser.parse_args()

fnout2d = args.out2d
fnm = args.matrix

m2d = pd.read_csv(fnout2d, sep="\t", header=None)
print(f"m2d -- nrow:{m2d.shape[0]} ncol:{m2d.shape[1]}", file=sys.stderr)
m2d = m2d.iloc[:, 1:].to_numpy()
print(f"m2d -- nrow:{m2d.shape[0]} ncol:{m2d.shape[1]}", file=sys.stderr)
m = pd.read_csv(fnm, sep="\t", header=None).to_numpy().T
[nrow, ncol]=m.shape
print(f"m -- nrow:{nrow} ncol:{ncol}", file=sys.stderr)
ss=1350 #sample size
ridx = np.random.randint(0, nrow, ss)
for i in range(len(ridx)):
    for j in range(i+1, len(ridx)):
        d1 = np.linalg.norm(m[i,:] - m[j,:])
        d2 = np.linalg.norm(m2d[i,:] - m2d[j,:])
        print(f"{d1:.3g}\t{d2:.3g}")
