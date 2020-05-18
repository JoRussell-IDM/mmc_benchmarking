import seaborn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


exp_ids = ['debd1782-c190-ea11-a2c5-c4346bcb1550','60048c83-4095-ea11-a2c5-c4346bcb1550']
cmap = ['#ff0000','#0000ff']
fig,ax = plt.subplots(1,1)

for i,exp_id in enumerate(exp_ids):
    output_fn = os.path.join('.','output',exp_id,'EIR_sweep_inset_chart.csv')
    df = pd.read_csv(output_fn)
    df['log_EIR'] = [np.log10(x*365) for x in df['Daily EIR']]
    ax.scatter(df['log_EIR'],df['True Prevalence'],color = cmap[i],alpha = 0.5)

plt.xlabel('annual EIR (log10)')
plt.ylabel('PfPR')
plt.title('EIR vs PfPR {red = MalariaOngoing,blue = CoTransmission}')
plt.savefig(os.path.join('.','output','combined_EIR_sweep_inset_chart.png'))
plt.show()