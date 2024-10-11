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

Run exonerate for all genes x all genomes using [`exonerate_parallel.py`](https://github.com/Kamouyiaraki/UCPCet/blob/main/scripts/exonerate_parallel.py)

### 4. Prepare exonerate output for next steps
- Turn output into FASTA format [`exonerate2fasta.sh`](https://github.com/Kamouyiaraki/UCPCet/blob/main/scripts/exonerate2fasta.sh)
- filter to keep top hit [`max_list.sh`](https://github.com/Kamouyiaraki/UCPCet/blob/main/scripts/max_list.sh) 
- merge hits to output a single FASTA per gene for downstream alignment [`grep_genes.sh`]()

### 5. Align genes using MACSE
`initial_alignment.sh`
