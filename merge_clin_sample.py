#!/usr/bin/env python
import json


with open("/scratch2/emanuele/data-nrykova/metadata-tcga/clinical/clinical.tsv") as fclinical:
    clinical=fclinical.read().split("\n")
    
with open("/scratch2/emanuele/data-nrykova/metadata-tcga/biospecimen/sample.tsv") as fcsample:
    sample=fcsample.read().split("\n")    
    

tblclin = {}
for i in range(1, len(clinical)-1):
    fields=clinical[i].split("\t")
    tblclin[fields[0]]=[fields[e] for e in [109, 122, 118]]

tblsample = {}
for j in range(1, len(sample)-1):
    fields=sample[j].split("\t")
    tblsample[fields[1]]=[fields[e] for e in [27, 34]]      
    

with open("/scratch2/emanuele/data-nrykova/metadata-tcga/metadata.cart.2022-03-31.json") as f:
    tbl = json.load(f)

with open('primary_tumor.txt', 'w') as f:
    for i in range(len(tbl)):
        fn = tbl[i]['file_name']
        caseid=tbl[i]['associated_entities'][0]['case_id']
        mdata=tblclin[caseid]
        sample=tblsample[caseid]
        l = f"{fn}\t{caseid}\t{mdata[0]}\t{mdata[1]}\t{mdata[2]}\t{sample[0]}\t{sample[1]}"
        f.write(f"{l}\n")
    
    