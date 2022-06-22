#!/usr/bin/env python
from pathlib import Path
import argparse
import matplotlib.pylab as plt 
import pandas as pd
import re
import torch 
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data
from torch.utils.data import TensorDataset
from torch.utils.data import DataLoader
import numpy as np

"""
for example
./in-out-dist.py pca-latent.txt filename-vs-caseid.txt
"""

def cancer_of_fname(fndict):
    tbl = {}
    with open(fndict, 'r') as fdict:
        for line in fdict:
            line=line.strip()
            fields=line.split("\t")
            k = fields[0].split(".methylation")[0]
            tbl[k] = fields[2]
    return tbl

        

def avg_dist(lat, id0, id1, n):
    lat0 = lat[lat[:, 0] == id0, :]
    lat1 = lat[lat[:, 0] == id1 , :]
    nr0 = lat0.shape[0]
    nr1 = lat1.shape[0]
    idx0 = np.random.randint(low=0, high=nr0, size=n)
    idx1 = np.random.randint(low=0, high=nr1, size=n)
    dist = []
    for i in idx0:
        for j in idx1:
            dist.append(np.linalg.norm(lat0[i,:]-lat1[j,:]))
    return np.mean(dist)
   

if ('__main__' == __name__):
    parser = argparse.ArgumentParser()
    parser.add_argument("fnlat", help = "table with latent space coords")
    parser.add_argument("fndict", help = "dictionary file ==> cancer type")
    parser.add_argument("n", type=int, help="number of random samples for avg dist")
    args = parser.parse_args()
    fnlat = args.fnlat
    fndict = args.fndict
    n = int(args.n)
    cnames = cancer_of_fname(fndict)
    uniqcnames = list(set(cnames.values()))
    ## type of tumor, x, y
    t=[];x=[];y=[]
    with open(fnlat, 'r') as flat:
        for i, line in enumerate(flat):
            line = line.strip()
            fields = line.split("\t")
            k = fields[0]
            t.append(uniqcnames.index(cnames[k]))
            x.append(float(fields[1]))
            y.append(float(fields[2]))
    lat = np.array([t,x,y]).T
    ids = list(set(t))
    distmat = np.empty((len(ids), len(ids)), dtype=np.float)
    for i in ids:
        for j in ids:
            ad = avg_dist(lat, i, j, n)
            print(f"{i}:{j}:{ad}")
            distmat[ids.index(i), ids.index(j)]=ad
    distmat = distmat/np.max(distmat)
    plt.imshow(distmat)
    ###
    
    df_ids = fndict.read_dict()
    clabels = df_ids.result["cancer_type"]
    plt.colorbar()
    plt.xlabel('ambient space')
    plt.ylabel('ambient space')
    plt.xticks(clabels)
    plt.yticks(clabels)
    plt.title("Heat map")
    plt.show()
    figname = fnlat.split("_")[0]
    output_folder = Path(f"/scratch2/emanuele/data-nrykova/distance/output_heatmap_{n}")
    output_folder.mkdir(exist_ok=True)
    plt.savefig(output_folder / f"heatmap_{figname}.png")
