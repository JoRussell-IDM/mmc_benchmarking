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
        self.tags = ['coverage_pair']
        self.output_fname = output_fname

    def select_simulation_data(self, data, simulation):


        simdata = pd.DataFrame(
            {'aEIR': [data[self.filenames[0]]['DataByTime']['Annual EIR'][0]],
             'PfPR_2to10': [data[self.filenames[0]]['DataByTime']['PfPR_2to10'][0]]

             }

        )


        return simdata

    def finalize(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("No data have been returned... Exiting...")
            return

        df = pd.concat(selected).reset_index(drop=True)

        df.to_csv('%s.csv' % self.output_fname)

        fig = plt.figure()
        ax = fig.gca()
        max_EIR = np.max(df['aEIR'])
        ax.scatter(np.log10(df['aEIR']), df['PfPR_2to10'])

        ax.set_xlabel('aEIR')
        ax.set_ylabel('PfPR [2 to 10]')
        ax.set_ylim(0,1)

        plt.title('PfPR [2 to 10] v. aEIR')


        plt.savefig('%s.png' % self.output_fname)
        plt.savefig('%s.pdf' % self.output_fname, format='PDF')

        plt.close('all')

if __name__ == '__main__' :

    expids = ['4f157763-d898-ea11-a2c5-c4346bcb1550']
    expnames = ['EIR_sweep']

    for expname, expid in zip(expnames, expids) :
        os.makedirs(os.path.join(wdir, expid),exist_ok=True)
        output_fname = os.path.join(wdir, expid,expname)
        am = AnalyzeManager(expid,
                            analyzers=EIR_PfPR_Analyzer(output_fname))
        am.analyze()

