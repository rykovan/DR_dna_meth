#!/usr/bin/env python

from pathlib import Path
import sklearn
from sklearn.neighbors import kneighbors_graph
import scipy.sparse 
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import seaborn as sb
from scipy import stats

"""
example: ./dist_neig.py /scratch2/emanuele/data-nrykova/distance/mfile.txt /scratch2/emanuele/data-nrykova/distance/pca_latent.txt 
/scratch2/emanuele/data-nrykova/distance/tsne_latent.txt /scratch2/emanuele/data-nrykova/distance/ae_latent.txt 
--means means_30.png --jac jac_30.png --spy spy_30.png
"""
parser = argparse.ArgumentParser()
#parser.add_argument("ambient", help="matrix-file")
#parser.add_argument("latent1", help="latent-space file pca")
#parser.add_argument("latent2", help="latent-space file tsne")
#parser.add_argument("latent3", help="latent-space file ae")
parser.add_argument("ro", type=int, default=1349, help="provide number of rows")
parser.add_argument("nei", type=int, default=30, help="number of neighbours")
parser.add_argument("--means", help="means file png name ")
parser.add_argument("--jac", help="file name png format for Jaccard distance")
parser.add_argument("--spy", help="sparse matrix png name ")

args = parser.parse_args()
#ambient = args.ambient
#latent1 = args.latent1
#latent2 = args.latent2
#latent3 = args.latent3
ambient_path = "/home/nrykova/masteruab/MethylationDNA/mfile.txt"
latent1_path = "/home/nrykova/masteruab/MethylationDNA/pca_latent.txt"
latent2_path = "/home/nrykova/masteruab/MethylationDNA/tsne_latent.txt"
latent3_path = "/home/nrykova/masteruab/MethylationDNA/ae_latent.txt"

ro = args.ro
nei = args.nei
means = args.means
jac = args.jac
spy = args.spy

# create folder
output_folder = Path(f"/scratch2/emanuele/data-nrykova/distance/output_{ro}_{nei}")
output_folder.mkdir(exist_ok=True)


def make_graph(path, sep="\t", slicer=slice(1, 3)):
    tbl = pd.read_csv(path, sep=sep, header=None)
    array = tbl.iloc[:ro, slicer].to_numpy()
    graph = sklearn.neighbors.kneighbors_graph(
        array, n_neighbors=nei, mode="distance", metric="euclidean"
    )
    return graph

def jac(ambient, latent):
    result = np.zeros((ambient.shape[0],), dtype=np.float32)
    for i in range(ambient.shape[0]):
        ramb, camb, _ = scipy.sparse.find(ambient[i, :])
        rlat, clat, _ = scipy.sparse.find(latent[i, :])
        ambidx = set(zip(ramb, camb))
        latidx = set(zip(rlat, clat))
        result[i] = 1.0 - len(ambidx.intersection(latidx)) / len(ambidx.union(latidx))
    return result

ambient = make_graph(ambient_path, slicer=slice(None, None))
latent1 = make_graph(latent1_path)
latent2 = make_graph(latent2_path)
latent3 = make_graph(latent3_path)

assert ambient.shape == latent1.shape
assert ambient.shape == latent2.shape
assert ambient.shape == latent3.shape

jac1 = jac(ambient, latent1)
jac2 = jac(ambient, latent2)
jac3 = jac(ambient, latent3)
print(jac1)


jac1_mean = jac1.mean()
jac2_mean = jac2.mean()
jac3_mean = jac3.mean()

#print mean hist - jac mean 
plt.figure(1)
plt.hist([[jac1_mean,], [jac2_mean,], [jac3_mean,]], label=['pca', 'tsne', 'ae'], color=['red','blue','green'])
plt.title('Mean, Jaccard distance, PCA, t-SNE, AE')
plt.xlabel('value of mean')
plt.ylabel('')
patch1 = mpatches.Patch(color='red', label='PCA')
patch2 = mpatches.Patch(color='blue', label='t-SNE')
patch3 = mpatches.Patch(color='green', label='AE')
plt.legend(handles=[patch1, patch2, patch3])
plt.show()
plt.savefig(output_folder / f"means_{args.ro}_{args.nei}.png")


# Jaccard distance histograms
plt.figure(2)
plt.hist([jac1, jac2, jac3], label=['pca', 'tsne', 'ae'], color=['red','blue','green'])
plt.xlabel('Value of Jac.distance')
plt.ylabel('Frequency')
plt.title('Jaccard distance, PCA, t-SNE, AE')
patch1 = mpatches.Patch(color='red', label='PCA', alpha=0.5)
patch2 = mpatches.Patch(color='blue', label='t-SNE', alpha=0.5)
patch3 = mpatches.Patch(color='green', label='AE', alpha=0.5)
plt.legend(handles=[patch1, patch2, patch3])
plt.show()
plt.savefig(output_folder / f"jac_{args.nei}.png")

# sparse matrices
plt.figure(3)
fig, axs = plt.subplots(2, 2)
axs[0, 0].spy(ambient)
axs[0, 0].set_title('Ambient(original)matrix')
axs[0, 1].spy(latent1)
axs[0, 1].set_title('Latent, PCA')
axs[1, 0].spy(latent2)
axs[1, 0].set_title('Latent, t-SNE')
axs[1, 1].spy(latent3)
axs[1, 1].set_title('Latent, AE')
fig.tight_layout()
plt.show()
plt.savefig(output_folder / f"spy_{args.ro}_{args.nei}.png")

with open(output_folder / f"jac_{args.ro}_{args.nei}.txt", "wt") as f:
    f.write("PCA\t{}\n".format(jac1))
    f.write("TSNE\t{}\n".format(jac2))
    f.write("AE\t{}\n".format(jac3))

shapiro_test1 = stats.shapiro(jac1)
shapiro_test2 = stats.shapiro(jac2)
print(shapiro_test1.statistic)
print(shapiro_test2.statistic)
l = shapiro_test1.pvalue
s = shapiro_test2.pvalue
alpha = 0.05
if l > alpha:
	print('Sample looks Gaussian (fail to reject H0)')
else:
	print('Sample does not look Gaussian (reject H0)')  

if s > alpha:
	print('Sample looks Gaussian (fail to reject H0)')
else:
	print('Sample does not look Gaussian (reject H0)')       