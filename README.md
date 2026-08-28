<p align="center">
<img src="https://anonymous.4open.science/r/biomQuants-EDEF/assets/biomQuants_Logo.png" width="300" alt="" height="300"/>
</p>

# $\texttt{biomQuants}$: A Systematic, Multifaceted, and Open-Source Framework for Biometric Quantification

<p align="center">
<a><img src="https://img.shields.io/badge/python-3.9+-blue"></a>
<a><img src="https://img.shields.io/badge/tensorflow-2.8+-orange"></a>
<a><img src="https://img.shields.io/badge/pytorch-2.2.0-purple"></a>
<a href="https://pypi.org/project/biomQuants/"><img src="https://img.shields.io/badge/PyPI-biomQuants-blue?" alt="github"></a>
<a href="https://anonymous.4open.science/r/MeasureSuite-822D/"><img src="https://img.shields.io/badge/Project-page-green" alt="github"></a>
</p>

## Abstract
Biometric quantification is used to assess and assign fitness scores to categories based on factors such as actions, sensors, and physiological conditions, enabling systematic discovery and evaluation of biometric characteristics. However, evaluating the quality of scores remains an open problem; error rate-based approaches require discretization over a fixed scale, while ranking- and correlation-based measures overlook relative score quality or trends. We present \texttt{biomQuant}, a multifaceted evaluation framework that jointly captures four complementary criteria. Besides ranking order, we reward high scores for high-ranked and low scores for low-ranked categories.
We also quantify correspondence between the trends of predicted and ground truth scores. Finally, we account for disentanglement between identity features of categories as a discounting factor.
These are combined using appropriate weights and result in the advanced acceptance score ($A_r^*$). 
Across $13$ biometric quantification scenarios spanning gesture, action, mobile activity, and sensor selection, $5$ biometric quantification frameworks, and $9$ state-of-the-art (SOTA) models, $A_r^*$ consistently favors scores that better satisfy the four criteria jointly. In intra-framework analysis, we show that $A_r^*$ prefers more holistic scores in $39$ out of $53$ scenarios, with $5$ additional near-optimal cases, and $17$ distinct selections from other measures. We also conduct extensive ablations to support the reliability, non-redundancy, stability, and sensitivity of the proposed measure. We release a Python package, biomQuants, comprising the proposed measure and other biometric quantification frameworks.

## News
* We have released our code, results, and made test-set embeddings public.

## Repository
> We release code, evaluation measures, testing and analysis code, and extracted embeddings for reproducibility.

> Environments/Dependencies
```
python == 3.9/3.10/3.11
TensorFlow == 2.8+
PyTorch == 2.2.0
scikit-image == 0.19.1
scikit-learn == 1.1.0
seaborn == 0.13.2
Levenshtein == 0.18.1
PyCompare
```

> The repository follows following structure:

```
.
├── main.py
├── correlation.py
├── utils 
    └── selector.py
    └── retList.py
    └── sensorSimulator.py
├──src
    └── quantifiers.py
    └── measures.py
    └── AcceptanceScore.py
    └── RankDeviation.py
    └── ICGDScore.py
    └── PatternMatchDistance.py
├──plot
    └── ... <Various plotting utilities>
├──misc
    └── ... <Some miscellaneous analysis scripts>
├──run
    └── ... <Bash scripts for experimentation>
├──quants
    └── ... <Training/testing recipes for PyTorch>
├──scutQuants
    └── ... <Training/testing recipes for Tensorflow>
├──_store
    └── ... <Various results and plots>
├──Embeddings
    └── ... <Embeddings and labels for reproducibility>
```

## How to use the repository

### Instructions
1. Clone the repo
2. Install the dependencies
3. This repository serves two purposes: (i) training quantification models, and (ii) analyzing quantification models.

### Training/Testing quantification models

For `Tensorflow`
- `cd ./scutQuants`
- `trainer.py` and `tester.py` have been provided, alter the data paths in them for your data
- Check for `./scutQuants/run/`: We have provided several bash files to run the scripts
- For example: 

