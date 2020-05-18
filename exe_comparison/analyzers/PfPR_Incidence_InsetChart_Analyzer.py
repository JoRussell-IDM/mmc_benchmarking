import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from simtools.Analysis.AnalyzeManager import AnalyzeManager
from simtools.Analysis.BaseAnalyzers import BaseAnalyzer
from simtools.SetupParser import SetupParser
from scipy import interpolate
import os

mpl.rcParams['pdf.fonttype'] = 42
if not SetupParser.initialized:
    SetupParser.init('HPC')

wdir = os.path.join(os.getcwd(),'output')

class PfPR_Incidence_Analyzer(BaseAnalyzer):
    def __init__(self, output_fname):
        super(PfPR_Incidence_Analyzer, self).__init__()
        self.filenames = ['output/InsetChart.json']
        # self.tag = 'annual EIR'
        self.output_fname = output_fname
        self.channels = ['True Prevalence','New Clinical Cases', 'Statistical Population']

    def select_simulation_data(self, data, simulation):
        simdata = pd.DataFrame()
        year_to_report = 40

        for channel in self.channels:
            value = np.mean(data[self.filenames[0]]['Channels'][channel]['Data'][
                            year_to_report * 365:(year_to_report * 365 + 365)])
            simdata[channel] = pd.Series(value)

        # simdata[self.tag] = simulation.tags[self.tag]
        simdata['id'] = simulation.id
        return simdata

    def finalize(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("No data have been returned... Exiting...")
            return

        df = pd.concat(selected).reset_index(drop=True)
        df.to_csv('%s_inset_chart.csv' % self.output_fname)

if __name__ == '__main__' :

    expids = ['debd1782-c190-ea11-a2c5-c4346bcb1550','5c02844c-7590-ea11-a2c5-c4346bcb1550']
    expnames = ['PfPR_Incidence','PfPR_Incidence']

    for expname, expid in zip(expnames, expids) :
        output_fname = os.path.join(wdir, expid,expname)
        os.makedirs(output_fname,exist_ok=True)

        am = AnalyzeManager(expid,
                            analyzers=PfPR_Incidence_Analyzer(output_fname))
        am.analyze()

