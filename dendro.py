#!/usr/bin/env python

import argparse
from matplotlib import pyplot as plt
import numpy as np
import re
import scipy
import sklearn.metrics
import sys
import utils

from scipy.cluster.hierarchy import dendrogram
from pathlib import Path

output_folder = Path(f"/scratch2/emanuele/data-nrykova/distance/output_dendrogram_hist")
output_folder.mkdir(exist_ok=True)

parser = argparse.ArgumentParser()
parser.add_argument("fntbl", help="table with merged methylation data")

args = parser.parse_args()
fntbl = args.fntbl


"""
for example
./dendro.py /scratch2/emanuele/data-nrykova/merged-chr14-100.txt 
"""
#fntbl="/scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt"
m, tbl = utils.tensor_of_fntbl(fntbl)
colnames = np.array([e for e in tbl.columns[3:]])
nclusters = 6

fndict ="/scratch2/emanuele/data-nrykova/filename-vs-caseid.txt"
df_ids = utils.read_dict(fndict)
ctypes = list(set([df_ids.loc[colnames[i],'cancer_type'] for i in range(len(colnames))]))
print(ctypes)
n= len(ctypes)
mdist = np.empty(int(scipy.special.binom(n,2)),)
for i in range(n):
    for j in range(i, n):
        print(f"{ctypes[i]}--{ctypes[j]}")
        icolidx= list(filter ((lambda e: df_ids.loc[colnames[e], 'cancer_type']==ctypes[i]), range(len(colnames))))
        jcolidx = list(filter ((lambda e: df_ids.loc[colnames[e], 'cancer_type']==ctypes[j]), range(len(colnames))))
        im = m[:, icolidx]
        jm = m[:, jcolidx]
        mdist[ n * i + j - ((i + 2) * (i + 1)) // 2]= np.mean(sklearn.metrics.pairwise_distances(im.T, jm.T))

z = scipy.cluster.hierarchy.linkage(mdist)
scipy.cluster.hierarchy.dendrogram(z, color_threshold=0, labels=[e[0:5] for e in ctypes])
plt.show()
plt.savefig(output_folder / "dendrogram.png")

"""
plt.figure(1)
plt.title("Hierarchical Clustering Dendrogram")
# plot the top three levels of the dendrogram
plot_dendrogram(model)
plt.xlabel("Number of points in node (or index of point if no parenthesis).")
plt.show()
"""


        

