#!/usr/bin/env python

import utils
import argparse
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
import sys

parser = argparse.ArgumentParser()
parser.add_argument("fntbl", help="table with merged methylation data")
parser.add_argument("--indim2",
                    help="provide a number of indim2: eg:32, 64, 128, 256",
                    type=int, default=32)

args = parser.parse_args()

fntbl = args.fntbl
indim2 = args.indim2

"""
for example
./ae.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --indim2 128 > ae_6types_result.txt 
"""

class Autoencoder(nn.Module):
    def __init__(self, latent_dims):
        super(Autoencoder, self).__init__()
        # encoder
        self.linear1 = nn.Linear(indim1, indim2)
        self.linear2 = nn.Linear(indim2, latent_dims)
        # decoder
        self.linear3 = nn.Linear(latent_dims, indim2)
        self.linear4 = nn.Linear(indim2, indim1)
        
    def encode(self, x):
        x = F.relu(self.linear1(x))
        ##x = torch.sigmoid(self.linear1(x))
        return self.linear2(x)
    
    def decode(self, x):
        x = F.relu(self.linear3(x))
        ##x = torch.sigmoid(self.linear3(x))
        x = torch.sigmoid(self.linear4(x))
        #x = self.linear4(x)
        return x

    def forward(self, x):
        x = self.decode(self.encode(x))
        return x

m, tbl = utils.tensor_of_fntbl(fntbl)
m = torch.transpose(m,0,1)

torch.manual_seed(1)
indim1 = m.shape[1]
indim2 = args.indim2
latent_dims = 2

device = torch.device('cpu')

    
ae = Autoencoder(latent_dims).to(device)
optimizer = optim.Adam(ae.parameters(), lr=1e-3)
print(optimizer, file=sys.stderr)

train_ds = TensorDataset(m, m)

## batch size
bs=64
train_dl = DataLoader(train_ds, batch_size=bs)

nepoch=100
vloss=np.empty((nepoch,))
for i in range(nepoch):
    for (x,y) in train_dl:
        pred = ae.forward(x)
        loss = F.mse_loss(pred, x)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    vloss[i]=loss
    print(f"{i}\tloss={loss:.4g}", file=sys.stderr)


lowdim = ae.encode(m)
x = lowdim.detach().numpy()[:,0]
y = lowdim.detach().numpy()[:,1]

nrow = lowdim.shape[0]
colnames = np.array([e for e in tbl.columns[3:]]).reshape((nrow, 1))
outm = np.column_stack((colnames, x, y))
outm.dtype='<U36'

np.savetxt(sys.stdout, outm, fmt="%s", delimiter = '\t')    
