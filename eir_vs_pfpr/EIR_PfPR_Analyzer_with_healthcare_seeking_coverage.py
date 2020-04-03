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
        self.tags = ['annual EIR','coverage_pair']
        self.output_fname = output_fname

    def select_simulation_data(self, data, simulation):


        simdata = pd.DataFrame(
            {'pfpr_underfives': [data[self.filenames[0]]['DataByTimeAndAgeBins']['PfPR by Age Bin'][0][0]],
             'pfpr_overfive': [data[self.filenames[0]]['DataByTimeAndAgeBins']['PfPR by Age Bin'][0][1]],
             'ci_underfives': [data[self.filenames[0]]['DataByTimeAndAgeBins']['Annual Clinical Incidence by Age Bin'][0][0]],
             'ci_overfive': [data[self.filenames[0]]['DataByTimeAndAgeBins']['Annual Clinical Incidence by Age Bin'][0][1]],

             }

        )

        for tag in self.tags:

            simdata[tag] = [simulation.tags[tag]]

        return simdata

    def finalize(self, all_data):

        selected = [data for sim, data in all_data.items()]
        if len(selected) == 0:
            print("No data have been returned... Exiting...")
            return

        df = pd.concat(selected).reset_index(drop=True)

        df['group'] = [list(eval(x))[0] for x in df['coverage_pair']]
        df_underfives = df.pivot(index = 'pfpr_underfives', columns = 'group', values = 'ci_underfives')
        df_overfives = df.pivot(index = 'pfpr_overfive', columns = 'group', values = 'ci_overfive')

        df.to_csv('%s_raw_output.csv' % self.output_fname)
        df_underfives.to_csv('%s_underfives.csv' % self.output_fname)
        df_overfives.to_csv('%s_overfives.csv' % self.output_fname)

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

    expids = ['9963e572-3275-ea11-a2c5-c4346bcb1550']
    expnames = ['EIR_sweep']

    for expname, expid in zip(expnames, expids) :
        output_fname = os.path.join(wdir, expid,expname)
        am = AnalyzeManager(expid,
                            analyzers=EIR_PfPR_Analyzer(output_fname))
        am.analyze()

