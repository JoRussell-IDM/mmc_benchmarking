import seaborn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


exp_ids = ['debd1782-c190-ea11-a2c5-c4346bcb1550','5c02844c-7590-ea11-a2c5-c4346bcb1550']
cmap = ['#ff0000','#0000ff']
fig,ax = plt.subplots(1,1)

for i,exp_id in enumerate(exp_ids):
    output_fn = os.path.join('.','output',exp_id,'PfPR_Incidence_inset_chart.csv')
    df = pd.read_csv(output_fn)
    df['Annual Incidence'] = [x*365/df['Statistical Population'][i] for i,x in enumerate(df['New Clinical Cases'])]
    ax.scatter(df['True Prevalence'],df['Annual Incidence'],color = cmap[i],alpha = 0.5)

plt.xlabel('PfPR')
plt.ylabel('Annual Incidence')
plt.title('PfPR vs Annual Clinical Incidence {red = MalariaOngoing,blue = CoTransmission}')
plt.savefig(os.path.join('.','output','combined_PfPR_Incidence_inset_chart.png'))
plt.show()