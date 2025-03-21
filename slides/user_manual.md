## User manual of seismic_data_qi
This is the user manual for members of the **“Hazards and Surface Processes Research Group and the Digital Earth Lab”** to access seismic data on the GFZ Glic server.

**Author: Qi Zhou** <br>
**Maintenance: Qi Zhou**

## 1, Preparation
### 1.1, Glic Account
Please make sure you have the GLIC account, <br>
if not, please contact the GFZ IT to apply one.

### 1.2, Python Environment for Obspy
Please refer this link to deploy your own python environmet, <br>
[Click here to see how to install conda on Glic](https://git-int.gfz-potsdam.de/hpc/user-manual/-/wikis/env#conda), <br>

for example, <br>
I create a envs named as **seismic**, <br>
and install **Obspy** package.
```sh
conda create --name seismic
conda activate seismic
conda install conda-forge::obspy
```

Finally, please double check that your python environment **seismic** has successfully installed Obspy! <br>

### 1.3, R Environment for Eseis (Not recommended)
If you want to use [Eseis](https://www.gfz-potsdam.de/en/section/geomorphology/projects/eseis) to process seismic data,
you can create a R environmet named as **r-base**, <br>
```bash
conda activate
conda create --name r-env r-essentials r-base
conda activate --stack r-env
R --version
conda deactivate
```
Please be super careful when you install **Eseis**,
#### 1.3.1, prepare the package for r-env
Please note: #eseis# package is not available via conda <br>
open terminal and active the envs **r-env**, <br>
```sh
conda install -c conda-forge r-essentials # install the essentials package
```
then install **terra**, **fftw**, and other package.
```sh
conda install -c r r-terra # https://docs.anaconda.com/free/working-with-conda/reference/r-language-pkg-docs/
```

#### 1.3.2, install #eseis# package
Please make sure all the eseis required packaged, then install #eseis# package , <br>
type **R** in terminal to entre the R, <br>

```sh
install.packages("eseis", repos="https://cloud.r-project.org")
```
then type
```sh
q()
```

### 1.4, sbatch file for Python
Prepare a **run.sh** file with the following information, <br>
and make sure you have the [read_data_from_Glic.py](example/read_data_from_Glic.py)
```sh
#!/bin/bash
#SBATCH -t 4-00:00:00              # time limit: (D-HH:MM:SS) 
#SBATCH --job-name=example          # job name, "Qi_run"
#SBATCH --ntasks=1                 # each individual task in the job array will have a single task associated with it
#SBATCH --mem-per-cpu=8G		       # Memory Request (per CPU; can use on GLIC)

#SBATCH --chdir=/storage/vast-gfz-hpc-01/project/seismic_data_qi/#temp/ES-learning-materials # set working dir
#SBATCH --output=out_%A_%a_%x.txt  # Standard Output Log File
#SBATCH --error=err_%A_%a_%x.txt   # Standard Error Log File

source /your/path/to/output/miniforge3/bin/activate
conda activate seismic

srun python example/read_data_from_Glic.py

```

### 1.5, sbatch file for R (Not recommended)
Prepare a **example.sh** file with the following information, <br>
and make sure you have the test.R

```sh
#!/bin/bash
#SBATCH -t 4-00:00:00              # time limit: (D-HH:MM:SS) 
#SBATCH --job-name=Qi_run          # job name, "Qi_run"
#SBATCH --ntasks=1                 # each individual task in the job array will have a single task associated with it
#SBATCH --mem-per-cpu=8G		       # Memory Request (per CPU; can use on GLIC)

CONDA_BASE=$(conda info --base) 
source "${CONDA_BASE}/etc/profile.d/conda.sh"
conda activate 
conda activate --stack r-env

Rscript /your/python/file/path/test.R
```

## 2, Shared Group Folder
Path **/storage/vast-gfz-hpc-01/project/seismic_data_qi** <br>
please do NOT overwrite or delete any file.

## 3, Access Seismic Data
You can use this code to fetch and convert the seismic data to numpy,
```python
example/read_data_from_Glic.py
```

## 4, Download Data
If you do not want to work on Glic, <br>
you can download the seismic data to your local PC by [FileZilla](FileZilla/FileZilla.png), <br>
and run this code [read_data_from_Glic](../example/seismic_data_processing.py) in Pycharm or VS code

personally, I higly suggested to perform your work on Glic and liberate you PC.
