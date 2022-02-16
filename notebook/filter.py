import numpy as np

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



def get_times(anomalies, filter_by=None):
    """
        extract time from anomalies based on filter
    """
    times = []
    for anomaly in anomalies:
        time_start = anomaly["time_start"]
        time_end = anomaly["time_end"]

        is_hit = False
        if filter_by == None:
            is_hit = True
        else:
            if filter_by in anomaly["attack_stages"]:
                is_hit = True

            if filter_by in anomaly["attack_points"]:
                is_hit = True

        if is_hit:
            times.append(np.array(time_start, dtype=np.datetime64))
            times.append(np.array(time_end, dtype=np.datetime64))

    times.sort()
    time_start = times[0]
    time_end = times[len(times)-1]

    return [ time_start, time_end ]