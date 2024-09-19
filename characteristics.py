import numpy as np
import pandas as pd


def calculate_statistics(data_3d):
    data_3d = np.array(pd.to_numeric(data_3d.flatten(), errors='coerce')).reshape(data_3d.shape)


    means = []
    for i in range(data_3d.shape[0]):
        data_without_nans = np.nan_to_num(data_3d[i], nan=0.0)
        mean_value = np.sum(data_without_nans) / (2400 * 5)  # Sum and divide by 2400*5
        means.append(mean_value)

    std_devs = []

    for i in range(data_3d.shape[0]):
        data_without_nans = np.nan_to_num(data_3d[i], nan=0.0)
        mean_value = np.sum(data_without_nans) / (2400 * 5)
        squared_diffs = (data_without_nans - mean_value) ** 2
        std_dev_value = np.sqrt(np.sum(squared_diffs) / (2400 * 5))
        std_devs.append(std_dev_value)
    # std_devs = np.nanstd(data_3d, axis=1)

    return means, std_devs



