# mmc_benchmarking

Benchmarking documentation

___________________

EIR_vs_PfPR
___________________


This exercise to plot model results for PfPR over a range of EIR settings was preformed using executables built from EMOD version 2.15.0.0.

Simulation context details are provided in the accompanying simulation commissioning script (mmc_benchmarking\eir_vs_pfpr\run_sims.py)

Briefly, simulations were run for burn-in period of 40 years before reports were generated to calculate average PfPR in individuals aged 2-10 years old for each simulation. Each simulation is defined by an average annaul EIR that is calculated from average of a scaled monthly EIR spline used to define seasonal malaria transmission. Simulations monitored 1000 individuals in a single node with disease mortality and vital dynamics (births and deaths). 

EMOD model parameters were fit using data as previously described in [1,2]. Data used in the calibration procedure included age-stratified prevalence data from Namawala, Tanzania and sites as measured in the Garki Project including Rafin Marke, Sugungum, and Matsari, Nigeria. In addition, parameters governing progression to symptomatic disease and were fit using age-stratified clinical incidence data from Ndiop and Dielmo, Senegal. 

References
1. https://malariajournal.biomedcentral.com/articles/10.1186/s12936-015-0751-y
2. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4326442/
 
________________________________________________________________________________
