import os
import glob
import subprocess
from concurrent.futures import ProcessPoolExecutor

# Directories and paths
dir_path = "/home/mkamouyi/scratch/private/cetaceans/reference_gene_sequences/*.fa"
genomes_path = "/home/mkamouyi/scratch/private/cetaceans/genomes/*.f*a"
output_dir = "exonerate_out"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get all the input files
reference_files = glob.glob(dir_path)
genome_files = glob.glob(genomes_path)

# Function to run exonerate command
def run_exonerate(reference_file, genome_file):
    input1_name = os.path.basename(reference_file)
    input2_name = os.path.basename(genome_file)

    output_file = f"{output_dir}/{input1_name.split('.')[0]}_{input2_name.split('.')[0]}.out"
    cmd = [
        "exonerate",
        "--model", "protein2genome",
        reference_file, genome_file,
        "--ryo", ">{}%s\n%tas\n".format("ti (tab - tae) "),
        "--bestn", "1"
    ]
    
    print(f"Running exonerate for {input1_name} in {input2_name}...")
    with open(output_file, "w") as outfile:
        subprocess.run(cmd, stdout=outfile)

# Function to handle the parallel execution with max_workers option
def parallel_exonerate(max_workers=None):
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for ref_file in reference_files:
            for genome_file in genome_files:
                executor.submit(run_exonerate, ref_file, genome_file)

if __name__ == "__main__":
    # Set max_workers to control the number of parallel processes
    max_workers = 4  # You can change this value as needed
    parallel_exonerate(max_workers=max_workers)
    print("Exonerate runs complete!")
