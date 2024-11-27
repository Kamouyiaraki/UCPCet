#!/bin/bash

dir="/home/mkamouyi/scratch/private/cetaceans/exonerate_out/*.fas"

for x in $dir
do
    # Extract the full sampleID from the file name
    sampleID=$(basename "$x" | sed -n 's/^[^_]*_\([^\.]*\)\.fas$/\1/p')

    # Find the maximum value from the 5th column
    grep "^>" "$x" | awk '{ print($5) }' | sort -n | tail -1 > max.out

    # Extract the headers with the maximum value
    grep -w -P -f max.out "$x" > list_of_headers.txt

    # Reformat the FASTA file
    awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);}  END {printf("\n");}' "$x" | tail -n +2 > "${x%.*}_SL.fas"

    # Extract sequences with the matching headers
    grep -A1 -f list_of_headers.txt "${x%.*}_SL.fas" > "${x%.*}_max.fas"

    # Add the sampleID to each sequence header in the final output
    sed -i "s/^>/&${sampleID}_/" "${x%.*}_max.fas"

    # Clean up intermediate files
    #rm "$x"
done

mkdir cleaned_exonerate_out
mv exonerate_out/max.out ./cleaned_exonerate_out/
mv exonerate_out/list_of_headers.txt ./cleaned_exonerate_out/
mv exonerate_out/*_SL.fas ./cleaned_exonerate_out/
mv exonerate_out/*_max.fas ./cleaned_exonerate_out/