```bash
==========  Training ========== 
python './trainer.py' --modelChoice mvit --lambda_id 0.5 --lambda_cgid 0.01 --local_batch_size 8 --exp_name "ms_mvit_pt5-pt01_scut"

==========  Testing ==========  
python './tester.py' --modelChoice mvit --lambda_id 0.5 --lambda_cgid 0.01 --local_batch_size 8 --exp_name "ms_mvit_pt5-pt01_scut"
```
- Following are the `flags`:
    *   `--modelChoice`: Choice of the model
    *   `--lambda_id`: Training weights for ID loss
    *   `--lambda_cgid`: Training weights for ICCD loss
    *   `--local_batch_size`: Batch used by a single GPU (we have distributed training)
    *   `--exp_name`: Name of the experiments, the dataFiles and embeddings will be stored via this name


For `PyTorch`
- `cd ./quants` (Adapted from the original [DGBQA](https://github.com/AmanVerma2307/DGBQA) repository)
- `trainer.py` and `tester.py` have been provided, alter the data paths in them for your data
- Check for `./quants/run/`: We have provided several bash files to run the scripts
- For example: 

```bash
==========  Training ========== 
python './trainer.py' --dataset ntu_120 --model hcn --num_epochs 100 --batch_size 128 --lambda_hgr 1.0 --lambda_id 0.5 --lambda_icgd 0.01 --lr 1e-3 --lrScheduler 1 --lrScheduler_mode multiStep --lrScheduler_stepGamma 0.1 --exp_name ms_hcn_1-pt5-pt01-multiStepmin3_ntu120

==========  Testing ==========  
python './tester.py' --dataset ntu_120 --model hcn --num_epochs 100 --batch_size 128 --lambda_hgr 1.0 --lambda_id 0.5 --lambda_icgd 0.01 --lr 1e-3 --lrScheduler 1 --lrScheduler_mode multiStep --lrScheduler_stepGamma 0.1 --exp_name ms_hcn_1-pt5-pt01-multiStepmin3_ntu120
```

### Analyzing quantification models

1. For analysis, you may use our open-source package `biomQuants` (https://pypi.org/project/biomQuants/)

2. With `main.py` you can conduct: (i) optimality analysis, and (ii) stability analysis. While with `correlation.py` you can conduct reliability analysis.

3. `./src` comprises `quantifiers.py`: file comprising multiple quantifiers, our measures, and `measure.py`: other existing measures.

4. `selector.py` comprises functions for

``` python
# Returns the value of a measure for a given emebdding
measures = get_val(embedding,
                    y_dev,
                    y_dev_id,
                    eer_values,
                    G_total,
                    I_total,
                    measure_req,
                    mode,
                    quantifier='dgbqa',
                    kappaVal=1,
                    lambdaVal=2,
                    nuVal=1,
                    betaVal=0.75,
                    normalize=1)
    # measure_req: The required evaluation measures
    # mode: If 'full' returns a list of values of several different measures
    # One can vary scaling factors as well


# Function to get measure value for the embedding list
measure_val = get_params(embedding_list,
                        dataset_list,
                        var,
                        quantifier='dgbqa',
                        kappaVal=1,
                        lambdaVal=2,
                        nuVal=1,
                        betaVal=0.75,
                        normalize=1):
    # dataset_list: The list containing names of the dataset corresponding to all the embeddings

# Function to get optimal model as per the 'var' metric
optModel = select_model(embedding_list,
                        dataset_list,
                        var,
                        quantifier,
                        kappaVal=1.0,
                        lambdaVal=2,
                        betaVal=0.75,
                        nuVal=1,
                        normalize=1
                        ):
```

5. Sample run and flags for `main.py`

```bash
# Optimality analysis
python './main.py' --mode 'comparison' --dataset '<>' --metric '<>' --quantifietr '<>' --initResultFile 1 --nameResultFile '<>' --betaVal --lambdaVal --kappaVal --nuVal

# Stability analsysis
python './main.py' --mode 'stability' --dataset '<>' --metric '<>' --quantifietr '<>' --initResultFile 1 --nameResultFile '<>' --betaVal --lambdaVal --kappaVal --nuVal
```

6. Sample run and flags for `correlation.py`
```bash
python './correlation.py' --dataset --quantifier  --measure1 --measure2  --corrPath '<Path to save Correlation plot>' --baPath '<Path to save Bland-Altman plot>' --nameCorrFile '<Path to store results of reliability analysis>' --initCorrFile 1
```

7. You can reproduce results using `bash` scripts in `run/`