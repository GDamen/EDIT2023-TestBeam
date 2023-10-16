import os
import re
import pandas as pd
import matplotlib.pyplot as plt

#df_results = pd.DataFrame(columns = columnnames, dtype='float64')
general_path = '.'

output_path = general_path  # Output path for dataframe
df_results = pd.read_csv(os.path.join(output_path, 'results.csv'))

binning = 50
fig, axs = plt.subplots(2, 4)
axs[0, 0].hist(df_results['Amp1[mV]'].dropna(), bins=binning, range = [0, 150], histtype='step', density=True)
axs[0, 1].hist(df_results['Amp2[mV]'].dropna(), bins=binning, range = [0, 150], histtype='step', density=True)
axs[0, 2].hist(df_results['Amp3[mV]'].dropna(), bins=binning, range = [0, 150], histtype='step', density=True)
axs[0, 3].hist(df_results['Amp4[mV]'].dropna(), bins=binning, range = [0, 150], histtype='step', density=True)
axs[1, 0].hist(df_results['Amp5[mV]'].dropna(), bins=binning, range = [0, 150], histtype='step', density=True)
axs[1, 1].hist(df_results['Amp6[mV]'].dropna(), bins=binning, range = [0, 150], histtype='step', density=True)
axs[1, 2].hist(df_results['Amp7[mV]'].dropna(), bins=binning, range = [0, 150], histtype='step', density=True)
axs[1, 3].hist(df_results['Amp8[mV]'].dropna(), bins=binning, range = [0, 150], histtype='step', density=True)

axs[0,0].set_title('Channel 1')
axs[0,1].set_title('Channel 2')
axs[0,2].set_title('Channel 3')
axs[0,3].set_title('Channel 4')
axs[1,0].set_title('Channel 5')
axs[1,1].set_title('Channel 6')
axs[1,2].set_title('Channel 7')
axs[1,3].set_title('Channel 8')

axs[0,0].set_xlabel('Amplitude [mV]')
axs[0,1].set_xlabel('Amplitude [mV]')
axs[0,2].set_xlabel('Amplitude [mV]')
axs[0,3].set_xlabel('Amplitude [mV]')
axs[1,0].set_xlabel('Amplitude [mV]')
axs[1,1].set_xlabel('Amplitude [mV]')
axs[1,2].set_xlabel('Amplitude [mV]')
axs[1,3].set_xlabel('Amplitude [mV]')

axs[0,0].set_ylabel('counts [a.u.]')
axs[0,1].set_ylabel('counts [a.u.]')
axs[0,2].set_ylabel('counts [a.u.]')
axs[0,3].set_ylabel('counts [a.u.]')
axs[1,0].set_ylabel('counts [a.u.]')
axs[1,1].set_ylabel('counts [a.u.]')
axs[1,2].set_ylabel('counts [a.u.]')
axs[1,3].set_ylabel('counts [a.u.]')

plt.subplots_adjust(left=0.04,
                    bottom=0.04, 
                    right=0.96, 
                    top=0.96, 
                    wspace=0.25, 
                    hspace=0.25)

plt.show()
