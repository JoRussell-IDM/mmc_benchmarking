Benchmarking documentation

___________________

EIR_vs_PfPR round 2
___________________


This exercise to plot model results for PfPR over a range of EIR settings with more detailed configuration specification (health seeking and seasonality) was preformed using executables built from EMOD version 2.15.0.0.

Simulation context details are provided in the accompanying simulation commissioning script (mmc_benchmarking\benchmarking_round_2\run_scenario_*.py)

Briefly, simulations were run for burn-in period of 50 years before reports were generated to calculate average PfPR in individuals aged 2-10 years old for each simulation. Each simulation is defined by an average annual EIR that is calculated from average of daily EIR values reported over the time interval (50th year). Seasonality was imposed by imposing constant climate but varying larval habitat with a scale factor as specified (factor = 1+sin(2*pi*t/365))  Simulations monitored 1000 individuals in a single node with disease mortality and vital dynamics (births and deaths). 

Output data and plots are contained in the adjacent directory (benchmarking_round_2\output) with separate directories for each experiment that contributed to this exercise  (directory name = IDM COMPS experiment id).

EMOD model parameters were fit using data as previously described in [1,2]. Data used in the calibration procedure included age-stratified prevalence data from Namawala, Tanzania and sites as measured in the Garki Project including Rafin Marke, Sugungum, and Matsari, Nigeria. In addition, parameters governing progression to symptomatic disease and were fit using age-stratified clinical incidence data from Ndiop and Dielmo, Senegal. 

References
1. https://malariajournal.biomedcentral.com/articles/10.1186/s12936-015-0751-y
2. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4326442/
 
________________________________________________________________________________
