import numpy as np
import matplotlib.pyplot as plt

def plot_data(LH_all_pre, RH_all_pre, LL_all_pre, RL_all_pre):
    time_per_row = np.arange(0, 2400, 1)

    fig, axs = plt.subplots(4, 1, figsize=(12, 24))

    # Plot LH Data
    axs[0].plot(time_per_row, LH_all_pre[:, 0])
    axs[0].set_title("LH Data - Time vs Amplitude")
    axs[0].set_xlabel("Time (minutes)")
    axs[0].set_ylabel("Amplitude(in V)")
    axs[0].grid(True)

    # Plot RH Data
    axs[1].plot(time_per_row, RH_all_pre[:, 0])
    axs[1].set_title("RH Data - Time vs Amplitude")
    axs[1].set_xlabel("Time (minutes)")
    axs[1].set_ylabel("Amplitude (in V)")
    axs[1].grid(True)

    # Plot LL Data
    axs[2].plot(time_per_row, LL_all_pre[:, 0])
    axs[2].set_title("LL Data - Time vs Amplitude")
    axs[2].set_xlabel("Time (minutes)")
    axs[2].set_ylabel("Amplitude (in V)")
    axs[2].grid(True)

    # Plot RL Data
    axs[3].plot(time_per_row, RL_all_pre[:, 0])
    axs[3].set_title("RL Data - Time vs Amplitude")
    axs[3].set_xlabel("Time (minutes)")
    axs[3].set_ylabel("Amplitude (in V)")
    axs[3].grid(True)

    plt.tight_layout(pad=2.0)
    plt.show()
