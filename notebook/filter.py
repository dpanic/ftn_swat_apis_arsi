import numpy as np
import pandas as pd

def get_stage(input):
    """
        gets stage from input
    """
    
    number = ""
    for i in input:
        if i not in ["0","1","2","3","4","5","6","7","8","9"]:
            continue
        number += i

    out = "P%s" %(number[0])
    return out


def load_df(df_file_loc, columns):
    """
    load df by columns
    """

    columns.insert(0, "Timestamp")
    # print(columns)

    df_out = pd.read_csv(df_file_loc, usecols=columns)
    # print(df_out.shape)
    # print(df_out.head())

    return df_out


def get_times(anomalies, filter_by=None):
    """
        extract time from anomalies based on filter
    """
    times = []

    filter_tag = ""
    if type(filter_by) == list:
        filter_by.sort()
        filter_tag = "_".join(filter_by)

    filtered_anomalies = []
    for anomaly in anomalies:
        is_hit = False
        if filter_by == None:
            is_hit = True
        else:
            if type(filter_by) == list:
                tag = "_".join(anomaly["attack_points"])
                if filter_tag == tag:
                    is_hit = True
            else:
                if filter_by in anomaly["attack_stages"]:
                    is_hit = True

                if filter_by in anomaly["attack_points"]:
                    is_hit = True

        if is_hit:
            time_start = anomaly["time_start"]
            time_end = anomaly["time_end"]
            times.append(np.array(time_start, dtype=np.datetime64))
            times.append(np.array(time_end, dtype=np.datetime64))

            filtered_anomalies.append(anomaly)


    times.sort()
    time_start = times[0]
    time_end = times[len(times)-1]

    return [ time_start, time_end, filtered_anomalies ]