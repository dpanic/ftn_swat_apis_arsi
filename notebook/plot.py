import sys
import numpy as np
import matplotlib.pyplot as plt


def process(obj):
    """
    Main function for plotting
    """

    file_loc = obj["file_loc"]
    df_custom = obj["df"]
    total_columns = obj["total_columns"]
    time_start = obj["time_start"]
    time_delta = obj["time_delta"]
    idx_start = obj["idx_start"]
    idx_end = obj["idx_end"]
    anomalies = obj["anomalies"]
    x = obj["x"]

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

    with plt.style.context("bmh"):
        _, axs = plt.subplots(total_columns, 1, figsize=(80, 150))

        anomaly_label_indexes = {}

        for i in range(total_columns):
            axs[i].plot(x, df_custom.iloc[idx_start:idx_end, i+1], label=df_custom.columns[i+1], color=color_plot)

            axs[i].set_xlabel("Time", fontdict=font)
            axs[i].set_ylabel("Value", fontdict=font)
            axs[i].legend(loc="upper left", prop=font_legend)
            labels = axs[i].get_xticklabels() + axs[i].get_yticklabels()
            [ label.set_fontname(font_family) for label in labels ]

            for anomaly in anomalies:
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