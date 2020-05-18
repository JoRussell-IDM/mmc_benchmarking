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

expids = ['4f157763-d898-ea11-a2c5-c4346bcb1550','3f4bf407-fa96-ea11-a2c5-c4346bcb1550']
n_exps = len(expids)

descriptors = ['no seasonality','with seasonality']
expnames = ['EIR_sweep']*n_exps
counters = np.arange(n_exps)
cmap = ['#ff0000','#0000ff']

df_all = pd.DataFrame()
fig,ax = plt.subplots()

for i,expname, expid,descriptor in zip(counters, expnames, expids,descriptors):
    output_fname = os.path.join(wdir, expid, expname)
    df = pd.read_csv('%s.csv' % output_fname)

    ax.scatter(np.log10(df['aEIR']), df['PfPR_2to10'],color = cmap[i], alpha = 0.5)
    ax.set_xlabel('aEIR (log10)')
    ax.set_ylabel('PfPR [2 to 10]')
    ax.set_ylim(0, 1)

plt.legend(descriptors)
plt.title('PfPR [2 to 10] v. aEIR')
plt.savefig('%s.png' % os.path.join(wdir, expnames[0]))
plt.savefig('%s.pdf' % os.path.join(wdir, expnames[0]), format='PDF')
plt.show()

plt.close('all')