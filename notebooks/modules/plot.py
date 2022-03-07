import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams["figure.max_open_warning"] = 0

import warnings
warnings.filterwarnings("ignore")

def process(obj):
    """
    Main function for plotting
    """

    name = obj["name"]

    file_loc = obj["file_loc"]
    if os.path.exists(file_loc):
        print("BEFORE = %s" %(file_loc))
        file_loc = file_loc.split(".png")[0]

        for it in range(1, 100):
            file_loc_test = file_loc + "_%d.png" %(it)
            if os.path.exists(file_loc_test) == False:
                break

        file_loc = file_loc_test
        print("AFTER = %s" %(file_loc))



    log_prefix = obj["log_prefix"]
    df_custom = obj["df"]
    time_start = obj["time_start"]
    time_delta = obj["time_delta"]
    idx_start = obj["idx_start"]
    idx_end = obj["idx_end"]
    filtered_anomalies = obj["filtered_anomalies"]
    title = obj["title"]
    x = obj["x"]
    total_columns = int(df_custom.shape[1])-1
 
    font_family = "verdana"
    color_anomaly = "darkred"
    color_plot = "#2f83e4"
    color_default = "#444444"

    font = {
        "color": color_default, 
        "size": 12, 
        "family": font_family
    }
    font_legend = {
        "size": 12, 
        "family": font_family
    }

    print("%sPlotting %s" %(log_prefix, file_loc))


    with plt.style.context("bmh"):
        fig_y = 5 * total_columns
        fig_x = 160

        # fix for broken plotting if 1 subplot
        if total_columns == 1:
            fig, axs = plt.subplots(2, 1, figsize=(fig_x, fig_y))
            axs.flat[-1].set_visible(False)
        else:
            fig, axs = plt.subplots(total_columns, 1, figsize=(fig_x, fig_y))
           
        if title != "":
            fig.suptitle(title, fontsize=96)
        anomaly_label_indexes = {}
 

        for i in range(total_columns):
            axs[i].plot(x, df_custom.iloc[idx_start:idx_end, i+1], label=df_custom.columns[i+1], color=color_plot, linewidth=2)

            axs[i].set_xlabel("Time", fontdict=font)
            axs[i].set_ylabel("Value", fontdict=font)
            axs[i].legend(loc="upper left", prop=font_legend)
            labels = axs[i].get_xticklabels() + axs[i].get_yticklabels()
            for label in labels:
                label.set_fontname(font_family) 

            for anomaly in filtered_anomalies:
                if df_custom.columns[i+1] not in anomaly["attack_points"]:
                    continue

                anomaly_idx = anomaly["time_start"] + np.arange(0, int((anomaly["time_end"] - anomaly["time_start"])/time_delta), 1)

                anomaly_idx_start = int((anomaly["time_start"] - time_start)/time_delta)
                anomaly_idx_end = int((anomaly["time_end"] - time_start)/time_delta)

                loc = df_custom.iloc[idx_start + anomaly_idx_start:idx_start + anomaly_idx_end, i+1]
                
                # if we haven't colored it yet
                if df_custom.columns[i+1] not in anomaly_label_indexes:
                    label = '{} Anomaly'.format(df_custom.columns[i+1])

                    axs[i].plot(anomaly_idx, loc, label=label, color=color_anomaly, linewidth=6, alpha=0.8)

                    axs[i].legend(loc="upper left", prop=font_legend)

                    anomaly_label_indexes[df_custom.columns[i+1]] = ""
                else:
                    axs[i].plot(anomaly_idx, loc, color=color_anomaly, linewidth=6, alpha=0.8)

    plt.savefig(file_loc)
    if os.path.exists(file_loc) == False:
        print("%sFailed plotting %s" %(log_prefix, file_loc))
