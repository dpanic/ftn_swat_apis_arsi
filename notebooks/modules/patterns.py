import os
import sys
import time
import binascii, struct
import statistics

import pandas as pd
import modules.filter as filter
import modules.normalize as normalize

import _thread as thread
import modules.threading_control as threading_control

class Patterns:
    def __init__(self, precission, window_size):
        self.files = []
        self.stats = {}
        self.windows = {}

        self.window_size = window_size
        self.precission = precission
        self.detection = {}
        self.header = None
        
        self.ref_tc = threading_control.threading_control(max_work=3600*12, max_threads=20)


        
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
            time_start = anomaly["time_start"]
            time_end = anomaly["time_end"]
            time_start_str = "%s" %(time_start.astype("str"))
            time_end_str = "%s" %(time_end.astype("str"))

            _, time_start_epoch, _ = normalize.date_time(time_start_str)
            _, time_end_epoch, _ = normalize.date_time(time_end_str)

            tag = "%d_%d" %(time_start_epoch, time_end_epoch)
            if tag not in self.stats.keys():
                self.stats[tag] = {
                    "index": anomaly["index"],
                    "anomalies": [],
                    "time_start": time_start,
                    "time_end": time_end,
                }


            self.stats[tag]["anomalies"].append(anomaly)


        # print(len(self.stats.keys()))
        # total = 0
        # for tag in self.stats.keys():
        #     print(tag, len(self.stats[tag]["anomalies"]))
        #     total += len(self.stats[tag]["anomalies"])
        # print("total", total)
        # print("anoamlies", len(anomalies))
        # return


        it = 1
        total_processed = 0

        self.total = {
            "rows": 0,
            "anomalies": 0,
            "stages": 0
        }
        self.anomalies_unique = {}
        self.stages_unique = {}

        if max_process == -1:
            max_process = len(self.files) - skip_first

        # iterate file by file
        for file in self.files:
            it += 1
            if skip_first > -1 and it < skip_first:
                continue

            if max_process > -1 and total_processed >= max_process:
                break

            print("[ %d / %d | %d / %d ] processing file %s" %(total_processed+1, max_process, it, len(self.files), file))

            self.ref_tc.wait_threads()
            self.ref_tc.inc_threads()

            if self.header == None:
                df = pd.read_csv(file)
                self.header = df.columns.tolist()

            thread.start_new_thread(self.process, (file,))
            total_processed += 1

        while self.ref_tc.get_total_threads() > 0 and self.ref_tc.can_work():
            time.sleep(0.3)


        self.total["total_attack_points"] = len(self.anomalies_unique.keys())
        self.total["total_attack_stages"] = len(self.stages_unique.keys())

        attack_points = ", ".join(self.anomalies_unique.keys())
        attack_stages = ", ".join(self.stages_unique.keys())

        table1 = [
            [ "# rows",  "# Attack points", "Attack points", "# Attacked stages", "Attacked stages" ],
            [ self.total["rows"], self.total["total_attack_points"], attack_points, self.total["total_attack_stages"], attack_stages]
        ]        

        table2 = [
            [ "Attack #", "Detected", "Missed", "Attack Type", "Detected network requests",  "Missed network requests", "False positive network requests" ],
        ]

        for index in self.detection.keys():
            if self.detection[index]["detected_network_requests"] > 0:
                self.detection[index]["detected"] = True
            elif self.detection[index]["missed_network_requests"] > 0:
                self.detection[index]["missed"] = True
            elif self.detection[index]["false_positive_network_requests"] > 0:
                self.detection[index]["false_positive"] = True
            
            self.detection[index]["attack_type"] = "Network"
            if self.detection[index]["detected"] == False and self.detection[index]["missed"] == False:
                self.detection[index]["attack_type"] = "Physical"

            if self.detection[index]["false_positive"] > 0:
                self.detection[index]["attack_type"] = "Network"



        stats_sorted = []
        for index in self.detection.keys():
            if self.detection[index]["attack_type"] != "Network":
                continue

            stats_sorted.append([
                index,
                self.detection[index]["detected"],
                self.detection[index]["missed"],
                self.detection[index]["attack_type"],
                self.detection[index]["detected_network_requests"],
                self.detection[index]["missed_network_requests"],
                self.detection[index]["false_positive_network_requests"],
            ])
                
        stats_sorted = sorted(stats_sorted, key=lambda x: x[0])
        for s in stats_sorted:
            if s[0] == 0:
                s[0] = "*"
            table2.append(s)



        # stats for network requests
        total = 0
        detected = 0 
        missed = 0
        false_positive = 0
        for index in self.detection.keys():
            if self.detection[index]["attack_type"] != "Network":
                continue

            total += self.detection[index]["detected_network_requests"]
            detected += self.detection[index]["detected_network_requests"]
        
            total += self.detection[index]["missed_network_requests"]
            missed += self.detection[index]["missed_network_requests"]

            total += self.detection[index]["false_positive_network_requests"]
            false_positive += self.detection[index]["false_positive_network_requests"]

        detection_rate = 0
        if detected > 0 and total > 0:
            detection_rate = detected * 100.0 / total 

        miss_rate = 0
        if missed > 0 and total > 0:
            miss_rate = missed * 100.0 / total 

        false_positive_rate = 0
        if false_positive > 0 and total > 0:
            false_positive_rate = false_positive * 100.0 / total 

        detection_rate = "%.2f" %(detection_rate)
        miss_rate = "%.2f" %(miss_rate)
        false_positive_rate = "%.2f" %(false_positive_rate)


        table3 = [
            [ "Total", "Detected", "Detection %", "Missed", "Miss %", "False Positive", "False Positive %" ],
            [ total, detected, detection_rate, missed, miss_rate, false_positive, false_positive_rate ],
        ]



        # stats for detection of anomalies
        total = 0
        detected = 0 
        missed = 0
        
        for index in self.detection.keys():
            if index == 0:
                continue

            if self.detection[index]["attack_type"] != "Network":
                continue
                        
            if self.detection[index]["detected"]:
                total += 1
                detected += 1
            else:
                total += 1
                missed += 1

        detection_rate = 0
        if detected > 0 and total > 0:
            detection_rate = detected * 100.0 / total 

        miss_rate = 0
        if missed > 0 and total > 0:
            miss_rate = missed * 100.0 / total 


        detection_rate = "%.2f" %(detection_rate)
        miss_rate = "%.2f" %(miss_rate)

        table4 = [
            [ "Total", "Detected", "Detection %", "Missed", "Miss %" ],
            [ total, detected, detection_rate, missed, miss_rate ],
        ]

        return [ table1, table2, table3, table4 ]




    def process(self, file):
        """
            process file
        """

        # reading csv file
        try:
            header = self.header
            
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
                        for attack_point in anomaly["attack_points"]:
                            self.anomalies_unique[attack_point] = ""

                        for attack_stage in anomaly["attack_stages"]:
                            self.stages_unique[attack_stage] = ""



                    obj = self.parse_csv(header, line, ",")
                    if obj["Modbus_Function_Description"].find("Response") == -1:
                        continue
                    self.total["rows"] += 1

                    value = 0
                    tmp = obj["Modbus_Value"].split(";")
                    val = tmp[0]
                    val = val.replace("0x", "")
                    val = val.replace(" ", "")
                    if len(val) != 8:
                        continue
                    value = struct.unpack('<f', binascii.unhexlify(val))[0]

                    #     x = struct.unpack('<f', binascii.unhexlify(val))[0]
                    # for modbus_value in obj["Modbus_Value"].split(";"):
                    #     val = modbus_value
                    #     val = val.replace("0x", "")
                    #     val = val.replace(" ", "")
                    #     if len(val) != 8:
                    #         continue

                    #     x = struct.unpack('<f', binascii.unhexlify(val))[0]
                    #     # print(x)
                    #     value = x
                    # print("end")


                    is_attack_ongoing = False
                    if len(anomalies) > 0:
                        is_attack_ongoing = True

                    # process detection
                    dest = obj["SCADA_Tag"]
                    dest = dest.lstrip("HMI_")

                    self.moving_window(dest, value)

                    for anomaly in anomalies:
                        index = anomaly["index"]

                        try:
                            tmp = self.detection[index]
                        except:
                            self.detection[index] = {
                                "detected": False,
                                "missed": False,
                                "false_positive": False,
                                "detected_network_requests": 0,
                                "missed_network_requests": 0,
                                "false_positive_network_requests": 0,
                            }


                        is_ok = False
                        for at in anomaly["attack_points"]:
                            if at == dest:
                                is_ok = True
                                break

                        if is_ok == False:
                            continue

                        # print(dest, anomaly["attack_points"])
                        # print(anomaly)
                        is_attack_detected = self.detect_attack(dest)
                        if is_attack_ongoing:
                            if is_attack_detected == True:
                                self.detection[index]["detected_network_requests"] += 1
                            else:
                                self.detection[index]["missed_network_requests"] += 1
                    
                    if len(anomalies) == 0:
                        is_attack_detected = self.detect_attack(dest)
                        if is_attack_detected == False:
                            continue

                        try:
                            tmp = self.detection[0]
                        except:
                            self.detection[0] = {
                                "detected": False,
                                "missed": False,
                                "false_positive": False,
                                "detected_network_requests": 0,
                                "missed_network_requests": 0,
                                "false_positive_network_requests": 0,
                            }
                        self.detection[0]["false_positive_network_requests"] += 1



                    # global stats

        except:
            print("process: %s" %(str(sys.exc_info())))
        self.ref_tc.dec_threads()



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


    def parse_csv(self, header, line, delimiter):
        """
            parses csv based on header and delimiter
        """
        obj = {}

        line = line.replace("\r", "")
        line = line.replace("\n", "")

        tmp = line.split(delimiter)

        for t in range(0, len(tmp)):
            key = header[t]
            obj[key] = tmp[t]

        return obj


    def moving_window(self, name, value):
        """
            counts stats based on name
        """

        try:
            tmp = self.windows[name]
        except:
            self.windows[name] = []

        if len(self.windows[name]) > self.window_size:
            self.windows[name] = self.windows[name][1:]
        self.windows[name].append(value)


    def detect_attack(self, name):
        """
            detect if attack is going or not
        """

        if len(self.windows[name]) < self.window_size:
            return False

        stdev = statistics.stdev(self.windows[name])
        avg = statistics.median(self.windows[name])

        min_border = avg - stdev
        max_border = avg + stdev

        alerts = []
        for idx in range(0, len(self.windows[name])-1):
            value = self.windows[name][idx]

            is_for_alert = False
            if value < min_border:
                is_for_alert = True

            if value > max_border:
              is_for_alert = True

            if is_for_alert:
                alerts.append(idx)


        # minimum 10% of window size must be detection rate
        min_alerts = self.window_size/100*10 
        max_alerts = self.window_size/100*25 
        if len(alerts) > min_alerts and len(alerts) < max_alerts:
            # print("dusan len(alerts)=%s | self.window_size=%d | stdev=%.2f | avg=%.2f"%(len(alerts), self.window_size, stdev, avg))
            return True
        
        return False




