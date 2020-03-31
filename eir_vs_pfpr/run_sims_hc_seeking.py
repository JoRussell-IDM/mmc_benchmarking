import os
import numpy as np
from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from dtk.generic.climate import set_climate_constant
from malaria.interventions.malaria_diagnostic import add_diagnostic_survey
from simtools.SetupParser import SetupParser
from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
from simtools.ModBuilder import  ModFn, ModBuilder

from malaria.reports.MalariaReport import add_patient_report, add_survey_report, add_summary_report
from malaria.interventions.malaria_drug_campaigns import add_drug_campaign
import copy
import pandas as pd
from datetime import date
from malaria.interventions.health_seeking import add_health_seeking
from dtk.interventions.outbreakindividual import recurring_outbreak
from dtk.vector.species import update_species_param
from dtk.vector.species import set_larval_habitat
from simtools.Utilities.Experiments import retrieve_experiment
from simtools.Utilities.COMPSUtilities import COMPS_login
from dtk.interventions.itn_age_season import add_ITN_age_season
from dtk.interventions.biting_risk import change_biting_risk
from dtk.interventions.irs import add_IRS
from malaria.reports.MalariaReport import add_event_counter_report
from malaria.interventions.malaria_drug_campaigns import add_drug_campaign
from dtk.interventions.input_EIR import add_InputEIR

# General
exp_name = 'healthcare_seeking_moz_eir_sweep'
years = 41 # length of simulation, in years

#Reading in from a config file specific for Malaria Functional Model which relies on 2.0 logic
config_path = os.path.join(os.path.expanduser('~'), 'Dropbox (IDM)',
                               'Malaria Team Folder', 'projects',
                               'updated_infection_and_immunity', 'malaria-two-pt-oh', 'bin', 'config.json')


# Setup ----------------------------------------------------------------------------------------------------------
# cb = DTKConfigBuilder.from_files(config_path)

cb = DTKConfigBuilder.from_defaults('MALARIA_SIM')

cb.update_params({'Vector_Species_Names' : [],
                  'Simulation_Duration' : (365*years)+1,
                  'Enable_Vital_Dynamics' : 1,
                  'Enable_Disease_Mortality': 1,
                  "Base_Population_Scale_Factor": 1,
                  "Enable_Initial_Prevalence": 0,
                  'Demographics_Filenames' : ['Namawala_single_node_demographics.json']
                  })

set_climate_constant(cb)

def sweep_coverages(cb,coverage):
    add_health_seeking(cb, start_day = 0,
    drug = ['Artemether', 'Lumefantrine'],
    targets = [
        {'trigger': 'NewClinicalCase', 'coverage': coverage[0], 'agemin': 0, 'agemax': 5, 'seek': 1,
         'rate': 0.3},
        {'trigger': 'NewClinicalCase', 'coverage': coverage[1], 'agemin': 10, 'agemax': 200,
         'seek': 1,
         'rate': 0.3},
        {'trigger': 'NewSevereCase', 'coverage': 0.95, 'agemin': 0, 'agemax': 200, 'seek': 1,
         'rate': 0.3}]

    ),
    return {'coverage_pair': coverage}
def sweep_scale_factor(cb, scale_factor) :

    monthly_EIR = [43.8, 68.5, 27.4, 46.6, 49.4, 24.7, 13.7, 11, 11, 2.74, 13.7, 16.5]
    add_InputEIR(cb, [x*scale_factor for x in monthly_EIR])
    return { 'annual EIR' : scale_factor*sum(monthly_EIR)}

# builder = ModBuilder.from_list( [[ ModFn(sweep_scale_factor, x)] for x in [0.01,10,100]])
report_years = 1
report_start = 40
survey_days = list(range(365 * report_start, (365 * (report_start + 1)), 30))

# add_survey_report(cb, survey_days, reporting_interval=1)
add_summary_report(cb,
                   start = 365*report_start,
                   description='Annual_Report',
                   interval = 365,
                   nreports = 1,
                   age_bins = [5,125],
                   parasitemia_bins = [0, 50, 200, 500, 2000000]
                   )


healthseeking_coverage_pairs = [[0.85,0.65],[0.7,0.5],[0.5,0.3]] # as U5 and then >5 year olds

# creates a sweep of simulations with varying coverages and Run_Number seeds
healthseeking = [
            [

               ModFn(sweep_coverages, coverages),

               ModFn(sweep_scale_factor, x)

            ]
            for x in np.logspace(-3, -1, 50)
            for coverages in healthseeking_coverage_pairs
        ]

builder = ModBuilder.from_list(healthseeking)


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
