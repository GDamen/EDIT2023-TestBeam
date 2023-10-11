import os
import pandas as pd

import plot_wf
import update_data


general_path = '/home/gdamen/projects/EDIT2023/'

input_path = general_path + 'DATA/DryRun2-take2/DryRun2-take2/'  # Location of waveform csv files
if not os.path.exists(input_path):
    print('Input path does not exist')
    quit()

output_path = general_path + 'pandas_df/'  # Output path for dataframe
if not os.path.exists(output_path):
    print("Output path does not exist. Creating /pandas_df/")
    os.mkdir(general_path + 'pandas_df/')

output_directory = general_path + 'plots/'
if not os.path.exists(output_directory):
    print("Plot path does not exist. Creating /plots/")
    os.mkdir(general_path + 'plots/')


trigger_numbers_df = pd.read_csv(output_path + 'trigger_numbers.csv')


num_points 			= 100  # Set the number of points to use. Warning/Note: Running over a large amount of points will freeze jupyter
required_channels 	= 8 # Set

required_channels 	= 8  # Replace with the number of channels you want to process
trigger_to_process 	= None  # If set to None, trigger_to_process will execute on all triggers.  #If you want to set specific triggers, here's an example: trigger_to_process = [10240, 10241, 10242]
num_points 			= 100

#update_data.update_data(input_path, output_path, num_points, required_channels)
#plot_wf.plot_and_save_amplitude_vs_time(trigger_numbers_df, output_path, output_directory, trigger_to_process, required_channels, num_points)
plot_wf.compute_parameters(trigger_numbers_df, output_path, output_directory, trigger_to_process, required_channels, num_points)
