#!/usr/bin/env python
import pandas as pd
import torch.nn.functional as F
import argparse
import numpy as np
import matplotlib.pyplot as plt
import utils
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("fndict", help="table mapping files to cancer type")
parser.add_argument("tsne", help="tsne output file")
parser.add_argument("--outfname", help="provide a PNG file name", default="")
args = parser.parse_args()

output_folder = Path(f"/scratch2/emanuele/data-nrykova/distance/output_tsne_graph")
output_folder.mkdir(exist_ok=True)

"""
example: ./plot_output_tsne.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt tsne_6_types_result.txt --outfname tsne_graph.png 
"""
fndict = args.fndict
fntsne = args.tsne
outfname = args.outfname

colormap = utils.colormap

df2d = utils.read_2d_result(fntsne)
df_ids = utils.read_dict(fndict)

df_result = pd.merge(df_ids, df2d, on="case_id")
df_result["color"] = df_result["cancer_type"].map(colormap)

clabels = df_result["cancer_type"]
ccolors = df_result["color"]

fig, ax = plt.subplots(1,1)
for clabel in set(clabels):
    df = df_result.loc[df_result['cancer_type'] == clabel]
    x = df[1]
    y = df[2]
    color = df.iloc[0]["color"]
    ax.scatter(x, y,
               c = colormap[clabel],
               label = clabel[0:5], s = 10 )
ax.set_xlabel("tsne1")
ax.set_ylabel("tsne2")
ax.set_title("tSNE")
legend1 = ax.legend( ncol = 3 )
plt.figure(1)
plt.show()
if ( outfname != "" ):
    plt.savefig(output_folder / outfname)























