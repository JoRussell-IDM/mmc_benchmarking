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
        self.filenames = ['output/MalariaSummaryReport_Annual_Report.json']
        self.tag = 'annual EIR'
        self.output_fname = output_fname

    def select_simulation_data(self, data, simulation):

        pfpr = data[self.filenames[0]]['DataByTime']['PfPR_2to10'][0]


        simdata = pd.DataFrame( {'pfpr' : [pfpr]})
        simdata[self.tag] = simulation.tags[self.tag]
        return simdata

    def finalize(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("No data have been returned... Exiting...")
            return

        df = pd.concat(selected).reset_index(drop=True)
        df.to_csv('%s.csv' % self.output_fname)
        # fig = plt.figure()
        # ax = fig.gca()
        #
        # ax.scatter(df[self.tag], df['pfpr'], 10)
        # ax.set_xscale('log')
        # ax.set_xlabel(self.tag)
        # ax.set_ylabel('PfPR [2 to 10]')
        # ax.set_ylim(0,1)
        #
        # plt.savefig('%s.png' % self.output_fname)
        # plt.savefig('%s.pdf' % self.output_fname, format='PDF')
        #
        # plt.close('all')

if __name__ == '__main__' :

    expids = ['c4b460c7-0c90-ea11-a2c5-c4346bcb1550']
    expnames = ['EIR_sweep']

    for expname, expid in zip(expnames, expids) :
        output_fname = os.path.join(wdir, expid,expname)
        am = AnalyzeManager(expid,
                            analyzers=EIR_PfPR_Analyzer(output_fname))
        am.analyze()

