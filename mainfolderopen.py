import os
import numpy as np
import pandas as pd
from tkinter import filedialog
from folderplot import plot_data
from characteristics import calculate_statistics,flatten_3d_to_2d, z_normalize, \
    process_batches_for_normalised, process_batches_raw

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

LH_all_post = data_dict['B']['LH']
RH_all_post = data_dict['B']['RH']
LL_all_post = data_dict['B']['LL']
RL_all_post = data_dict['B']['RL']




# plot_data(LH_all_pre, RH_all_pre, LL_all_pre, RL_all_pre)

means_LH_all_pre, std_devs_LH_all_pre = calculate_statistics(LH_all_pre)
means_RH_all_pre, std_devs_RH_all_pre = calculate_statistics(RH_all_pre)
means_LH_all_post, std_devs_LH_all_post = calculate_statistics(LH_all_post)
means_RH_all_post, std_devs_RH_all_post = calculate_statistics(RH_all_post)

# Print the results but datatype np.float
# print("LH Means:\n", means_LH)
# print("LH Standard Deviations:\n", std_devs_LH)
# print("RH Means:\n", means_RH)
# print("RH Standard Deviations:\n", std_devs_RH)


# print("LH Means:")
# print([float(mean) for mean in means_LH])
# print("LH Standard Deviations:")
# print([float(std_dev) for std_dev in std_devs_LH])
# print("RH Means:")
# print([float(mean) for mean in means_RH])
# print("RH Standard Deviations:")
# print([float(std_dev) for std_dev in std_devs_RH])

LH_all_pre_normalised=flatten_3d_to_2d(LH_all_pre)
LH_all_pre_raw=LH_all_pre_normalised
for i in range(0,len(means_LH_all_pre)):
  LH_all_pre_normalised[i]=z_normalize(LH_all_pre_normalised[i],means_LH_all_pre[i],std_devs_LH_all_pre[i])

RH_all_pre_normalised=flatten_3d_to_2d(RH_all_pre)
RH_all_pre_raw=RH_all_pre_normalised
for i in range(0,len(means_RH_all_pre)):
  RH_all_pre_normalised[i]=z_normalize(RH_all_pre_normalised[i],means_RH_all_pre[i],std_devs_RH_all_pre[i])

LH_all_post_normalised=flatten_3d_to_2d(LH_all_post)
LH_all_post_raw=LH_all_post_normalised
for i in range(0,len(means_LH_all_post)):
  LH_all_post_normalised[i]=z_normalize(LH_all_post_normalised[i],means_LH_all_post[i],std_devs_LH_all_post[i])

RH_all_post_normalised=flatten_3d_to_2d(RH_all_post)
RH_all_post_raw=RH_all_post_normalised
for i in range(0,len(means_RH_all_post)):
  RH_all_post_normalised[i]=z_normalize(RH_all_post_normalised[i],means_RH_all_post[i],std_devs_RH_all_post[i])




normalised_variances_pre_LH = []
normalised_kurtoses_pre_LH = []
for array in LH_all_pre_normalised:
    var, kurt = process_batches_for_normalised(array)
    normalised_variances_pre_LH.append(var)
    normalised_kurtoses_pre_LH.append(kurt)
normalised_variances_pre_LH = np.array(normalised_variances_pre_LH)
normalised_kurtoses_pre_LH = np.array(normalised_kurtoses_pre_LH)


normalised_variances_pre_RH = []
normalised_kurtoses_pre_RH = []
for array in RH_all_pre_normalised:
    var, kurt = process_batches_for_normalised(array)
    normalised_variances_pre_RH.append(var)
    normalised_kurtoses_pre_RH.append(kurt)
normalised_variances_pre_RH = np.array(normalised_variances_pre_RH)
normalised_kurtoses_pre_RH = np.array(normalised_kurtoses_pre_RH)


raw_means_pre_LH=[]
raw_stddev_pre_LH=[]
raw_variance_pre_LH=[]
raw_skewness_pre_LH=[]
for array in LH_all_pre_raw:
    mean, std, var, skew = process_batches_raw(array)
    raw_means_pre_LH.append(mean)
    raw_stddev_pre_LH.append(std)
    raw_variance_pre_LH.append(var)
    raw_skewness_pre_LH.append(skew)
raw_means_pre_LH = np.array(raw_means_pre_LH)
raw_stddev_pre_LH = np.array(raw_stddev_pre_LH)
raw_variance_pre_LH=np.array(raw_variance_pre_LH)
raw_skewness_pre_LH=np.array(raw_skewness_pre_LH)


raw_means_pre_RH=[]
raw_stddev_pre_RH=[]
raw_variance_pre_RH=[]
raw_skewness_pre_RH=[]
for array in RH_all_pre_raw:
    mean, std, var, skew = process_batches_raw(array)
    raw_means_pre_RH.append(mean)
    raw_stddev_pre_RH.append(std)
    raw_variance_pre_RH.append(var)
    raw_skewness_pre_RH.append(skew)
raw_means_pre_RH = np.array(raw_means_pre_RH)
raw_stddev_pre_RH = np.array(raw_stddev_pre_RH)
raw_variance_pre_RH=np.array(raw_variance_pre_RH)
raw_skewness_pre_RH=np.array(raw_skewness_pre_RH)



normalised_variances_post_LH = []
normalised_kurtoses_post_LH = []
for array in LH_all_post_normalised:
    var, kurt = process_batches_for_normalised(array)
    normalised_variances_post_LH.append(var)
    normalised_kurtoses_post_LH.append(kurt)
normalised_variances_post_LH = np.array(normalised_variances_post_LH)
normalised_kurtoses_post_LH = np.array(normalised_kurtoses_post_LH)


normalised_variances_post_RH = []
normalised_kurtoses_post_RH = []
for array in RH_all_post_normalised:
    var, kurt = process_batches_for_normalised(array)
    normalised_variances_post_RH.append(var)
    normalised_kurtoses_post_RH.append(kurt)
normalised_variances_post_RH = np.array(normalised_variances_post_RH)
normalised_kurtoses_post_RH = np.array(normalised_kurtoses_post_RH)


raw_means_post_LH=[]
raw_stddev_post_LH=[]
raw_variance_post_LH=[]
raw_skewness_post_LH=[]
for array in LH_all_post_raw:
    mean, std, var, skew = process_batches_raw(array)
    raw_means_post_LH.append(mean)
    raw_stddev_post_LH.append(std)
    raw_variance_post_LH.append(var)
    raw_skewness_post_LH.append(skew)
raw_means_post_LH = np.array(raw_means_post_LH)
raw_stddev_post_LH = np.array(raw_stddev_post_LH)
raw_variance_post_LH=np.array(raw_variance_post_LH)
raw_skewness_post_LH=np.array(raw_skewness_post_LH)


raw_means_post_RH=[]
raw_stddev_post_RH=[]
raw_variance_post_RH=[]
raw_skewness_post_RH=[]
for array in RH_all_post_raw:
    mean, std, var, skew = process_batches_raw(array)
    raw_means_post_RH.append(mean)
    raw_stddev_post_RH.append(std)
    raw_variance_post_RH.append(var)
    raw_skewness_post_RH.append(skew)
raw_means_post_RH = np.array(raw_means_post_RH)
raw_stddev_post_RH = np.array(raw_stddev_post_RH)
raw_variance_post_RH=np.array(raw_variance_post_RH)
raw_skewness_post_RH=np.array(raw_skewness_post_RH)
