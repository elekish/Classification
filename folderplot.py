import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# def plot_data(matrix):
#     time_per_row = np.arange(0, 12000, 1)  # Time vector for 2400 rows
#     matrix=np.array(matrix)
#     plt.figure(figsize=(20,8))
#     for i in range(matrix.shape[0]):
#       plt.plot(np.array(matrix[i,:]))
#
#     # for i, row in enumerate(MATRIX):
#     #     plt.scatter(time_per_row, row)
#
#     # Adding labels and title
#     plt.title('LH_B_P')
#     plt.xlabel('TIME')
#     plt.ylabel('AMPLITUDE')
#     plt.legend()
#     plt.show()
#
#     # Plot LH data
#     # for i in range(LH_all_pre.shape[0]):
#     #     axs[0].plot(time_per_row, LH_all_pre[i, :, 0])
#     #
#     # axs[0].set_title("LH Data - Time vs Amplitude")
#     # axs[0].set_xlabel("Time (minutes)")
#     # axs[0].set_ylabel("Amplitude")
#     # axs[0].legend()
#     # axs[0].grid(True)
#     #
#     # # Plot RH data
#     # for i in range(RH_all_pre.shape[0]):
#     #     axs[1].plot(time_per_row, RH_all_pre[i, :, 0])
#     #
#     # axs[1].set_title("RH Data - Time vs Amplitude")
#     # axs[1].set_xlabel("Time (minutes)")
#     # axs[1].set_ylabel("Amplitude")
#     # axs[1].legend()
#     # axs[1].grid(True)
#     #
#     # # Plot LL data
#     # for i in range(LL_all_pre.shape[0]):
#     #     axs[2].plot(time_per_row, LL_all_pre[i, :, 0])
#     #
#     # axs[2].set_title("LL Data - Time vs Amplitude")
#     # axs[2].set_xlabel("Time (minutes)")
#     # axs[2].set_ylabel("Amplitude")
#     # axs[2].legend()
#     # axs[2].grid(True)
#     #
#     # # Plot RL data
#     # for i in range(RL_all_pre.shape[0]):
#     #     axs[3].plot(time_per_row, RL_all_pre[i, :, 0])
#     #
#     # axs[3].set_title("RL Data - Time vs Amplitude")
#     # axs[3].set_xlabel("Time (minutes)")
#     # axs[3].set_ylabel("Amplitude")
#     # axs[3].legend()
#     # axs[3].grid(True)
#
#     plt.tight_layout(pad=2.0)
#     plt.show()



def plot_data(matrix, save_path='C:\\Users\\Ishita Biswas\\OneDrive\\Pictures\\plot\\RH_all_pre_NP.jpg'):
    sns.set(style="whitegrid")
    matrix = np.array(matrix)

    plt.figure(figsize=(20, 10))
    palette = sns.color_palette("husl", matrix.shape[0])
    for i in range(matrix.shape[0]):
        plt.plot(matrix[i, :], color=palette[i], linewidth=1.0)
    plt.title('RH_pre_NP', fontsize=16)
    plt.xlabel('TIME', fontsize=14)
    plt.ylabel('AMPLITUDE', fontsize=14)
    plt.legend(title="Data Rows", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

    plt.tight_layout()
    plt.savefig(save_path, format='jpg', dpi=300)
    plt.show()
