# Estimating misreporting in the presence of genuine modification: a causal perspective
# Part 1. No Data-Stitching (simulations written by Dylan)

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

## Results directories
Results for synthetic simulations 1-5 are in synthetic_sim_results

# Part 2. Data-Stitching (simulations written by Muskaan)
## Simulations overview
- synthetic_simulations_[6, 7, 8].ipynb: Various data-stitching simulations; imulation scenarios are noted in a comment at the top of each .ipynb file. These use the model cmre_ds from models_ds.py (sim7 also uses cmre_ds_adjusted_for_U)
- sensitivity_analysis_simulation.ipynb: In case we have 2 HCC's X\*1 and X\*2 that both affect the same anchor variable Y, we perform sensitivity analysis to compare 1) ground truth upcoding rate of HCC X\*1; 2) estimated upcoding rate of HCC X\*1 obtained by data-stitched cmre completely ignoring that HCC X\*2 also affects the same anchor variable Y; 3) estimated upcoding rate of HCC X\*1 obtained by data-stitched cmre by adjusting for X2 (but not X\*2, which is the true (but unobservable) value we want to control for). The first two cases use cmre_ds from models_ds.py while third case uses cmre_ds_adjusted_for_z from models_ds.py.
- sensitivity_analysis_randomized_graph.ipynb: \[work-in-progress\] Code to generate a graph containing n HCCs and 1 anchor variable, randomly sampling the causal effect of HCC X\*1, 2, ... on Y from a discrete distribution. Can then verify sensitivity analysis results from the above simulation with this randomized graph.

## Results directories
- Results for synthetic_sims_\[6-8] are currently not in this repo but can be reproduced using the code
- Results for sensitivity_analysis_simulation.ipynb are in sensitivity_analysis_results_1 (while sensitivity_analysis_results contains results from a very similar sensitivity analysis simulation but that used different constants in the causal graph).
- Results for sensitivity_analysis_randomized_graph.ipynb will go in synthetic_sim_randomized_graph_results once done