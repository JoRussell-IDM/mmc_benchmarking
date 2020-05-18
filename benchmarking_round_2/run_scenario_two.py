import os
import numpy as np
from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from dtk.generic.climate import set_climate_constant
from malaria.interventions.malaria_diagnostic import add_diagnostic_survey
from simtools.SetupParser import SetupParser
from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
from simtools.ModBuilder import  ModFn, ModBuilder
import math

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
exp_name = 'scenario_2_eir_sweep_seasonal_lower_habitat_bound'
years = 51 # length of simulation, in years
num_seeds = 5
vector_habitat_days = list(np.arange(365))
vector_habitat_values = [1+(math.sin(2*math.pi*x/365)) for x in vector_habitat_days]

# Setup ----------------------------------------------------------------------------------------------------------

cb = DTKConfigBuilder.from_defaults('MALARIA_SIM')

cb.update_params({
                  "logLevel_default": "ERROR",
                  'Simulation_Duration' : (365*years),
                  'Enable_Vital_Dynamics' : 1,
                  'Enable_Disease_Mortality': 1,
                  'x_Base_Population':1,
                  'Enable_Initial_Prevalence': 1,
                  'Demographics_Filenames' : ['Namawala_single_node_demographics_balanced_pop_growth.json'],
                  'Incubation_Period_Distribution': "CONSTANT_DISTRIBUTION",
                  'Vector_Species_Names': ["SillySkeeter"],
                  'Vector_Sampling_Type': "VECTOR_COMPARTMENTS_NUMBER",
                  'Vector_Species_Params': [
                        {
                            "Name": "SillySkeeter",
                            "Acquire_Modifier": 1,
                            "Adult_Life_Expectancy": 20,
                            "Male_Life_Expectancy": 10,
                            "Anthropophily": 0.95,
                            "Aquatic_Arrhenius_1": 84200000000,
                            "Aquatic_Arrhenius_2": 8328,
                            "Aquatic_Mortality_Rate": 0.1,
                            "Days_Between_Feeds": 3,
                            "Egg_Batch_Size": 100,
                            "Immature_Duration": 2,
                            "Indoor_Feeding_Fraction": 1.0,
                            "Infected_Arrhenius_1": 117000000000,
                            "Infected_Arrhenius_2": 8336,
                            "Infected_Egg_Batch_Factor": 0.8,
                            "Infectious_Human_Feed_Mortality_Factor": 1.5,
                            "Larval_Habitat_Types": {
                                "LINEAR_SPLINE": {
                                    "Capacity_Distribution_Number_Of_Years": 1,
                                    "Capacity_Distribution_Over_Time": {
                                        "Times": vector_habitat_days
                                                  ,
                                                  "Values": vector_habitat_values
                                        },
                                    "Max_Larval_Capacity": 39810717005.534969
                                        }
                            },

                            "Nighttime_Feeding_Fraction": 1,
                            "Transmission_Rate": 1.0,
                            "Vector_Sugar_Feeding_Frequency": "VECTOR_SUGAR_FEEDING_NONE"
                        }
                    ]


                  })

set_climate_constant(cb)

def sweep_coverages(cb,coverage):
    add_health_seeking(cb, start_day = 0,
    drug = ['DHA', 'Piperaquine'],
    targets = [
        {'trigger': 'NewClinicalCase', 'coverage': coverage[0], 'agemin': 0, 'agemax': 5, 'seek': 1,
         'rate': 0.3},
        {'trigger': 'NewClinicalCase', 'coverage': coverage[1], 'agemin': 10, 'agemax': 200,
         'seek': 1,
         'rate': 0.3},
        {'trigger': 'NewSevereCase', 'coverage': 0.30, 'agemin': 0, 'agemax': 200, 'seek': 1,
         'rate': 0.3}]

    ),
    return {'coverage_pair': coverage}
def scale_linear_spline_max_habitat(cb,scale_factor):
    for species_params in cb.get_param("Vector_Species_Params"):
        habitats = species_params["Larval_Habitat_Types"]
        scaled_habitats = habitats.copy()
        scaled_habitats["LINEAR_SPLINE"]["Max_Larval_Capacity"] = habitats["LINEAR_SPLINE"][
                                                                      "Max_Larval_Capacity"] * scale_factor
        species_params["Larval_Habitat_Types"] = scaled_habitats
    return {'larval_habitat_multiplier': scale_factor}

# builder = ModBuilder.from_list( [[ ModFn(sweep_scale_factor, x)] for x in [0.01,10,100]])
report_years = 1
report_start = 50
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


healthseeking_coverage_pairs = [[0.30,0.30]] # as U5 and then >5 year olds

# creates a sweep of simulations with varying coverages and Run_Number seeds
healthseeking = [
            [

               ModFn(sweep_coverages, coverages),
               ModFn(scale_linear_spline_max_habitat, x),
               ModFn(DTKConfigBuilder.set_param,'Run_Number',seed)

            ]
            for x in np.logspace(-3, -0.3, 50)
            for coverages in healthseeking_coverage_pairs
            for seed in range(num_seeds)
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
