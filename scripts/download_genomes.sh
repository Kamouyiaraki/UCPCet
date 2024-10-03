#!/bin/bash



# File containing URLs to genomes (one per line)
FILE="links_to_download.txt"

# Directory to save downloaded genomes
OUTDIR="genomes"
mkdir -p $OUTDIR

# Loop through each URL in the file and download the genome
while read -r URL; do
    echo "Downloading $URL..."
    wget -P $OUTDIR "$URL"
done < $FILE

echo "Download complete!"
