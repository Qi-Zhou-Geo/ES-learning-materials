#!/bin/bash
#SBATCH -t 4-00:00:00              # time limit: (D-HH:MM:SS) 
#SBATCH --job-name=example         # job name, "Qi_run"
#SBATCH --ntasks=1                 # each individual task in the job array will have a single task associated with it
#SBATCH --mem-per-cpu=8G		       # Memory Request (per CPU; can use on GLIC)

#SBATCH --output=/storage/vast-gfz-hpc-01/project/seismic_data_qi/#temp/ES-learning-materials/out_%A_%a_%x.txt  # Standard Output Log File
#SBATCH --error=/storage/vast-gfz-hpc-01/project/seismic_data_qi/#temp/ES-learning-materials/err_%A_%a_%x.txt   # Standard Error Log File

source /your/path/to/output/miniforge3/bin/activate
conda activate seismic

srun python example/read_data_from_Glic.py
