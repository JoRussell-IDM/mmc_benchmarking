import os
import numpy as np
from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from dtk.generic.climate import set_climate_constant

from simtools.SetupParser import SetupParser
from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
from simtools.ModBuilder import  ModFn, ModBuilder

from malaria.reports.MalariaReport import add_patient_report, add_survey_report, add_summary_report

from dtk.interventions.input_EIR import add_InputEIR

# General
exp_name = 'mmc_benchmark_eir_vs_pfpr_annual'
years = 43 # length of simulation, in years

#Reading in from a config file specific for Malaria Functional Model which relies on 2.0 logic
config_path = os.path.join(os.path.expanduser('~'), 'Dropbox (IDM)',
                               'Malaria Team Folder', 'projects',
                               'updated_infection_and_immunity', 'malaria-two-pt-oh', 'bin', 'config.json')

# Setup ----------------------------------------------------------------------------------------------------------
# cb = DTKConfigBuilder.from_files(config_path)

cb = DTKConfigBuilder.from_defaults('MALARIA_SIM')

cb.update_params({'Vector_Species_Names' : [],
                  'Simulation_Duration' : 365*years,
                  'Enable_Vital_Dynamics' : 1,
                  'Enable_Disease_Mortality': 1,
                  "Base_Population_Scale_Factor": 1,
                  "Enable_Initial_Prevalence": 0,
                  'Demographics_Filenames' : ['Namawala_single_node_demographics.json']
                  })

set_climate_constant(cb)


def sweep_scale_factor(cb, scale_factor) :

    monthly_EIR = [43.8, 68.5, 27.4, 46.6, 49.4, 24.7, 13.7, 11, 11, 2.74, 13.7, 16.5]
    add_InputEIR(cb, [x*scale_factor for x in monthly_EIR])
    return { 'annual EIR' : scale_factor*sum(monthly_EIR)}

# builder = ModBuilder.from_list( [[ ModFn(sweep_scale_factor, x)] for x in [0.01,10,100]])
report_years = 1
report_start = 40
add_summary_report(cb,
                   start = 365*report_start,
                   description='Annual_Report',
                   interval = 365,
                   nreports = 1,
                   age_bins = [2, 10, 125],
                   parasitemia_bins = [0, 50, 200, 500, 2000000]
                   )

builder = ModBuilder.from_list( [[ ModFn(sweep_scale_factor, x)] for x in np.logspace(-3, 0, 200)])




# Run args
run_sim_args = {'config_builder': cb,
                'exp_name': exp_name,
                'exp_builder': builder
                }

if __name__ == "__main__":

    if not SetupParser.initialized:
        SetupParser.init('HPC')

    exp_manager = ExperimentManagerFactory.init()
    exp_manager.run_simulations(**run_sim_args)
    exp_manager.wait_for_finished(verbose=True)
    assert (exp_manager.succeeded())
