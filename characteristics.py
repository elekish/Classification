import numpy as np
import pandas as pd
from scipy.stats import kurtosis,skew


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

def flatten_3d_to_2d(array_3d):
    if array_3d.ndim != 3:
        raise ValueError("Input array must be 3D")
    flattened_arrays = np.array([array_3d[i].flatten() for i in range(array_3d.shape[0])])

    return flattened_arrays


def flatten_3d_to_2d_col(array_3d):
    if array_3d.ndim != 3:
        raise ValueError("Input array must be 3D")
    n_slices, rows, cols = array_3d.shape
    flattened_arrays = []
    for i in range(n_slices):
        array_2d = array_3d[i]
        flattened_array = array_2d.T.flatten()  # Transpose to get columns first, then flatten
        flattened_arrays.append(flattened_array)

    return np.array(flattened_arrays)

def z_normalize(array_1d, mean, std_dev):
    return (array_1d - mean) / std_dev


def calculate_normalized_variance_and_kurtosis(data):
    data = np.asarray(data, dtype=float)  # Convert to float, handles None
    data = np.nan_to_num(data)
    normalized_variance = np.var(data, ddof=1)  # Sample variance
    kurt_value = kurtosis(data)
    return normalized_variance, kurt_value

def process_batches_for_normalised(array_1d, batch_size=200):
    num_batches = len(array_1d) // batch_size
    variances = []
    kurtoses = []

    for i in range(num_batches):
        batch = array_1d[i * batch_size:(i + 1) * batch_size]
        var, kurt = calculate_normalized_variance_and_kurtosis(batch)
        variances.append(var)
        kurtoses.append(kurt)

    return np.array(variances), np.array(kurtoses)

def calculate_statistics_in_batches(data):
    # Ensure data is numeric and replace NaN/None with 0
    data = np.asarray(data, dtype=float)  # Convert to float, handles None
    data = np.nan_to_num(data)  # Replace NaN with 0

    # Calculate mean, standard deviation, variance, and skewness
    mean_value = np.mean(data)
    std_dev_value = np.std(data, ddof=1)  # Sample std deviation
    variance_value = np.var(data, ddof=1)  # Sample variance
    skewness_value = skew(data)

    return mean_value, std_dev_value, variance_value, skewness_value

def process_batches_raw(array_1d, batch_size=200):
    num_batches = len(array_1d) // batch_size
    means = []
    stddevs=[]
    variances=[]
    skews=[]

    for i in range(num_batches):
        batch = array_1d[i * batch_size:(i + 1) * batch_size]
        mm, sstd, varr, skewness = calculate_statistics_in_batches(batch)
        variances.append(varr)
        means.append(mm)
        stddevs.append(sstd)
        skews.append(skewness)


    return np.array(means), np.array(stddevs), np.array(variances), np.array(skews)
