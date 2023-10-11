import os
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

#Define gaussian to fit the data to
def fitfunc(t,A,dev,shift,offset):
	return -np.abs(A)*np.e**(-(t-shift)**2/(2*dev**2))+offset

def fancyfit(tims, amps):
	params,errs = curve_fit(fitfunc, tims, amps, p0 = [np.abs(np.min(amps)), 0.1e-8, tims[amps[amps == np.min(amps)].index[0]],0])#,bounds=([0,None,None,None], [1,None,None,None]))

	#calculate the fwhm
	if abs(params[0]) < 0.005 or min(amps) > -0.005: #when we don't see a signal, don't save the results
		maxamp	= None
		fwhm	= None
	else:
		maxamp	= abs(params[0]) * 1E3
		halfmax	= params[3]-(abs(params[0])+params[3])/2
		halfmaxline = [halfmax]*len(tims)
		idx = np.argwhere(np.diff(np.sign(fitfunc(tims, params[0], params[1], params[2], params[3]) - halfmaxline))).flatten() #find the indices where the gaussian is at halfmax
		if len(idx) < 2:
			fwhm = None
		else:
			fwhm = (np.array(tims)[idx[1]]-np.array(tims)[idx[0]]) * 1E9
	
	return maxamp, fwhm

def dumbfit(tims, amps):
	maxamp 	= max(-amps)
	imax 	= np.argmax(-amps)
	t1		= None
	t2 		= None
	for el in range(imax):
		if -amps[imax - el] <= maxamp/2.:
			t1 = tims[imax - el]
			break
	for el in range(imax):
		if -amps[imax + el] <= maxamp/2.:
			t2 = tims[imax + el]
			break
	fwhm	= t2 - t1
	return maxamp * 1E3, fwhm * 1E9

#Extract parameters of interest
def AnalyzeWaveformFunction(outputdf, trigger_file):
	
	input_file = 'pandas_df/' + trigger_file + '.csv'
	
	if not os.path.exists(input_file):
		return

	inputdf = pd.read_csv(input_file)
	trigger_number = int(((input_file.split('Trigger_')[1]).split('.csv'))[0])

	#do analysis for each channel
	if int(trigger_number) not in outputdf.index: #Don't redo analysis!
		mask_amplitude 	= inputdf.columns.str.contains('Amplitude_Channel*')
		mask_time 		= inputdf.columns.str.contains('Time_Channel*')
		df_amplitude 	= inputdf.loc[:, mask_amplitude]
		df_time			= inputdf.loc[:, mask_time]
		number_of_channels = len(df_amplitude.columns)

		for channel_number in range(1, number_of_channels + 1):
			
			amps = df_amplitude['Amplitude_Channel' + str(channel_number)]
			tims = df_time['Time_Channel' + str(channel_number)]
			
			maxamp 	= None
			fwhm	= None
			
			if (min(amps) > -0.010):
				maxamp	= None
				fwhm	= None
			else:
				maxamp, fwhm = dumbfit(tims, amps)
				
				#Now save your results to the ouput dataframe
				if trigger_number not in outputdf.index:
					outputdf.loc[trigger_number] = [None]*len(inputdf.transpose())

			#Now find a way to extract "Amp 1, Amp2, Amp3 etc from file name so we know where to save"
			outputdf['Amp' 	+ str(channel_number) + '[mV]'].loc[trigger_number] = maxamp
			outputdf['FWHM' + str(channel_number) + '[ns]'].loc[trigger_number] = fwhm

	return outputdf

if __name__ == '__main__':
	#define an empty dataframe that we can update with our function (let's not run everything again each time)
	columnnames=["Amp1[mV]", "Amp2[mV]", "Amp3[mV]", "Amp4[mV]", "Amp5[mV]", "Amp6[mV]", "Amp7[mV]", "Amp8[mV]", "FWHM1[ns]","FWHM2[ns]","FWHM3[ns]", "FWHM4[ns]","FWHM5[ns]","FWHM6[ns]","FWHM7[ns]","FWHM8[ns]"]
	df_results = pd.DataFrame(columns = columnnames, dtype='float64')
	
	AnalyzeWaveformFunction(df_results, 'Trigger_00008')
	AnalyzeWaveformFunction(df_results, 'Trigger_00005')

