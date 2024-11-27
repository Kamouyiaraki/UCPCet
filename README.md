# UCPCet

## Scripts in order of use:

### Python >= 3.9 set up
```
python3.9 -m pip install progress
python3.9 -m pip install bs4
python3.9 -m pip install lxml
```

### 1. Download genomes

Done using [`download_genomes.sh`](https://github.com/Kamouyiaraki/UCPCet/blob/main/scripts/download_genomes.sh) with [`genome_links.txt`] (https://github.com/Kamouyiaraki/UCPCet/blob/main/downloads/genomes_links.txt) as input.

Unzip all genomes for use
```
gunzip *.gz
```

### 2. Download reference genes using gene list generated from KEGG pathway

Done using [`get_pathway_genes.py`](https://github.com/Kamouyiaraki/UCPCet/blob/main/scripts/get_pathway_genes.py) with [`thermogenesis_kegg_hsa_genecodes.tsv`](https://github.com/Kamouyiaraki/UCPCet/blob/main/downloads/thermogenesis_kegg_hsa_genecodes.tsv)

*Note:* 
*The structure to define whether retrieving nt sequences or aa is:* 
```
-f -n a hsa:<geneID> #for AA seq
-f -n n hsa:<geneID> #for nt seq
```

 
### 3. Exonerate reference genes for each genome

Run exonerate for all genes (240) for all genomes (72) using [`exonerate_parallel.py`](https://github.com/Kamouyiaraki/UCPCet/blob/main/scripts/exonerate_parallel.py)

### 4. Prepare exonerate output for next steps
- Turn output into FASTA format [`exonerate2fasta.sh`](https://github.com/Kamouyiaraki/UCPCet/blob/main/scripts/exonerate2fasta.sh)
- filter to keep top hit [`max_list.sh`](https://github.com/Kamouyiaraki/UCPCet/blob/main/scripts/max_list.sh) 
- merge hits to output a single FASTA per gene for downstream alignment [`grep_genes.sh`](https://github.com/Kamouyiaraki/UCPCet/blob/main/scripts/grep_genes.sh)

### 5. Align gene files using MACSE v2.07

- The [latest release of MACSE](https://www.agap-ge2pop.org/macsee-pipelines/) was downloaded directly into the working directory:

```
wget https://www.agap-ge2pop.org/wp-content/uploads/macse/releases/macse_v2.07.jar
```

- [`macse_alignment.py`](https://github.com/Kamouyiaraki/UCPCet/blob/main/scripts/macse_alignment.py) was run on all gene files, where the input required is the directory where all the sequence files are kept (`seq_dir`) and the location of the MACSE `.jar` file. 
