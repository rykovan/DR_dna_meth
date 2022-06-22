#!/usr/bin/env python

import numpy as np
import pandas as pd
import sys
from scipy import stats

fndist = sys.argv[1]

tbl = pd.read_csv(fndist, sep="\t", header=None).to_numpy()

ambient = tbl[:,0].tolist()
latent = tbl[:,1].tolist()


corr, pvalue = stats.spearmanr(ambient, latent)
print(corr)
print(f"pvalue={pvalue}")
 