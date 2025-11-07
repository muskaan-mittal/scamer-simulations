# Estimating misreporting in the presence of genuine modification: a causal perspective

## Simulations overview
The code to replicate all of the of the semi-synthetic loan fraud experiments be found in the following Jupyter notebook files.
- synthetic_simulations_1.ipynb: Generated Figure 2 (main text), Figure 3 (Appendix)
- synthetic_simulations_2.ipynb: Generated Figure 4 (Appendix)
- synthetic_simulations_3.ipynb: Generated Figure 5 (Appendix)
- synthetic_simulations_4.ipynb: Generated Figure 6 (Appendix)
- synthetic_simulations_5.ipynb: Generated Figure 7 (Appendix)

## How to run each simulation
Before running the experiments in each Jupyter notebook, the variable "RESULTS_DIR" must be set. This variable is used to indicate where the generated plots will be saved and where several pickled pandas dataframes from the simulations will be stored. These dataframes store the estimated misreporting rates from each model over every simulation.

## Other files
The following is a short description of each of the other files required to run the code
- models.py: contains the code for CMRE and all baselines
- plots.py: contains the code to create all of the plots for the semi-synthetic loan fraud experiments
- datasets/default_of_credit_card_clients.xls: the real credit card dataset, which is used to generate the semi-synthetic loan fraud dataset
