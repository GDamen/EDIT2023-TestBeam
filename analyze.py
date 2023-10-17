import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import glob

noise_value = 10

# Fill here your functions
def getMaxAmplitude(amps):
	return max(-amps) * 1E3

def getFWHM(tims, amps):
	return 0

def getNoise(amps):
	return 0

def getSlewRate(tims, amps):
	return 0

def getPosition(amps):
	return 0

#Extract parameters of interest
def AnalyzeWaveformFunction(outputdf, input_file):

	inputdf 		= pd.read_csv(input_file)
	trigger_number 	= int(((input_file.split('Trigger_')[1]).split('.csv'))[0])

	#do analysis for each channel
	#if int(trigger_number) not in outputdf.index: #Don't redo analysis!
	print('New file found! ' + input_file)
	mask_amplitude 	= inputdf.columns.str.contains('Amplitude_Channel*')
	mask_time 		= inputdf.columns.str.contains('Time_Channel*')
	df_amplitude 	= inputdf.loc[:, mask_amplitude]
	df_time			= inputdf.loc[:, mask_time]
	number_of_channels = len(df_amplitude.columns)

	for channel_number in range(1, number_of_channels + 1):
		
		amps = df_amplitude['Amplitude_Channel' + str(channel_number)]
		tims = df_time['Time_Channel' + str(channel_number)]

		maxamp 	= getMaxAmplitude(amps)
		fwhm 	= getFWHM(tims, amps)

		if (maxamp < noise_value):
			maxamp	= None
			fwhm	= None
			
		#Now save your results to the ouput dataframe
		if trigger_number not in outputdf.index:
			outputdf.loc[trigger_number] = [None]*len(inputdf.transpose())

		#Now find a way to extract "Amp 1, Amp2, Amp3 etc from file name so we know where to save"
		outputdf['Amp' 	+ str(channel_number) + '[mV]'].loc[trigger_number] = maxamp
		outputdf['FWHM' + str(channel_number) + '[ns]'].loc[trigger_number] = fwhm
	return outputdf

def acquire():
	#define an empty dataframe that we can update with our function (let's not run everything again each time)
	columnnames=["Amp1[mV]", "Amp2[mV]", "Amp3[mV]", "Amp4[mV]", "Amp5[mV]", "Amp6[mV]", "Amp7[mV]", "Amp8[mV]", "FWHM1[ns]","FWHM2[ns]","FWHM3[ns]", "FWHM4[ns]","FWHM5[ns]","FWHM6[ns]","FWHM7[ns]","FWHM8[ns]"]
	
    # Create a DataFrame to store trigger numbers

	input_path = 'dataset/pandas_df/'

	if not os.path.exists(input_path + 'results.csv'):
		print("results.csv does not exist. Creating...")
		df_results = pd.DataFrame(columns = columnnames, dtype = 'float64')
	else:
		df_results = pd.read_csv(input_path + 'results.csv', index_col='Trigger')

	file_path = sorted(glob.glob(f'{input_path}Trigger_*.csv'))

	for f in file_path:
		df_results = AnalyzeWaveformFunction(df_results, f)

	df_results.to_csv(os.path.join(input_path, 'results.csv'), index=True, index_label='Trigger', encoding='utf-8')
	print("Saved results to 'results.csv'.")

if __name__ == '__main__':
	acquire()
