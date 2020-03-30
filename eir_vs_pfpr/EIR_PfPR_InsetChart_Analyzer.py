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

class EIR_PfPR_Analyzer(BaseAnalyzer):
    def __init__(self, output_fname):
        super(EIR_PfPR_Analyzer, self).__init__()
        self.filenames = ['output/InsetChart.json']
        self.tag = 'annual EIR'
        self.output_fname = output_fname
        self.channels = ['True Prevalence','PCR Parasite Prevalence', 'PfHRP2 Prevalence','Blood Smear Parasite Prevalence']

    def select_simulation_data(self, data, simulation):
        simdata = pd.DataFrame()
        year_to_report = 40
        for channel in self.channels:

            pfpr = np.mean(data[self.filenames[0]]['Channels'][channel]['Data'][year_to_report*365:(year_to_report*365+365)])
            simdata[channel] = pd.Series(pfpr)

        simdata[self.tag] = simulation.tags[self.tag]
        return simdata

    def finalize(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("No data have been returned... Exiting...")
            return

        df = pd.concat(selected).reset_index(drop=True)
        df.to_csv('%s_inset_chart.csv' % self.output_fname)

if __name__ == '__main__' :

    expids = ['9877c946-b54e-ea11-a2c3-c4346bcb1551']
    expnames = ['EIR_sweep']

    for expname, expid in zip(expnames, expids) :
        output_fname = os.path.join(wdir, expid,expname)
        am = AnalyzeManager(expid,
                            analyzers=EIR_PfPR_Analyzer(output_fname))
        am.analyze()

