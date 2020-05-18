import os
import numpy as np
from dtk.utils.core.DTKConfigBuilder import DTKConfigBuilder
from dtk.generic.climate import set_climate_constant

from simtools.SetupParser import SetupParser
from simtools.ExperimentManager.ExperimentManagerFactory import ExperimentManagerFactory
from simtools.ModBuilder import  ModFn, ModBuilder

from malaria.reports.MalariaReport import add_patient_report, add_survey_report, add_summary_report

from dtk.interventions.input_EIR import add_InputEIR

# General --------------------------------------------------------------------------------------------------------
exp_name = 'PfPR_by_EIR_sweep_CoTransmission_fixedEXE'
years = 50 # length of simulation, in years
num_seeds = 5
report_start = years-5
# Setup ----------------------------------------------------------------------------------------------------------
# config_path = os.path.join('.', 'inputs','config.json')
# cb = DTKConfigBuilder.from_files(config_path)

cb = DTKConfigBuilder.from_defaults('MALARIA_SIM')

cb.update_params({
    "Demographics_Filenames": ["Namawala_single_node_demographics_balanced_pop_growth.json"],
    "x_Base_Population":1,
    "Enable_Disease_Mortality":0,
    "Simulation_Duration":years*365,
    "Enable_Malaria_CoTransmission": 1,
    "Max_Individual_Infections": 10,
    "Number_Basestrains": 1,
    "Number_Substrains": 0,
    "Maternal_Antibodies_Type": "OFF",
    "Age_Dependent_Biting_Risk_Type": "OFF",
    "Incubation_Period_Distribution": "CONSTANT_DISTRIBUTION",
    "Vector_Species_Names": ["SillySkeeter"],
    "Vector_Sampling_Type": "TRACK_ALL_VECTORS",
    "Vector_Species_Params": [
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
                "CONSTANT": 80000000,
                    "TEMPORARY_RAINFALL": 800000000
            },
            "Nighttime_Feeding_Fraction": 1,
            "Transmission_Rate": 1.0,
            "Vector_Sugar_Feeding_Frequency": "VECTOR_SUGAR_FEEDING_NONE"
        }
    ]


})

set_climate_constant(cb)

#Experimental Design -------------------------------------------------------------------------------------------------
def sweep_larval_habitat(cb, scale_factor) :
    cb.update_params({"x_Temporary_Larval_Habitat": scale_factor })
    return { 'larval_habitat_multiplier' : scale_factor}


#Reporting -----------------------------------------------------------------------------------------------------------
add_summary_report(cb,
                   start = 365*report_start,
                   description='Annual_Report',
                   interval = 365,
                   nreports = 1,
                   age_bins = [2, 10, 125],
                   parasitemia_bins = [0, 50, 200, 500, 2000000]
                   )

builder = ModBuilder.from_list(
    [
            [
                ModFn(sweep_larval_habitat, scale_factor = habitat_multiplier),
                ModFn(DTKConfigBuilder.set_param,'Run_Number',seed)
            ]
        for habitat_multiplier in np.logspace(-2, 1, 50)
        for seed in range(num_seeds)
    ]
)


# builder = ModBuilder.from_list( [[ ModFn(sweep_scale_factor, x)] for x in [0.01,10,100]])
# report_years = 1
# report_start = 40


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
