import os
import re
import pandas as pd
import matplotlib.pyplot as plt

import analyzewaveformfunction

def plot_and_save_amplitude_vs_time(trigger_numbers_df, data_path, output_path, trigger_to_process=None, required_channels=4, num_points=1000):
	# Read the trigger numbers DataFrame
	trigger_numbers = trigger_numbers_df["TriggerNumber"].tolist()

	# Determine the triggers to process based on user input
	if trigger_to_process is not None:
		#triggers_to_process = set(trigger_to_process)
		triggers_to_process = trigger_to_process
	else:
		#triggers_to_process = set(trigger_numbers)
		triggers_to_process = trigger_numbers

	# Create the output directory if it doesn't exist
	if not os.path.exists(output_path):
		os.makedirs(output_path)

	# Loop through each trigger number
	for trigger_number in triggers_to_process:
		# Create the file path for the trigger-specific data
		numeric_trigger_number = re.search(r'\d+', trigger_number).group(0)
		data_file = os.path.join(data_path, f"Trigger_{numeric_trigger_number.zfill(5)}.csv")

		# Check if the data file exists
		if not os.path.exists(data_file):
			print(f"Data file for Trigger {trigger_number} not found. Skipping.")
			continue

		# Read the data file into a DataFrame
		df = pd.read_csv(data_file)

		# Extract the time and amplitude columns for each channel
		time_columns = [f"Time_Channel{i}" for i in range(1, required_channels + 1)]
		amplitude_columns = [f"Amplitude_Channel{i}" for i in range(1, required_channels + 1)]

		# Create a single plot for all channels of the same trigger
		plt.figure(figsize=(10, 6))
		for i in range(required_channels):
			channel_num = i + 1
			if time_columns[i] in df.columns and amplitude_columns[i] in df.columns:
				plt.plot(df[time_columns[i]][:num_points], df[amplitude_columns[i]][:num_points], label=f"Channel {channel_num}")

		plt.xlabel("Time")
		plt.ylabel("Amplitude")
		plt.title(f"Trigger {trigger_number} - Amplitudes vs. Time")
		plt.grid(True)
		plt.legend(title="Channels", labels=[f"Amplitude_Channel{i} Trigger {trigger_number}" for i in range(1, required_channels + 1)])
		plt.tight_layout()

		# Save the plot as a PNG file
		plot_filename = f"Trigger_{trigger_number}_Amplitudes.png"
		plot_path = os.path.join(output_path, plot_filename)
		plt.savefig(plot_path)
		plt.close()

		print(f"Saved plot for Trigger {trigger_number} - Amplitudes vs. Time to {plot_filename}")
		
def compute_parameters(trigger_numbers_df, data_path, output_path, trigger_to_process=None, required_channels=4, num_points=1000):
	# Read the trigger numbers DataFrame
	trigger_numbers = trigger_numbers_df["TriggerNumber"].tolist()

	#define an empty dataframe that we can update with our function (let's not run everything again each time)
	columnnames=["Amp1[mV]", "Amp2[mV]", "Amp3[mV]", "Amp4[mV]", "Amp5[mV]", "Amp6[mV]", "Amp7[mV]", "Amp8[mV]", "FWHM1[ns]","FWHM2[ns]","FWHM3[ns]","FWHM4[ns]", "FWHM5[ns]","FWHM6[ns]","FWHM7[ns]","FWHM8[ns]"]
	df_results = pd.DataFrame(columns = columnnames, dtype='float64')

	# Determine the triggers to process based on user input
	if trigger_to_process is not None:
		triggers_to_process = trigger_to_process
	else:
		triggers_to_process = trigger_numbers

	for trigger_number in triggers_to_process:
		print(f"Computed parameters for Trigger {trigger_number}")
		analyzewaveformfunction.AnalyzeWaveformFunction(df_results, trigger_number)
		
	df_results.to_csv(os.path.join(data_path, 'results.csv'), index=False, encoding='utf-8')
