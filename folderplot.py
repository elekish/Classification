import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from matplotlib.widgets import CheckButtons


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



def plot_data(matrix, save_path='C:\\Users\\PC1\\Pictures\\plot\\deviation_post_P.jpg'):
    sns.set(style="whitegrid")
    matrix = np.array(matrix)

    plt.figure(figsize=(20, 10))
    palette = sns.color_palette("husl", matrix.shape[0])
    for i in range(matrix.shape[0]):
        plt.plot(matrix[i, :], color=palette[i], linewidth=1.0)
    plt.title('deviation_post_P', fontsize=16)
    plt.xlabel('TIME', fontsize=14)
    plt.ylabel('AMPLITUDE', fontsize=14)
    plt.legend(title="Data Rows", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)

    plt.tight_layout()
    plt.savefig(save_path, format='jpg', dpi=300)
    plt.show()

# def plot_data(matrix, save_path='C:\\Users\\PC1\\Pictures\\plot\\deviation_post_NP.jpg'):
#     sns.set(style="whitegrid")
#     matrix = np.array(matrix)
#     fig, ax = plt.subplots(figsize=(20, 10))
#     palette = sns.color_palette("husl", matrix.shape[0])
#     lines = []
#     for i in range(matrix.shape[0]):
#         line, = ax.plot(matrix[i, :], color=palette[i], linewidth=1.0, label=f'Line {i + 1}')
#         lines.append(line)
#     ax.set_title('deviation_post_NP', fontsize=16)
#     ax.set_xlabel('TIME', fontsize=14)
#     ax.set_ylabel('AMPLITUDE', fontsize=14)
#     labels = [f'Line {i + 1}' for i in range(matrix.shape[0])]
#     check = CheckButtons(ax=plt.axes([0.8, 0.4, 0.1, 0.15]), labels=labels, actives=[True] * len(labels))
#
#     for i, line in enumerate(lines):
#         check.labels[i].set_color(line.get_color())
#     def func(label):
#         index = labels.index(label)
#         lines[index].set_visible(not lines[index].get_visible())
#         plt.draw()
#
#     check.on_clicked(func)
#
#     plt.tight_layout()
#     # plt.savefig(save_path, format='jpg', dpi=300)
#     plt.show()


def plot_state_means(LH_all_pre_P, RH_all_pre_P, save_path='C:\\Users\\PC1\\Pictures\\plot\\pre_P.jpg'):

    def extract_state_data(combined_LH, combined_RH):
        states = {}
        num_samples = combined_LH.shape[0]  # Number of samples
        num_states = combined_LH.shape[2]    # Number of states (5 in this case)

        for i in range(num_samples):  # Iterate through the samples
            for j in range(num_states):  # Iterate through the states
                state_name = f'State {j + 1}'
                if state_name not in states:
                    states[state_name] = []
                states[state_name].append(combined_LH[i, :, j])  # Append LH data
                states[state_name].append(combined_RH[i, :, j])  # Append RH data

        return states


    state_data_pre_P = extract_state_data(LH_all_pre_P, RH_all_pre_P)
    print(state_data_pre_P)
    means = {}
    for state_name, data in state_data_pre_P.items():
        means[state_name] = [np.mean(data_array) for data_array in data]
    box_data = {state: [] for state in means.keys()}
    for state in means.keys():
        box_data[state].extend(means[state])
    # plt.figure(figsize=(15, 10))
    # sns.boxplot(data=[box_data[state] for state in box_data], palette="Set3")
    # plt.xticks(ticks=np.arange(len(box_data)), labels=box_data.keys())
    # plt.title('Box Plots of Means for Each State')
    # plt.xlabel('States')
    # plt.ylabel('Mean Values')
    # # plt.legend(['Pre P', 'Post P', 'Pre NP', 'Post NP'], loc='upper right')
    # plt.savefig(save_path, format='jpg', dpi=300)
    # plt.tight_layout()
    # plt.show()

# Example usage:
# if __name__ == "__main__":
#     plot_state_means(LH_all_pre_P, RH_all_pre_P, LH_all_post_P, RH_all_post_P,
#                      LH_all_pre_NP, RH_all_pre_NP, LH_all_post_NP, RH_all_post_NP)

