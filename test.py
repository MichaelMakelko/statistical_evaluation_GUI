import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

freq = '30s'

df = pd.DataFrame(np.random.randint(10, size=4*24*200*20))
df.index = pd.date_range(start='2019-02-01 11:30:00', periods=200*24*4*20, freq=freq)

df['hour'] = df.index.strftime('%H:%M:%S')
df['dayofyear'] = df.index.date


df = df.pivot(index='dayofyear', columns='hour', values=df.columns[0])

print(df)
df.columns = pd.DatetimeIndex(df.columns).strftime('%H:%M')
df.index = pd.DatetimeIndex(df.index).strftime('%m/%Y')


xticks_spacing = int(pd.Timedelta('2h')/pd.Timedelta(freq))
ax = sns.heatmap(df, xticklabels=xticks_spacing, yticklabels=30)
plt.yticks(rotation=0)
plt.show()