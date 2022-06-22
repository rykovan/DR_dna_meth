#!/usr/bin/env python
import pandas as pd
import torch.nn.functional as F
import argparse
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

#usage
# ./eig_var.py --eigenplot eigenplot.png --varplot varplot.png

parser = argparse.ArgumentParser()
parser.add_argument("--eigenplot", help="eigenplot output file name, png", default="")
parser.add_argument("--varplot", help="varianceplot output file name, png", default="")
args = parser.parse_args()

output_folder = Path(f"/scratch2/emanuele/data-nrykova/distance/output_eigenvalues_and_variance")
output_folder.mkdir(exist_ok=True)

eigenplot = args.eigenplot
varplot = args.varplot


tbl = pd.read_csv("/home/nrykova/masteruab/MethylationDNA/evalues.txt", sep="\t", header=None)
eigen = tbl.iloc[:, 0]
print(eigen)
#barplot of 12 eigenvalues
plt.figure(1)
#barplot of 12 eigenvalues
x = ['1egv', '2egv', '3egv', '4egv', '5egv', '6egv', '7egv', '8egv', '9egv', '10egv', '11egv', '12egv']
plt.bar(x, eigen)
plt.title('eigenvalues')
plt.xlabel('')
plt.ylabel('value')      
plt.show()
plt.savefig(output_folder / eigenplot)


# plot of cumulative explained variance

plt.figure(2)
plt.plot(np.cumsum(eigen))
plt.xlim(xmax = len(eigen), xmin = 0)
plt.ylim(ymax = 2000, ymin = 0)
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance')
plt.show()
plt.savefig(output_folder / varplot)

