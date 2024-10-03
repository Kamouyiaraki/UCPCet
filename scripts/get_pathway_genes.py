import csv
import urllib.request
from bs4 import BeautifulSoup as bs
from progress.bar import Bar
import os
import re

# Function to get FASTA sequences for a given gene ID
def get_fasta(gene_id):
    URL = 'http://www.genome.jp'
    FUN = '/entry/-f+-n+a+hsa:'
    response = urllib.request.urlopen(URL + FUN + gene_id)
    html = bs(response.read(), features="lxml")
    return html.pre.text

# Function to read gene IDs from a specific column in a TSV file
def read_gene_ids_from_tsv(tsv_file, column_index=0, skip_header=True):
    gene_ids = []
    with open(tsv_file, newline='') as file:
        reader = csv.reader(file, delimiter='\t')  # Read tab-separated file
        if skip_header:
            next(reader)  # Skip the header row
        for row in reader:
            if len(row) > column_index:  # Ensure the column exists in this row
                gene_ids.append(row[column_index])  # Extract gene ID from the specified column
    return gene_ids

def sanitize_filename(filename):
    """Remove or replace any invalid characters from the filename."""
    # Replace whitespace with underscores and remove any non-alphanumeric characters
    return re.sub(r'\W+', '', filename)


# Main function to process gene IDs from a TSV file and write to separate files
def process_genes_from_tsv(tsv_file, column_index, output_dir):
    gene_ids = read_gene_ids_from_tsv(tsv_file, column_index)
    
    if not gene_ids:
        print(f"No gene IDs found in column {column_index} of {tsv_file}. Exiting.")
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Found {len(gene_ids)} gene IDs in column {column_index}. Fetching FASTA sequences...")

    # Set up progress bar
    bar = Bar('Downloading', max=len(gene_ids))
    
    # Fetch and save sequences in separate files for each gene ID
    for gene_id in gene_ids:
        fasta = get_fasta(gene_id)

        # Sanitize the gene_id to ensure no whitespaces or invalid characters in the filename
        sanitized_gene_id = sanitize_filename(gene_id)

        output_file = os.path.join(output_dir, f"{sanitized_gene_id}.fa")  # Create a separate file for each gene
        with open(output_file, 'w') as out:
            out.write(fasta)

        bar.next()

    bar.finish()
    print(f"FASTA sequences written to individual files in {output_dir}")

if __name__ == "__main__":
    # Example usage
    tsv_file = "thermogenesis_kegg_hsa_genecodes.tsv"  # Path to your TSV file
    column_index = 0  # Specify which column contains the gene IDs (0-based index)
    output_dir = "reference_gene_sequences"  # Directory to store output FASTA files

    process_genes_from_tsv(tsv_file, column_index, output_dir)

