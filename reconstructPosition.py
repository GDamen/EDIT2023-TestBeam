import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

channel_map = [[2, 5, 6, 7, 8, 3, 1, 4], [1, 2, 3, 4, 5, 6, 7, 8]]


def reconstructPosition(df):
	print(df)


general_path = '/home/gdamen/projects/EDIT2023/'

output_path = general_path + 'pandas_df/'  # Output path for dataframe
df_results = pd.read_csv(os.path.join(output_path, 'results.csv'))	
	
print (df_results)

for trigger in range(len(df_results)):
	print(df_results['Amp3[mV]'].loc[trigger])
	break
	#reconstructPosition(trigger)
