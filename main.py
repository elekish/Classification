import os
import numpy as np
import scipy.io as sio
import pandas as pd
from tkinter import filedialog
import matplotlib.pyplot as plt

filepaths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx")])

LH_all_pre = np.zeros((2400, 0))
RH_all_pre = np.zeros((2400, 0))
LL_all_pre = np.zeros((2400, 0))
RL_all_pre = np.zeros((2400, 0))

LH_all_post = np.zeros((2400, 0))
RH_all_post = np.zeros((2400, 0))
LL_all_post = np.zeros((2400, 0))
RL_all_post = np.zeros((2400, 0))



def load_and_extract_data(filepath):
    dataall = pd.read_excel(filepath, sheet_name=2).to_numpy()

    LH = dataall[:, 1::7]
    RH = dataall[:, 2::7]
    LL = dataall[:, 3::7]
    RL = dataall[:, 4::7]


    LH = LH[2:, :]
    RH = RH[2:, :]
    LL = LL[2:, :]
    RL = RL[2:, :]

    return LH, RH, LL, RL



for filepath in filepaths:
    filename = os.path.basename(filepath)
    # print(filename)

    if filename[9] == 'A' :  #and filename[18:21] == 'data':
        LH, RH, LL, RL = load_and_extract_data(filepath)
        print(LH)

        LH_all_pre = np.hstack((LH_all_pre, LH[:, :5]))
        RH_all_pre = np.hstack((RH_all_pre, RH[:, :5]))
        LL_all_pre = np.hstack((LL_all_pre, LL[:, :5]))
        RL_all_pre = np.hstack((RL_all_pre, RL[:, :5]))


    elif filename[9] == 'B' : #and filename[18:21] == 'data':
        LH, RH, LL, RL = load_and_extract_data(filepath)


        LH_all_post = np.hstack((LH_all_post, LH[:, :5]))
        RH_all_post = np.hstack((RH_all_post, RH[:, :5]))
        LL_all_post = np.hstack((LL_all_post, LL[:, :5]))
        RL_all_post = np.hstack((RL_all_post, RL[:, :5]))


time_per_row = np.arange(0, 5 * 2, 2)  #time vector size 10 mins with 2 mins interval
fig, axs = plt.subplots(4, 1, figsize=(12, 24))

for i in range(LH_all_pre.shape[0]):
    axs[0].plot(time_per_row, LH_all_pre[i, :], label=f"Row {i+1}")

axs[0].set_title("LH Data - Time vs Amplitude")
axs[0].set_xlabel("Time (minutes)")
axs[0].set_ylabel("Amplitude")
axs[0].legend()
axs[0].grid(True)


for i in range(RH_all_pre.shape[0]):
    axs[1].plot(time_per_row, RH_all_pre[i, :]) #, label=f"Row {i+1}")

axs[1].set_title("RH Data - Time vs Amplitude")
axs[1].set_xlabel("Time (minutes)")
axs[1].set_ylabel("Amplitude")
axs[1].legend()
axs[1].grid(True)


for i in range(LL_all_pre.shape[0]):
    axs[2].plot(time_per_row, LL_all_pre[i, :], label=f"Row {i+1}")

axs[2].set_title("LL Data - Time vs Amplitude")
axs[2].set_xlabel("Time (minutes)")
axs[2].set_ylabel("Amplitude")
axs[2].legend()
axs[2].grid(True)

for i in range(RL_all_pre.shape[0]):
    axs[3].plot(time_per_row, RL_all_pre[i, :], label=f"Row {i+1}")

axs[3].set_title("RL Data - Time vs Amplitude")
axs[3].set_xlabel("Time (minutes)")
axs[3].set_ylabel("Amplitude")
axs[3].legend()
axs[3].grid(True)

plt.tight_layout(pad=2.0)
plt.show()
