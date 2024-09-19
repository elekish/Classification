import os
import numpy as np
import pandas as pd
from tkinter import filedialog
from folderplot import plot_data
from characteristics import calculate_statistics

def load_and_extract_data(filepath):
    dataall = pd.read_excel(filepath, sheet_name='240229SN').to_numpy()

    LH = dataall[:, 11::7]
    RH = dataall[:, 12::7]
    LL = dataall[:, 13::7]
    RL = dataall[:, 14::7]

    LH = LH[2:, :]
    RH = RH[2:, :]
    LL = LL[2:, :]
    RL = RL[2:, :]



    return LH, RH, LL, RL

def reshape_data(data, target_shape=(2400, 5)):
    if data.shape[0] < target_shape[0]:

        padded = np.zeros(target_shape)
        padded[:data.shape[0], :data.shape[1]] = data
        return padded
    elif data.shape[0] > target_shape[0]:

        return data[:target_shape[0], :target_shape[1]]
    return data


folder_path = filedialog.askdirectory(title="Select a folder containing Excel files")
data_dict = {
    'A': {
        'LH': [],
        'RH': [],
        'LL': [],
        'RL': [],
    },
    'B': {
        'LH': [],
        'RH': [],
        'LL': [],
        'RL': [],
    },
}
for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        filepath = os.path.join(folder_path, filename)
        LH, RH, LL, RL = load_and_extract_data(filepath)

        if filename[10] == 'A':
            data_dict['A']['LH'].append(reshape_data(LH[:, :5]))
            data_dict['A']['RH'].append(reshape_data(RH[:, :5]))
            data_dict['A']['LL'].append(reshape_data(LL[:, :5]))
            data_dict['A']['RL'].append(reshape_data(RL[:, :5]))

        elif filename[10] == 'B':
            data_dict['B']['LH'].append(reshape_data(LH[:, :5]))
            data_dict['B']['RH'].append(reshape_data(RH[:, :5]))
            data_dict['B']['LL'].append(reshape_data(LL[:, :5]))
            data_dict['B']['RL'].append(reshape_data(RL[:, :5]))


for key in data_dict:
    for sub_key in data_dict[key]:
        if data_dict[key][sub_key]:
            data_dict[key][sub_key] = np.stack(data_dict[key][sub_key])
        else:
            data_dict[key][sub_key] = np.zeros((0, 2400, 5))  # Handling empty cases as needed

LH_all_pre = data_dict['A']['LH']
RH_all_pre = data_dict['A']['RH']
LL_all_pre = data_dict['A']['LL']
RL_all_pre = data_dict['A']['RL']


# print(LH_all_pre)

# plot_data(LH_all_pre, RH_all_pre, LL_all_pre, RL_all_pre)

means_LH, std_devs_LH = calculate_statistics(LH_all_pre)
means_RH, std_devs_RH = calculate_statistics(RH_all_pre)

# Print the results but datatype np.float
# print("LH Means:\n", means_LH)
# print("LH Standard Deviations:\n", std_devs_LH)
# print("RH Means:\n", means_RH)
# print("RH Standard Deviations:\n", std_devs_RH)


print("LH Means:")
print([float(mean) for mean in means_LH])
print("LH Standard Deviations:")
print([float(std_dev) for std_dev in std_devs_LH])
print("RH Means:")
print([float(mean) for mean in means_RH])
print("RH Standard Deviations:")
print([float(std_dev) for std_dev in std_devs_RH])

