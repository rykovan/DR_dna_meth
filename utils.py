import numpy as np
import pandas as pd
import re
import sys
import torch


colormap = {'Glioblastoma': 'red',
            'Renal cell carcinoma, NOS':'blue' ,
            'Squamous cell carcinoma, NOS': 'green',
            'Adenocarcinoma, NOS': 'brown',
            'Endometrioid adenocarcinoma, NOS':'orange' ,
            'Infiltrating duct carcinoma, NOS': 'magenta',
            'Malignant melanoma, NOS': 'violet',
            'Ewing Sarcoma': 'cyan',
            'Cholangiocarcinoma': 'coral',
            'Mucinous adenocarcinoma': 'chocolate',
            'Mixed type rhabdomyosarcoma': 'lime',
            'Serrated adenoma': 'darkorange',
            'Carcinoma': 'tan',
            'Metaplastic carcinoma': 'purple',
            'Gliosarcoma': 'olive'}

def read_2d_result(fn2d):
    """
    I think this reads 2d coordinates

    i.e. (coordinates in latent space)
    """
    with open(fn2d) as f:
        df2d = pd.read_csv(f, header=None, sep="\t")
        df2d = df2d.rename(columns = {0: "case_id"})
        df2d.set_index("case_id", inplace = True)
        return df2d

def read_dict(fndict):
    """
    reads the dictionary file

    returns a panda dataframe where trimmes file names are used as index
    """
    with open(fndict) as f:
        df_ids = pd.read_csv(f, header=None, sep="\t")
        df_ids.columns = ["case_id", "uuid", "cancer_type"]
        ## trim file name
        df_ids["case_id"] = df_ids["case_id"].apply(lambda x: x.split(".methylation")[0])
        df_ids.set_index("case_id", inplace = True)
    return df_ids

def tensor_of_fntbl(fntbl):
    """
    reads methylation data.

    filter rows with too mant NAs, and does imputation
    """
    tbl = pd.read_csv(fntbl, sep="\t", header=0)
    tbl.rename(columns = {tbl.columns[0]:re.sub("#", "", tbl.columns[0])},
               inplace = True)
    m = tbl[:][tbl.columns[3:]].to_numpy()
    ## flag NAs
    m[m<0]=np.nan
    nanpos=np.isnan(m)
    ## filter away rows with too many NAs
    thres = int(0.05 * m.shape[1])
    print(f"threshold={thres}",
          file = sys.stderr)
    m = m[np.sum(nanpos, 1) < thres, :]
    print(f"size of m after filtering:{m.shape}",
          file = sys.stderr)
    if ( 0 == m.shape[0] ):
        sys.exit()
    ## imputation
    mmean = np.nanmean(m,1).reshape(m.shape[0], 1)
    m = np.where(np.isnan(m), mmean , m)
    ## only consider rows with high sdev
    sdev = np.nanstd(m,1)
    ranksdev = np.argsort(-sdev)
    m = m[ranksdev[0:2000],:]
    m = torch.tensor(m, dtype=torch.float)
    return m, tbl
