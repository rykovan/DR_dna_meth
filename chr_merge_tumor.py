#!/usr/bin/env python
import pandas as pd
df1 = pd.read_csv("/scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt", delimiter="\t") 
df2 = pd.read_csv("/scratch2/emanuele/data-nrykova/primary_tumor.txt", delimiter="\t", header=None) 
uids = [uid.replace(".methylation_array.sesame.level3betas.txt", "") for uid in df2[0]]
uids = [uid for uid in uids if uid != "dc504e99-f492-4b31-8e54-a47e42e611d3"]
df_out = df1.loc[:, ["#chrom", "pos", "probe"] + uids]
df_out.to_csv("/scratch2/emanuele/data-nrykova/first_six_cancer/chr_merged_onlytumor.txt", sep="\t", index=False)





