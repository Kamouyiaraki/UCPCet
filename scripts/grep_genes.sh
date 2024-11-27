#!/bin/bash

dir="/home/mkamouyi/scratch/private/cetaceans/reference_gene_sequences/*.fa"
#mkdir alignment_files

for x in $dir
do	
    input1_name=$(basename "${x}")
    prefix="${input1_name%%.*}"
    
    # Find matching files using the full path and prefix
    matching_files=$(ls /home/mkamouyi/scratch/private/cetaceans/exonerate_out/"${prefix}"*_max.fas 2>/dev/null)
    
    if [ -n "$matching_files" ]; then
        grep -h "" $matching_files > "/home/mkamouyi/scratch/private/cetaceans/alignment_files/${prefix}.fas"
    else
        echo "No matching files found for ${input1_name}"
    fi
done
