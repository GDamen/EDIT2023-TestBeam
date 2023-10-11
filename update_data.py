import os
import pandas as pd
import glob

def update_data(input_path, output_path, num_points=10, required_channels=1):
    # Create a DataFrame to store trigger numbers
    trigger_numbers_df = pd.DataFrame(columns=["TriggerNumber"])

    # Check if the input path exists
    if not os.path.exists(input_path):
        print(f"The input path '{input_path}' does not exist.")
        return

    print("Input path exists.")
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Created output directory: {output_path}")

    # Create a dictionary to store DataFrames for each trigger number
    trigger_data = {}

    # Use glob to get a list of CSV file paths with the specified format
    # File name must follow this format: C1--XX--10294.csv where:
    # C represents Channel
    # 1 represents the channel number
    # XX represents the frequency
    # 10294 represents the trigger number
    file_paths = sorted(glob.glob(f'{input_path}C*--*--*.csv'))

    if not file_paths:
        print(f"No CSV files meeting the criteria found in the input path.")
        return

    print(f"Found {len(file_paths)} CSV file(s) meeting the criteria.")

    # Loop through the CSV files and organize data by trigger number and channel
    for file_path in file_paths:
        # Parse trigger number from the file name
        filename = os.path.basename(file_path)
        parts = filename.split('--')

        # Flag: Check if the file has the correct format
        if len(parts) != 3:
            print(f"Skipping file '{file_path}' due to incorrect file name format.")
            continue

        # Extracting the information from the CSV file name
        channel_number 	= parts[0][1:]  # Extract channel number (remove 'C')
        frequency 		= parts[1]
        trigger_number 	= parts[2].replace('.csv', '')  # Remove '.csv' from trigger number

        # Check if the trigger number is not already in the DataFrame
        if trigger_number not in trigger_numbers_df["TriggerNumber"].values:
            # Add the trigger number to the DataFrame
            trigger_numbers_df = pd.concat([trigger_numbers_df, pd.DataFrame({"TriggerNumber": [trigger_number]})], ignore_index=True)

            print(f"Added Trigger Number {trigger_number} to trigger_numbers_df.")

        # Check if the trigger has the required number of channels
        # Each trigger must have the required number of channels before it is added to the dataframe
        if len(trigger_data.get(trigger_number, [])) < required_channels:
            # Read the CSV file into a DataFrame, skip the header rows, and extract the Time and Amplitude columns
            df = pd.read_csv(file_path, skiprows=9, names=["Time", "Ampl"], encoding="utf-8")

            # Select the specified number of points.
            df = df.iloc[:, :num_points]

            # Create a dictionary entry for this file
            file_data = {
                f"Time_Channel{channel_number}": df["Time"].values,
                f"Amplitude_Channel{channel_number}": df["Ampl"].values,
            }

            # Append the data to the appropriate channel list in the dictionary
            if trigger_number not in trigger_data:
                trigger_data[trigger_number] = []

            # Check if the current channel is within the required channels
            if int(channel_number) <= required_channels:
                trigger_data[trigger_number].append(pd.DataFrame(file_data))
                print(f"Processed CSV file '{file_path}' for Trigger Number {trigger_number}.")

    # Check if there are additional DataFrames to save
    if trigger_data:
        # Save each trigger's data to a separate CSV file with times and amplitudes grouped by channel
        for trigger_number, channel_dataframes in trigger_data.items():
            # Check if the number of channels matches the required channels
            if len(channel_dataframes) == required_channels:
                # Concatenate DataFrames for each channel
                combined_df = pd.concat(channel_dataframes, axis=1)

                # Rearrange the columns to group the time and amplitude in chronological order
                sorted_columns = []
                for i in range(1, required_channels + 1):
                    sorted_columns.extend([f"Time_Channel{i}", f"Amplitude_Channel{i}"])

                # Check if there are columns to sort
                if sorted_columns:
                    combined_df = combined_df[sorted_columns]

                    # Save the data to a CSV file
                    trigger_filename = f'Trigger_{trigger_number}.csv'
                    trigger_file_path = os.path.join(output_path, trigger_filename)
                    combined_df.to_csv(trigger_file_path, index=False)
                    print(f"Saved data for Trigger Number {trigger_number} to '{trigger_filename}'.")
                else:
                    print(f"Skipping Trigger Number {trigger_number} due to insufficient columns.")
            else:
                print(f"Skipping Trigger Number {trigger_number} due to insufficient channels.")


        # Save the trigger_numbers_df DataFrame to the output directory as a CSV file with UTF-8 encoding
        trigger_numbers_df["TriggerNumber"] = trigger_numbers_df["TriggerNumber"].apply(lambda x: f"Trigger_{x.zfill(5)}")
        trigger_numbers_df.to_csv(os.path.join(output_path, 'trigger_numbers.csv'), index=False, encoding='utf-8')

        print("Saved trigger_numbers_df to 'trigger_numbers.csv'.")
    else:
        print("No CSV files meeting the criteria found in the input path.")
