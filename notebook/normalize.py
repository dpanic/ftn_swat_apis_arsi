

def date_time(input):
    tmp = str(input).split(" ")

    year, month, day = date(tmp[0])
    hour, minute, second = time(tmp[1])


    timestamp = "%s-%s-%sT%s:%s:%s" %(year, month, day, hour, minute, second)
    timestamp_date = "%s-%s-%s" %(year, month, day)

    return [ timestamp, timestamp_date ]


def date(input):
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

    return [ str(year), str(month), str(day) ]

def time(input):
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

    return [ str(hour), str(minute), str(second) ]