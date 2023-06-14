
# HORNET

HORNET: Holistic RNA Structure Determination by Unsupervised Learning and Deep Neural Networks. HORNET is a software package for determining 3D topological structures of RNA conformers using atomic force microscopy topographic images and deep learning. Overall, the computation using HORNET consists of 4 steps:

1 - Running a Dynamic Fitting calculation based on AFM topography biasing potential

2 - Transforming the output of the dynamic fitting into inputs for UML/DNN analysis

3 - Unsupervised Learning Cohort Selection

4 - Supervised Neural Network RMSD Prediction

## Step 1 - Dynamic Fitting

See [here](https://github.com/PNAI-CSB-NCI-NIH/HORNET/tree/main/DynamicFitting/README.md) for a more detailed explanation of how to perform the Dynamic Fitting calculations.

## Steps 2-4

For the input preparation and unsupervised and supervised learning analyses, one should proceed with the following installations (typical installation time < 30 min):

### Installation

To install the necessary packages, one just need to create a conda environment, by first installing conda:
- [Linux](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html)
- [Mac](https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html)

After the installation, create a [conda environment](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) using:

```bash
conda create -n hornet python=3.7
```

You now can enter the environment by running:

```bash
conda activate hornet
```

And install the requirements:

```bash
pip install -r requirements.txt
```

The final step is to install [Tensorflow](https://www.tensorflow.org/install/pip#linux) 2.11. Please, check Tensorflow's page for help but it should be something as:

```bash
conda install -c conda-forge cudatoolkit=11.2.2 cudnn=8.1.0
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/
python3 -m pip install tensorflow==2.11.0
```
If you have trouble installing tensorflow, please check the [Tensorflow Documentation](https://www.tensorflow.org/install/pip#linux).

### Usage

Remember that the hornet environment should be activated for using the following scripts:
```bash
conda activate hornet
```

#### Step 2 - Input Preparation

The scripts for preparing the input data for both UML and DNN are located in [UML](https://github.com/PNAI-CSB-NCI-NIH/HORNET/tree/main/UML) folder. The first step is copying the output files (.ts) from the Dynamic Fitting folder into the UML/data/ folder as a txt file in which the name carries the kappa (the weighting factor for the AFM pseudo-potential) value:

```bash
cp <Dynamic-Fitting-Output>/<kappa>/<file-name.ts> <HORNET-PATH>/UML/data/en_allk<kappa>.txt
```

The kappa values used for AFM in the calculation are embedded in the name of the file and they will be extracted when loading the files.

The next step is to run the [input_prep.py](https://github.com/PNAI-CSB-NCI-NIH/HORNET/tree/main/UML/input_prep.py) script, which collects all of en_allk* files, transform and merge them, followed by saving them in an output file called "Full_Trajectory.csv". The numbers of base-pairs and base-stacking per trajectory are required for normalizations with a specific kappa value. This information can be taken into the script by simply creating a 3 column comma separated file (frame, base_pair, base_stack) per trajectory (see an example [here](https://github.com/PNAI-CSB-NCI-NIH/HORNET/tree/main/)). The name of this file should be `bases_k<kappa>.txt` and be placed in the same directory as the copied `en_allk<kappa>.txt` files are, where `<kappa>` in all examples should be replaced by the kappa values used in the calculation, eg., bases_k2.txt and en_allk2.txt if the kappa value was 2. 

For the best normalization and prediction, one should use the number of base-pair and base-stacking of the specific frame, or at least a smoothed value for each ~50 sequential frames. However, it is possible for the user to estimate an average value for all of the trajectories and pass this as a single constant value argument, at the cost of reducing accuracy in the RMSD predictions using DNN.

First, cd into the UML directory:

```bash
cd UML
```

And then run:

```bash
python input_prep.py <input-directory> [<base-pairs>] [<base-stacking>]
```

Where:
- input-directory: is the location where all the en_allk*.txt files are located, and the bases_k*.txt (if bases_k* exists)
- base_pairs: in case the user does not have a file with all the base_pairs per frame, they can pass an average value here
- base-stacking: in case the user does not have a file with all the base_stacking per frame, they can pass an average value here

Hence, once the file with base-pairing and base-stacking is ready and is located within the data directory, along with the en_allk* files, one should use:

```bash
python input_prep.py data
```

If the user wants to try with constant values for base-pairs and stackings, say the average values of base-pairing is 80 and base-stacking is 120, type:

```bash
python input_prep.py data 80 120
```

The output file "Full_Trajectory.csv" will be created within the `<input-directory>`. The Full_Trajectory.csv contains the collection of all calculated structures with topography and energy information.

Typical running time in a normal computer ~ 5 min for a dataset with 20M entries.

#### Step 3 - Unsupervised Learning Cohort Selection

To select top cohort structures using unsupervised learning, one just needs to run the [uml.py](https://github.com/PNAI-CSB-NCI-NIH/HORNET/tree/main/UML/uml.py) script, by using:

```bash
python uml.py <input-directory>/<Full-Trajectory-File>
```

Which in this example is:

```bash
python uml.py data/Full_Trajectory.csv
```

The output files from this script will be, within the data folder:
- 'Filtered_Data.csv': The first step of the UML analysis (Energy Filtering)
- 'Select_Cluster.csv': The second step of the UML analysis (PCA+Clustering)
- 'Final_Cohort.csv': The third step of the UML analysis (Cohort Selection)

Typical running time in a normal computer ~ 5 min for a dataset with 20M entries.

#### Step 4 - Deep Learning Predictions

The scripts for training models and performing predictions are located at [DNN](https://github.com/PNAI-CSB-NCI-NIH/HORNET/tree/main/DNN) folder. 

##### Predictions

To predict the RMSD (score) of structures, either from a Full_Trajectory, Filtered_Data, Select_Cluster or Final_Cohort, one needs to run the [predict.py](https://github.com/PNAI-CSB-NCI-NIH/HORNET/tree/main/DNN/predict.py) script:

```bash
python predict.py -o <output-directory> -d <dataset> -n <number-of-residues>
                  -m <model-location> [-k <kappa-cut>] [-f <frame-cut>] [-h]
```

Required arguments:

- output-directory: the directory where the output of the prediction will be stored
- dataset: the data to be used in predictions, such as 'Full_Trajectory.csv', 'Filtered_Data.csv', 'Select_Cluster.csv' or 'Final_Cohort.csv'
- number-of-residues: Number of residues of the RNA
- model-location: location where the trained model is stored

Optional arguments:

- kappa-cut: Maximum accepted kappa (for HORNET 1.0 it is 50)
- frame-cut: Minimum accepted frame (default is 2000, but this is trajectory dependent)
- help: Display the usage of the script

Example: to predict the Final_Cohort file and save the output in the prediction_test folder, using the HORNET trained model, where the number of residues is, for example, 268, one should use:

```bash
python predict.py -o prediction_test -d <path-to-file>/Final_Cohort.csv -m models/hornet -n 268
```

The output prediction file is saved under the output directory with the name of the dataset plus a prediction suffix, eg., Final_Cohort_prediction.csv.
IMPORTANT: All example datasets built within DNN/data have 268 ncl, so when using those datasets 268 is the number that should be used.

Typical running time in a normal computer ~ 1 min for a dataset with 1M entries.

##### Training

If one wants to train a model with other data, one just needs to run the [train.py](https://github.com/PNAI-CSB-NCI-NIH/HORNET/tree/main/DNN/train.py) script, as:

```bash
python train.py -o <output-directory> -d <dataset> -n <number-of-residues>
                [-e <epochs>] [-k <kappa-cut>] [-f <frame-cut>]
                [-v <validation>] [-vn <validation-residues>]
                [-l <loss-function>] [-s <seed>] [-h]
```

Required arguments:
- output-directory: output directory for the trained model
- dataset: Array of datasets to be used in training, separated by commas
  Example: "data/train_sample1.csv,data/train_sample2.csv"
- number-of-residues: Array of the number of residues related to the RNA datasets
  Example: considering the example above, if train_sample1 has 200 residues and train_sample2 has 500 onde should use 200,500.
IMPORTANT: All datasets within DNN/data have 268 ncl, this is what should be used.

Optional arguments:
- validation: dataset to be used as validation if any
  Example: "data/train_sample2.csv"
- validation-residues: Number of residues related to the validation data
- epochs: number of epochs to train the model
- kappa-cut: Maximum accepted kappa (For HORNET 1.0 it is 50)
- frame-cut: Minimum accepted frame (Default is 2000, but this is trajectory dependent)
- loss-function: Loss function to be used to train the model. Accepts: 'huber' or 'mse'
- seed: Seed to maintain reproducible results across testing, use 0 for random
- help: Displays usage and help information for running the script

Example: to create a model based on the dataset "data/train_sample1.csv" using dataset "data/train_sample2.csv" as validation, using an output folder called "train_test", for 5 epochs using huber loss, one should call:

```bash
python train.py -o train_test -d data/train_sample1.csv -n 268 \
                -v data/train_sample2.csv -vn 268 -e 5 -l huber
```

Typical running time in a normal computer is ~ 2 min per epoch for a dataset with 1M entries.
