import os
import csv
from time import time

import pandas as pd
import modules.filter as filter
import modules.normalize as normalize


class Patterns:
    def __init__(self, precission):
        self.files = []
        self.stats = {}
        self.precission = precission


    def bootstrap(self, folder_loc):
        """
        load list of files
        """
        files = []

        total_files = 0
        total_loaded = 0
        total_skipped = 0

        for file in os.listdir(folder_loc):
            total_files += 1
            if file.endswith(".csv"):
                files.append(os.path.join(folder_loc, file))
                total_loaded += 1
            else:
                total_skipped += 1
        
        files.sort()
        self.files = files

        table = [
            [ "Total files", "Skipped", "Loaded" ],
            [ total_files, total_skipped, total_loaded ]
        ]

        return table 


    def process_all(self, anomalies, skip_first, max_process):
        """
        process file by file with anomalies
        """

        self.stats = {}

        for anomaly in anomalies:
            time_start, time_end, filtered_anomalies = filter.get_times(anomalies, anomaly["attack_points"])
            
            time_start_str = "%s" %(time_start.astype("str"))
            time_end_str = "%s" %(time_end.astype("str"))

            _, time_start_epoch, _ = normalize.date_time(time_start_str)
            _, time_end_epoch, _ = normalize.date_time(time_end_str)

            tag = "%d_%d" %(time_start_epoch, time_end_epoch)
            if tag not in self.stats.keys():
                self.stats[tag] = {
                    "anomalies": [],
                    "time_start": time_start,
                    "time_end": time_end,
                }


            for filtered_anomaly in filtered_anomalies:
                self.stats[tag]["anomalies"].append(filtered_anomaly)


        it = 1
        total_processed = 0
        for file in self.files:
            it += 1
            if skip_first > -1 and it < skip_first:
                continue

            if max_process > -1 and total_processed > max_process:
                break

            print("[ %d / %d ] processing file %s" %(it, len(self.files), file))
            yield self.process(file)
            total_processed += 1




    def process(self, file):
        """
            process file
        """

        # reading csv file
        df = pd.read_csv(file)
        names = df.columns.tolist()

        total = {
            "rows": 0,
            "attack": 0,
            "normal": 0,
            "anomalies": 0,
            "stages": 0
        }
        anomalies_unique = {}
        stages_unique = {}

        with open(file, "r") as file:
            it = 0
            for line in file:
                it += 1
                
                if it % self.precission != 0:
                    continue

                tmp = line.split(",")
                if tmp[1] == "date" and tmp[2] == "time":
                    continue

                if tmp[1].find("-") > -1:
                    ttt = tmp[1].split("-")
                    tmp[1] = "%s%s20%s" %(ttt[0], ttt[1], ttt[2])

                tmp[1] = tmp[1].replace("Jan", "/1/")
                tmp[1] = tmp[1].replace("Feb", "/2/")
                tmp[1] = tmp[1].replace("Mar", "/3/")
                tmp[1] = tmp[1].replace("Apr", "/4/")
                tmp[1] = tmp[1].replace("May", "/5/")
                tmp[1] = tmp[1].replace("Jun", "/6/")
                tmp[1] = tmp[1].replace("Jul", "/7/")
                tmp[1] = tmp[1].replace("Aug", "/8/")
                tmp[1] = tmp[1].replace("Sep", "/9/")
                tmp[1] = tmp[1].replace("Oct", "/10/")
                tmp[1] = tmp[1].replace("Nov", "/11/")
                tmp[1] = tmp[1].replace("Dec", "/12/")

                dts = tmp[1] + " " + tmp[2]
                _, timestamp_epoch, _ = normalize.date_time(dts)
                
                
                anomalies = self.get_anomalies_by_timestamp(timestamp_epoch)
                for anomaly in anomalies:
                    tag = "".join(anomaly["attack_points"])
                    anomalies_unique[tag] = ""

                    tag = "".join(anomaly["attack_stages"])
                    stages_unique[tag] = ""


                if len(anomalies) > 0:
                    total["attack"] += 1
                else:
                    total["normal"] += 1
                total["rows"] += 1
        
        
        total["anomalies"] = len(anomalies_unique.keys())
        total["stages"] = len(stages_unique.keys())

        table = [
            [ "Total rows", "Attack", "Normal", "Attack points", "Attacked stages" ],
            [ total["rows"], total["attack"], total["normal"], total["anomalies"], total["stages"]]
        ]
        return table



    def get_anomalies_by_timestamp(self, timestamp_epoch):
        """
        goes through stats
        """

        res = []
        for tag in self.stats.keys():
            tmp = tag.split("_")
            ts_start = float(tmp[0])
            ts_end = float(tmp[1])

            if timestamp_epoch >= ts_start and timestamp_epoch <= ts_end:
                for anomaly in self.stats[tag]["anomalies"]:
                    res.append(anomaly)


        return res