import sys
import numpy as np
import pandas as pd

import filter
import normalize

def anomalies(file_loc):
    """
        load and process anomalies
    """
    stages = {}
    anomalies = []

    df = pd.read_excel(file_loc)


    for index, row in df.iterrows():
        try:
            # skip if there is no attack
            try:
                tmp = int(row["Attack #"])
            except:
                continue

            # skip if there is no attack
            attack_point = str(row["Attack Point"])
            attack_point = attack_point.replace(";", ",")
            tmp = attack_point.split(",")
            if row["Attack Point"] == "No Physical Impact Attack":
                continue

            # extract attack start time
            time_start, time_start_date = normalize.date_time(row["Start Time"])

            # extract attack end time
            time_end = str(row["End Time"])
            time_end = "%sT%s" %(time_start_date, time_end)

            # extract attack points
            attack_points = {}
            attack_stages = {}
            for i in tmp:
                i = i.strip(" ")
                i = i.upper()
                i = i.replace("-", "")
                attack_points[i] = ""
                stage = filter.get_stage(i)
                attack_stages[stage] = ""

                if stage not in stages.keys():
                    stages[stage] = {}
                stages[stage][i] = ""


            attack_points = list(attack_points.keys())
            attack_points.sort()

            attack_stages = list(attack_stages.keys())
            attack_stages.sort()
            

            print(attack_points, attack_stages)
            # define anomaly
            anomaly = {
                "time_start": np.array(time_start, dtype=np.datetime64),
                "time_end": np.array(time_end, dtype=np.datetime64),
                "attack_points": attack_points,
                "attack_stages": attack_stages,
            }

            anomalies.append(anomaly)
        except:
            print("Error: %s" %(str(sys.exc_info())))
            print("Row value: %s" %(row))
            print("Index: %d" %(index))

    # sort fields
    for key in stages.keys():
        stages[key] = list(stages[key].keys())
        print(key, stages[key])

    df.reset_index()
    return [ stages, anomalies ]
