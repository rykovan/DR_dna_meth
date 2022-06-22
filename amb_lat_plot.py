#!/usr/bin/env python
import matplotlib.pyplot as plt
import pandas as pd
import torchvision.datasets as dset
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import numpy as np
import pandas as pd
import sys
from scipy import stats
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("distfile", help="distance ambient/latent space pca,ae,tsne file")
args  = parser.parse_args()
distfile = args.distfile

fname = distfile.split(".")[0]
output_folder = Path(f"/scratch2/emanuele/data-nrykova/distance/output_{fname}")
output_folder.mkdir(exist_ok=True)

# distance plot 

tbl = pd.read_csv(distfile, sep="\t", header=None)
ambient = tbl.iloc[:, 0]
latent = tbl.iloc[:, 1]
plt.plot(ambient, latent, 'r+')
plt.xlabel('ambient space')
plt.ylabel('latent space')

title = fname.rsplit("_", 1)[-1]
plt.title(f"{title}")

plt.show()
plt.savefig(output_folder / f"{fname}.png")
