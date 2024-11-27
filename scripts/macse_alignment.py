import os
import sys
import subprocess
import logging
import pathlib
import re
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

# Ensure the logs directory exists
log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

# Set up logging to both stdout and a file
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Set to DEBUG for more detailed logs

# Configure logging handlers
if not logger.hasHandlers():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)

    file_handler = logging.FileHandler(os.path.join(log_dir, "check_assembly.log"))
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

# Function to get gene IDs from files
def get_ids(seq_dir):
    dir_path = pathlib.Path(seq_dir)
    if not dir_path.is_dir():
        logger.error(f"Directory {seq_dir} does not exist.")
        return set()

    logger.info(f"Scanning directory: {dir_path}")
    ids = {match.group(0) for file in dir_path.glob("*.fas")
           if (match := re.match(r'^\d+\.fas$', file.name))}
    if not ids:
        logger.warning("No IDs found.")
    else:
        logger.info(f"Found IDs: {', '.join(ids)}")
    
    return ids

# Function to run the alignment for a given gene file
def align_gene(id, seq_dir, macse_jar):
    gene_file = Path(f"{seq_dir}/{id}")
    output_file = Path(seq_dir) / f"{id}_NT.fas"

    # Check if aligned gene file already exists
    if output_file.is_file():
        logger.info(f"Output file already exists for {id}. Maybe it's already been aligned.")
    else:
        logger.info(f"Aligning {id} in MACSE...")
        command = ["java", "-jar", macse_jar, "-prog", "alignSequences","-seq", str(gene_file)]
        try:
            subprocess.run(command, check=True)
            logger.info(f"MACSE alignment completed for {id}")
        except subprocess.CalledProcessError as e:
            logger.error(f"MACSE alignment failed for {id}: {e}")

def main(seq_dir, macse_jar, max_workers=4):
    ids = get_ids(seq_dir)
    if not ids:
        logger.error("No IDs found. Exiting.")
        return

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(align_gene, id, seq_dir, macse_jar): id for id in ids}

        for future in as_completed(futures):
            id = futures[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"MACSE alignment failed for {id}: {e}")

if __name__ == "__main__":
    seq_dir = './test_dir/'
    MACSE_JAR = 'macse_v2.07.jar'  # Path to the MACSE jar file

    main(seq_dir, MACSE_JAR, max_workers=8)
