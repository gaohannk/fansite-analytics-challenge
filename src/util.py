import datetime
import time


def convertBack(day, month, year, hours, minutes, seconds):
    day = str(day) if day >= 10 else "0" + str(day)
    month = numToMonth[month]
    year = str(year)
    hours = str(hours) if hours >= 10 else "0" + str(hours)
    minutes = str(minutes) if minutes >= 10 else "0" + str(minutes)
    seconds = str(seconds) if seconds >= 10 else "0" + str(seconds)
    return day + "/" + month + "/" + year + ":" + hours + ":" + minutes + ":" + seconds + " -0400"


def datetime_to_timestamp(datetime_obj):
    local_timestamp = long(time.mktime(datetime_obj.timetuple()))
    return local_timestamp


def timestamp_to_datetime(timestamp):
    local_dt_time = datetime.datetime.fromtimestamp(timestamp)
    return local_dt_time


monthToNum = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
              "Nov": 11, "Dec": 12}

numToMonth = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct",
              11: "Nov", 12: "Dec"}
