import sys
import time


def date_time(input):
    """
        process date/time in desired format
    """
    
    timestamp = ""
    timestamp_epoch = 0
    timestamp_date = ""

    try:
        input = str(input)
        input = input.replace("T", " ")
        tmp = input.split(" ")

        year, month, day = parse_date(tmp[0])
        hour, minute, second = parse_time(tmp[1])


        timestamp = "%s-%s-%sT%s:%s:%s" %(year, month, day, hour, minute, second)
        timestamp_date = "%s-%s-%s" %(year, month, day)

        dts = time.strptime(timestamp, "%Y-%m-%dT%H:%M:%S")
        timestamp_epoch = time.mktime(dts)
    except:
        print("Error happened: %s, for input: '%s'" %(str(sys.exc_info()), input))



    return [ timestamp, timestamp_epoch, timestamp_date ]


def parse_date(input):
    """
        process date in desired format
    """
    year = ""
    month = ""
    day = ""

    try:
        if input.find("/") > -1:
            t = input.split("/")
            year = int(t[2])
            month = int(t[1])
            day = int(t[0])
        else:
            t = input.split("-")
            year = int(t[0])
            month = int(t[1])
            day = int(t[2])

        if month < 10:
            month = "0" + str(month)
        if day < 10:
            day = "0" + str(day)
    except:
        print("Error happened: %s, for input: '%s'" %(str(sys.exc_info()), input))

    return [ str(year), str(month), str(day) ]

def parse_time(input):
    """
        process time in desired format
    """

    hour = ""
    minute = ""
    second = ""

    try:
        t = input.split(":")

        hour = int(t[0])
        if hour < 10:
            hour = "0" + str(hour)

        minute = int(t[1])
        if minute < 10:
            minute = "0" + str(minute)

        second = int(t[2])
        if second < 10:
            second = "0" + str(second)

    except:
        print("Error happened: %s, for input: '%s'" %(str(sys.exc_info()), input))

    return [ str(hour), str(minute), str(second) ]


