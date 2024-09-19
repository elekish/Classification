import os
import numpy as np
import pandas as pd
from tkinter import filedialog
from plot import plot_data

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

print("Do you want to plot the data?")
answer=input()
if answer.lower()=="yes":
    plot_data(LH_all_pre, RH_all_pre, LL_all_pre, RL_all_pre)

