A directory for exploring and comparing the model behavior of DTK through development
Date: 05/02/2020
Author: Jon Russell

Directory structure:
./analyzers
./commissioners
./executables
./reporter_plugins

-----ANALYZERS-----
A directory containing analyzers for comparing fundemanteal modeled quantities and relationships deemed important to capturing malaria epidemiology in any setting. Analyzers should be named with the convention {QUANTITY1}_{QUANTITY2}_Analyzer.py These include:

Quantities:

Parasite Prevalence (PfPR)
Entomological Inoculation Rate (EIR)
Clinical Incidence (Incidence)
Age
Complexity of Infection (CoI)

Relationships:

PfPR vs. EIR
Incidence vs PfPR 
Incidence vs Age (by EIR)
CoI vs Age (by EIR)
CoI vs EIR


-----COMMISSIONERS-----
A directory if directories used to configure and run DTK simulations. Each commissioners directory should be named with convention {EXPERIMENT DESCRIPTION} and should contain:

-run_sims.py: file that configures model and campaign parameters and uses ModFn to build experiments (parameter sweeps).

-inputs: directory containing
	-config.json
	-campaign.json
	-*demographics.json
	-*climate_files.json
-outputs: a directory for any plots or output files to be saved from analyzers on commissioned sims

-simtools.ini: a text file pointing that configures job submission (HPC/Local) as well as paths to exe version (in ./executables) as well as local inputs and dlls (if applicable, *dlls (reporter_plugins) are no longer required with DTK exe)

-----EXECUTABLES-----
A directory containing exe versions to be named with the convention of Eradication_{DATE}_{DESCRIPTION}.exe
The path to the appropriate exe should be specified in the ./commissioners/*/simtools.ini file under exe_path

See ./executables/exe_README.txt for a running list of exe versions and descriptors
fields:
exe name	/	date	/	description
	
-----REPORTER PLUGINS-----
A directory containing reporter_plugins folders for use when comparing any older DTK version that requires reporter_plugins directories associated with that build of the DTK, path to be specified in the ./commissioners/*/simtools.ini file under dll_root
*current DTK versions do not require dlls