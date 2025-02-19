import os
import numpy as np
import pandas as pd
from tkinter import filedialog
from plot import plot_data, plot_state_means
from characteristics import calculate_statistics, flatten_3d_to_2d, z_normalize, \
    process_batches_for_normalised, process_batches_raw, flatten_3d_to_2d_col
import matplotlib.pyplot as plt
import seaborn as sns


def load_and_extract_data(filepath):
    # try:
    dataall = pd.read_excel(filepath, sheet_name='240229SN').to_numpy()
    # except ValueError as e:
    #     print(f"Error processing {filename}: {e}")


    LH = dataall[:, 11:43:7]
    RH = dataall[:, 12:43:7]
    LL = dataall[:, 13:43:7]
    RL = dataall[:, 14:43:7]

    LH = LH[2:2404, :]
    RH = RH[2:2404, :]
    LL = LL[2:2404, :]
    RL = RL[2:2404, :]



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
data_dictP = {
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

data_dictNP = {
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
# for filename in os.listdir(folder_path):
#     if filename.endswith('.xlsx'):
#         filepath = os.path.join(folder_path, filename)
#         try:
#             LH, RH, LL, RL = load_and_extract_data(filepath)
#
#             # Additional debug print to catch string values before processing
#             print(f"Checking for non-numeric values in {filename}")
#             print("LH:", LH)
#             print("RH:", RH)
#
#         except ValueError as e:
#             print(f"Error processing {filename}: {e}")
for filename in os.listdir(folder_path):
    if filename.endswith('.xlsx'):
        filepath = os.path.join(folder_path, filename)
        LH, RH, LL, RL = load_and_extract_data(filepath)

        if filename[9] == 'A':
            if filename[10]=='P':
                data_dictP['A']['LH'].append(reshape_data(LH[:, :5]))
                data_dictP['A']['RH'].append(reshape_data(RH[:, :5]))
                data_dictP['A']['LL'].append(reshape_data(LL[:, :5]))
                data_dictP['A']['RL'].append(reshape_data(RL[:, :5]))
            else:
                data_dictNP['A']['LH'].append(reshape_data(LH[:, :5]))
                data_dictNP['A']['RH'].append(reshape_data(RH[:, :5]))
                data_dictNP['A']['LL'].append(reshape_data(LL[:, :5]))
                data_dictNP['A']['RL'].append(reshape_data(RL[:, :5]))

        elif filename[9] == 'B':
            if filename[10]=='P':
                data_dictP['B']['LH'].append(reshape_data(LH[:, :5]))
                data_dictP['B']['RH'].append(reshape_data(RH[:, :5]))
                data_dictP['B']['LL'].append(reshape_data(LL[:, :5]))
                data_dictP['B']['RL'].append(reshape_data(RL[:, :5]))
            else:
                data_dictNP['B']['LH'].append(reshape_data(LH[:, :5]))
                data_dictNP['B']['RH'].append(reshape_data(RH[:, :5]))
                data_dictNP['B']['LL'].append(reshape_data(LL[:, :5]))
                data_dictNP['B']['RL'].append(reshape_data(RL[:, :5]))


for key in data_dictP:
    for sub_key in data_dictP[key]:
        if data_dictP[key][sub_key]:
            data_dictP[key][sub_key] = np.stack(data_dictP[key][sub_key])
        else:
            data_dictP[key][sub_key] = np.zeros((0, 2400, 5))


def pad_array_to_shape(arr, target_shape):
    arr = np.asarray(arr)
    if arr.dtype.kind in {'U', 'S', 'O'}:
        arr = np.where(arr == ' ', 0, arr)
        arr = arr.astype(float)
    current_shape = arr.shape
    padded_array = np.zeros(target_shape)
    rows = min(current_shape[0], target_shape[0])
    cols = min(current_shape[1], target_shape[1])
    padded_array[:rows, :cols] = arr[:rows, :cols]

    return padded_array

target_shape = (2400, 5)

for key in data_dictNP:
    for sub_key in data_dictNP[key]:
        if data_dictNP[key][sub_key]:
            padded_arrays = [pad_array_to_shape(arr, target_shape) for arr in data_dictNP[key][sub_key]]
            data_dictNP[key][sub_key] = np.stack(padded_arrays)
        else:
            data_dictNP[key][sub_key] = np.zeros((0, *target_shape))

# for key in data_dictNP:
#     for sub_key in data_dictNP[key]:
#         if data_dictNP[key][sub_key]:
#             data_dictNP[key][sub_key] = np.stack(data_dictNP[key][sub_key])
#         else:
#             data_dictNP[key][sub_key] = np.zeros((0, 2400, 5))

# for key in data_dictNP:
#     for sub_key in data_dictNP[key]:
#         try:
#             if data_dictNP[key][sub_key]:
#                 data_dictNP[key][sub_key] = np.stack(data_dictNP[key][sub_key])
#             else:
#                 data_dictNP[key][sub_key] = np.zeros((0, 2400, 5))
#         except ValueError as e:
#             print(f"Error occurred in key: {key}, sub_key: {sub_key}")
#             # print(f"Data: {data_dictNP[key][sub_key]}")
#             print(f"Error message: {e}")


LH_all_pre_P = 1000*data_dictP['B']['LH']
RH_all_pre_P = 1000*data_dictP['B']['RH']
# LL_all_pre_P = data_dictP['B']['LL']
# RL_all_pre_P = data_dictP['B']['RL']

LH_all_post_P = 1000*data_dictP['A']['LH']
RH_all_post_P = 1000*data_dictP['A']['RH']
# LL_all_post_P = data_dictP['A']['LL']
# RL_all_post_P = data_dictP['A']['RL']


LH_all_pre_NP = 1000*data_dictNP['B']['LH']
RH_all_pre_NP = 1000*data_dictNP['B']['RH']
# LL_all_pre_NP = data_dictNP['B']['LL']
# RL_all_pre_NP = data_dictNP['B']['RL']

LH_all_post_NP = 1000*data_dictNP['A']['LH']
RH_all_post_NP = 1000*data_dictNP['A']['RH']
# LL_all_post_NP = data_dictNP['A']['LL']
# RL_all_post_NP = data_dictNP['A']['RL']

x=plot_median_of_means(LH_all_pre_P, RH_all_pre_P)
(np.array(x)).tofile('p_pre.csv', sep=',')
x=plot_median_of_means(LH_all_post_P, RH_all_post_P)
(np.array(x)).tofile('p_post.csv', sep=',')
x=plot_median_of_means(LH_all_post_NP, RH_all_post_NP)
(np.array(x)).tofile('np_post.csv', sep=',')
x=plot_median_of_means(LH_all_pre_NP, RH_all_pre_NP)
(np.array(x)).tofile('np_pre.csv', sep=',')

x=plot_median_of_std(LH_all_pre_P, RH_all_pre_P)
(np.array(x)).tofile('p_pre_std.csv', sep=',')
x=plot_median_of_std(LH_all_post_P, RH_all_post_P)
(np.array(x)).tofile('p_post_std.csv', sep=',')
x=plot_median_of_std(LH_all_post_NP, RH_all_post_NP)
(np.array(x)).tofile('np_post_std.csv', sep=',')
x=plot_median_of_std(LH_all_pre_NP, RH_all_pre_NP)
(np.array(x)).tofile('np_pre_std.csv', sep=',')

# plot_state_means(LH_all_pre_NP, RH_all_pre_NP)
# flattened_LH_all_pre_P= flatten_3d_to_2d_col(LH_all_pre_P)
# flattened_LH_all_pre_NP= flatten_3d_to_2d_col(LH_all_pre_NP)
# flattened_RH_all_pre_P= flatten_3d_to_2d_col(RH_all_pre_P)
# flattened_RH_all_pre_NP= flatten_3d_to_2d_col(RH_all_pre_NP)
# flattened_LH_all_post_P= flatten_3d_to_2d_col(LH_all_post_P)
# flattened_LH_all_post_NP= flatten_3d_to_2d_col(LH_all_post_NP)
# flattened_RH_all_post_P= flatten_3d_to_2d_col(RH_all_post_P)
# flattened_RH_all_post_NP= flatten_3d_to_2d_col(RH_all_post_NP)

# plot_data(flattened_RH_all_pre_NP)
# print(flattened_LH_all_pre_P[0,:])




# plot_data(LH_all_pre, RH_all_pre, LL_all_pre, RL_all_pre)



# means_LH_all_pre_P, std_devs_LH_all_pre_P = calculate_statistics(LH_all_pre_P)
# means_LH_all_pre_NP, std_devs_LH_all_pre_NP = calculate_statistics(LH_all_pre_NP)
# means_RH_all_pre_P, std_devs_RH_all_pre_P = calculate_statistics(RH_all_pre_P)
# means_RH_all_pre_NP, std_devs_RH_all_pre_NP = calculate_statistics(RH_all_pre_NP)
# means_LH_all_post_P, std_devs_LH_all_post_P = calculate_statistics(LH_all_post_P)
# means_LH_all_post_NP, std_devs_LH_all_post_NP = calculate_statistics(LH_all_post_NP)
# means_RH_all_post_P, std_devs_RH_all_post_P = calculate_statistics(RH_all_post_P)
# means_RH_all_post_NP, std_devs_RH_all_post_NP = calculate_statistics(RH_all_post_NP)

# means_LH_all_pre_P = np.mean(flattened_LH_all_pre_P, axis=1)
# means_LH_all_pre_NP = np.mean(flattened_LH_all_pre_NP, axis=1)
# means_RH_all_pre_P = np.mean(flattened_RH_all_pre_P, axis=1)
# means_RH_all_pre_NP = np.mean(flattened_RH_all_pre_NP, axis=1)
# means_LH_all_post_P = np.mean(flattened_LH_all_post_P, axis=1)
# means_LH_all_post_NP = np.mean(flattened_LH_all_post_NP, axis=1)
# means_RH_all_post_P = np.mean(flattened_RH_all_post_P, axis=1)
# means_RH_all_post_NP = np.mean(flattened_RH_all_post_NP, axis=1)
# print(means_LH_all_pre_NP)
#
# for i in range(flattened_LH_all_pre_P.shape[0]):
#     flattened_LH_all_pre_P[i, :] -= means_LH_all_pre_P[i]
#
# for i in range(flattened_LH_all_pre_NP.shape[0]):
#     flattened_LH_all_pre_NP[i, :] -= means_LH_all_pre_NP[i]
#
# for i in range(flattened_RH_all_pre_P.shape[0]):
#     flattened_RH_all_pre_P[i, :] -= means_RH_all_pre_P[i]
#
# for i in range(flattened_RH_all_pre_NP.shape[0]):
#     flattened_RH_all_pre_NP[i, :] -= means_RH_all_pre_NP[i]
#
# for i in range(flattened_LH_all_post_P.shape[0]):
#     flattened_LH_all_post_P[i, :] -= means_LH_all_post_P[i]
#
# for i in range(flattened_LH_all_post_NP.shape[0]):
#     flattened_LH_all_post_NP[i, :] -= means_LH_all_post_NP[i]
#
# for i in range(flattened_RH_all_post_P.shape[0]):
#     flattened_RH_all_post_P[i, :] -= means_RH_all_post_P[i]
#
# for i in range(flattened_RH_all_post_NP.shape[0]):
#     flattened_RH_all_post_NP[i, :] -= means_RH_all_post_NP[i]
#
# deviation_pre_P = np.vstack((flattened_LH_all_pre_P, flattened_RH_all_pre_P))
# deviation_pre_NP = np.vstack((flattened_LH_all_pre_NP, flattened_RH_all_pre_NP))
# deviation_post_P = np.vstack((flattened_LH_all_post_P, flattened_RH_all_post_P))
# deviation_post_NP = np.vstack((flattened_LH_all_post_NP, flattened_RH_all_post_NP))
# plot_data(deviation_post_P)

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

# LH_all_pre_normalised=flatten_3d_to_2d(LH_all_pre)
# LH_all_pre_raw=LH_all_pre_normalised
# for i in range(0,len(means_LH_all_pre)):
#   LH_all_pre_normalised[i]=z_normalize(LH_all_pre_normalised[i],means_LH_all_pre[i],std_devs_LH_all_pre[i])
#
# RH_all_pre_normalised=flatten_3d_to_2d(RH_all_pre)
# RH_all_pre_raw=RH_all_pre_normalised
# for i in range(0,len(means_RH_all_pre)):
#   RH_all_pre_normalised[i]=z_normalize(RH_all_pre_normalised[i],means_RH_all_pre[i],std_devs_RH_all_pre[i])
#
# LH_all_post_normalised=flatten_3d_to_2d(LH_all_post)
# LH_all_post_raw=LH_all_post_normalised
# for i in range(0,len(means_LH_all_post)):
#   LH_all_post_normalised[i]=z_normalize(LH_all_post_normalised[i],means_LH_all_post[i],std_devs_LH_all_post[i])
#
# RH_all_post_normalised=flatten_3d_to_2d(RH_all_post)
# RH_all_post_raw=RH_all_post_normalised
# for i in range(0,len(means_RH_all_post)):
#   RH_all_post_normalised[i]=z_normalize(RH_all_post_normalised[i],means_RH_all_post[i],std_devs_RH_all_post[i])
#
#
#
#
# normalised_variances_pre_LH = []
# normalised_kurtoses_pre_LH = []
# for array in LH_all_pre_normalised:
#     var, kurt = process_batches_for_normalised(array)
#     normalised_variances_pre_LH.append(var)
#     normalised_kurtoses_pre_LH.append(kurt)
# normalised_variances_pre_LH = np.array(normalised_variances_pre_LH)
# normalised_kurtoses_pre_LH = np.array(normalised_kurtoses_pre_LH)
#
#
# normalised_variances_pre_RH = []
# normalised_kurtoses_pre_RH = []
# for array in RH_all_pre_normalised:
#     var, kurt = process_batches_for_normalised(array)
#     normalised_variances_pre_RH.append(var)
#     normalised_kurtoses_pre_RH.append(kurt)
# normalised_variances_pre_RH = np.array(normalised_variances_pre_RH)
# normalised_kurtoses_pre_RH = np.array(normalised_kurtoses_pre_RH)
#
#
# raw_means_pre_LH=[]
# raw_stddev_pre_LH=[]
# raw_variance_pre_LH=[]
# raw_skewness_pre_LH=[]
# for array in LH_all_pre_raw:
#     mean, std, var, skew = process_batches_raw(array)
#     raw_means_pre_LH.append(mean)
#     raw_stddev_pre_LH.append(std)
#     raw_variance_pre_LH.append(var)
#     raw_skewness_pre_LH.append(skew)
# raw_means_pre_LH = np.array(raw_means_pre_LH)
# raw_stddev_pre_LH = np.array(raw_stddev_pre_LH)
# raw_variance_pre_LH=np.array(raw_variance_pre_LH)
# raw_skewness_pre_LH=np.array(raw_skewness_pre_LH)
#
#
# raw_means_pre_RH=[]
# raw_stddev_pre_RH=[]
# raw_variance_pre_RH=[]
# raw_skewness_pre_RH=[]
# for array in RH_all_pre_raw:
#     mean, std, var, skew = process_batches_raw(array)
#     raw_means_pre_RH.append(mean)
#     raw_stddev_pre_RH.append(std)
#     raw_variance_pre_RH.append(var)
#     raw_skewness_pre_RH.append(skew)
# raw_means_pre_RH = np.array(raw_means_pre_RH)
# raw_stddev_pre_RH = np.array(raw_stddev_pre_RH)
# raw_variance_pre_RH=np.array(raw_variance_pre_RH)
# raw_skewness_pre_RH=np.array(raw_skewness_pre_RH)
#
#
#
# normalised_variances_post_LH = []
# normalised_kurtoses_post_LH = []
# for array in LH_all_post_normalised:
#     var, kurt = process_batches_for_normalised(array)
#     normalised_variances_post_LH.append(var)
#     normalised_kurtoses_post_LH.append(kurt)
# normalised_variances_post_LH = np.array(normalised_variances_post_LH)
# normalised_kurtoses_post_LH = np.array(normalised_kurtoses_post_LH)
#
#
# normalised_variances_post_RH = []
# normalised_kurtoses_post_RH = []
# for array in RH_all_post_normalised:
#     var, kurt = process_batches_for_normalised(array)
#     normalised_variances_post_RH.append(var)
#     normalised_kurtoses_post_RH.append(kurt)
# normalised_variances_post_RH = np.array(normalised_variances_post_RH)
# normalised_kurtoses_post_RH = np.array(normalised_kurtoses_post_RH)
#
#
# raw_means_post_LH=[]
# raw_stddev_post_LH=[]
# raw_variance_post_LH=[]
# raw_skewness_post_LH=[]
# for array in LH_all_post_raw:
#     mean, std, var, skew = process_batches_raw(array)
#     raw_means_post_LH.append(mean)
#     raw_stddev_post_LH.append(std)
#     raw_variance_post_LH.append(var)
#     raw_skewness_post_LH.append(skew)
# raw_means_post_LH = np.array(raw_means_post_LH)
# raw_stddev_post_LH = np.array(raw_stddev_post_LH)
# raw_variance_post_LH=np.array(raw_variance_post_LH)
# raw_skewness_post_LH=np.array(raw_skewness_post_LH)
#
#
# raw_means_post_RH=[]
# raw_stddev_post_RH=[]
# raw_variance_post_RH=[]
# raw_skewness_post_RH=[]
# for array in RH_all_post_raw:
#     mean, std, var, skew = process_batches_raw(array)
#     raw_means_post_RH.append(mean)
#     raw_stddev_post_RH.append(std)
#     raw_variance_post_RH.append(var)
#     raw_skewness_post_RH.append(skew)
# raw_means_post_RH = np.array(raw_means_post_RH)
# raw_stddev_post_RH = np.array(raw_stddev_post_RH)
# raw_variance_post_RH=np.array(raw_variance_post_RH)
# raw_skewness_post_RH=np.array(raw_skewness_post_RH)
