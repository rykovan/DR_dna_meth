# the best graphs
./pca.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --pc 2  --matrix mfile.txt > pca_latent.txt
./tsne.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --pc 20 --per 30  > tsne_latent.txt
./ae.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --indim2 256 > ae_latent.txt 

./plot_output_pca.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt pca_latent.txt --outfname pca_graph.png 
./plot_output_tsne.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt tsne_latent.txt --outfname tsne_graph.png 
./plot-output-ae.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt ae_latent.txt --outfname ae_graph.png 

# perplexity graphs
./tsne.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --pc 20 --per 2  > tsne_per2.txt
./tsne.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --pc 20 --per 5 > tsne_per5.txt
./tsne.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --pc 20 --per 30  > tsne_per30.txt
./tsne.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --pc 20 --per 50 > tsne_per50.txt
./tsne.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --pc 20 --per 100  > tsne_per100.txt

./plot_output_tsne.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt tsne_per2.txt --outfname tsne_graph_per2.png 
./plot_output_tsne.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt tsne_per5.txt --outfname tsne_graph_per5.png 
./plot_output_tsne.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt tsne_per30.txt --outfname tsne_graph_per30.png 
./plot_output_tsne.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt tsne_per50.txt --outfname tsne_graph_per50.png 
./plot_output_tsne.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt tsne_per100.txt --outfname tsne_graph_per100.png 

# ae graphs with different nn
./ae.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --indim2 32 > ae_latent32.txt 
./ae.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --indim2 64 > ae_latent64.txt 
./ae.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --indim2 128 > ae_latent128.txt 
./ae.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --indim2 256 > ae_latent256.txt 
./ae.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --indim2 512 > ae_latent512.txt 
./ae.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --indim2 1024 > ae_latent1024.txt 

./plot-output-ae.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt ae_latent32.txt --outfname ae_graph32.png 
./plot-output-ae.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt ae_latent64.txt --outfname ae_graph64.png 
./plot-output-ae.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt ae_latent128.txt --outfname ae_graph128.png 
./plot-output-ae.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt ae_latent256.txt --outfname ae_graph256.png 
./plot-output-ae.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt ae_latent512.txt --outfname ae_graph512.png 
./plot-output-ae.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt ae_latent1024.txt --outfname ae_graph1024.png 

# dendrogram 

./dendro.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt

# distances measurements
./dist-neig.py $1 $2

./in-out-dist.py pca_latent.txt /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt 100
./in-out-dist.py tsne_latent.txt /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt 100
./in-out-dist.py ae_latent.txt /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt 100

./cmp-dist.py /home/nrykova/masteruab/MethylationDNA/pca_latent.txt mfile.txt > dis_amb_lat_pca.txt
./cmp-dist.py /home/nrykova/masteruab/MethylationDNA/tsne_latent.txt mfile.txt > dis_amb_lat_tsne.txt
./cmp-dist.py /home/nrykova/masteruab/MethylationDNA/ae_latent.txt mfile.txt > dis_amb_lat_ae.txt

./stats-dist_spearman.py dis_amb_lat_pca.txt
./stats-dist_spearman.py dis_amb_lat_tsne.txt
./stats-dist_spearman.py dis_amb_lat_ae.txt

./amb_lat_plot.py dis_amb_lat_pca.txt 
./amb_lat_plot.py dis_amb_lat_tsne.txt 
./amb_lat_plot.py dis_amb_lat_ae.txt 

#eigenvalues and varplot
./pca.py /scratch2/emanuele/data-nrykova/first_six_cancer/chr14-merge-1350.txt --pc 12  --evalues evalues.txt
./eig_var.py --eigenplot eigenplot.png --varplot varplot.png

## only primary_tumor samples analysis filter 
./merge_clin_sample.py
./chr_merge_tumor.py 
#algorithms

./pca.py /home/nrykova/masteruab/MethylationDNA/chr_merged_onlytumor.txt --pc 2  --matrix mfile_tumor.txt > pca_latent_tumor.txt
./tsne.py /home/nrykova/masteruab/MethylationDNA/chr_merged_onlytumor.txt --pc 20 --per 30  > tsne_latent_tumor.txt
./ae.py /home/nrykova/masteruab/MethylationDNA/chr_merged_onlytumor.txt --indim2 256 > ae_latent_tumor.txt 

./plot_output_pca.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt pca_latent_tumor.txt --outfname pca_tumor_graph.png 
./plot_output_tsne.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt tsne_latent_tumor.txt --outfname tsne_tumor_graph.png 
./plot-output-ae.py /scratch2/emanuele/data-nrykova/filename-vs-caseid.txt ae_latent_tumor.txt --outfname ae_tumor_graph.png 




