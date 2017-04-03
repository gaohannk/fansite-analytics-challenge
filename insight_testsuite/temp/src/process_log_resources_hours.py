from __future__ import print_function
import argparse
import operator
import re
import datetime
import time

def convertBack(day, month, year, hours, minutes, seconds):
    day = str(day) if day >= 10 else "0" + str(day)
    month = numToMonth[month]
    year = str(year)
    hours = str(hours) if hours >= 10 else "0" + str(hours)
    minutes = str(minutes) if minutes >= 10 else "0" + str(minutes)
    seconds = str(seconds) if seconds >= 10 else "0" + str(seconds)
    return day + "/" + month + "/" + year + ":" + hours + ":" + minutes + ":" + seconds+" -0400"


def datetime_to_timestamp(datetime_obj):
    local_timestamp = long(time.mktime(datetime_obj.timetuple()))
    return local_timestamp


def timestamp_to_datetime(timestamp):
    local_dt_time = datetime.datetime.fromtimestamp(timestamp)
    return local_dt_time


monthToNum = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10,
              "Nov": 11,
              "Dec": 12}
numToMonth = {1: "Jan", 2: "Feb", 3: "Mar",
              4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12:
                  "Dec"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Log', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', default=None, help='Input file path containing log')
    parser.add_argument('--resources', default=None, help='Input file path containing top 10 resources')
    parser.add_argument('--output', default=None, help='Output file path to save top 3 busiest 60-minute period for each top 10 resources')
    args = parser.parse_args()
    resources = set()
    # {resource:[($subString, $time)]} where $subString is time string in [] and $time is converted seconds format
    timeDict = {}
    print("Reading data for input file: ", args.input)
    with open(args.resources, 'r') as f:
        for line in f:
            line = line[0:len(line)-1]
            resources.add(line)
            timeDict[line] = []
    resList = []
    with open(args.input, 'r') as f:
        for line in f:
            subString = line[line.find(']'):]
            lidx = subString.find('/')
            ridx = subString.rfind('HTTP')
            resource = subString[lidx: ridx-1]
            if resource not in resources:
                continue
            subString = re.search('\[.*\]', line).group(0)
            subString = subString[1:len(subString) - 1]
            splits = subString.split('/')
            month = monthToNum[splits[1]]
            ss = splits[2].split(':')
            year = int(ss[0])
            days = int(splits[0])
            ss = splits[2].split(':')
            hours = int(ss[1])
            minutes = int(ss[2])
            seconds = int(ss[3][0:2])
            dt = datetime.datetime(year, month, days, hours, minutes, seconds)
            # time = (days - 1) * 24 * 3600 + hours * 3600 + minutes * 60 + seconds
            timeDict[resource].append(dt)
    for resource, list in timeDict.items():
        countDict = {}
        first = datetime_to_timestamp(timeDict[resource][0])
        last = datetime_to_timestamp(timeDict[resource][len(timeDict[resource]) - 1])
        head, end, count = 0, 0, 0
        for sec in range(first, last):
            while end < len(timeDict[resource]) and datetime_to_timestamp(timeDict[resource][end]) <= sec + 3600:
                count += 1
                end += 1
            countDict[sec] = count
            # print(sec,count)
            while head < len(timeDict[resource]) and datetime_to_timestamp(timeDict[resource][head]) == sec:
                count -= 1
                head += 1
        countList = [(key, value) for key, value in countDict.items()]
        countList.sort(key=operator.itemgetter(1), reverse=True)
        for i in range(0, min(3,len(countList))):
            dt = timestamp_to_datetime(countList[i][0] * 1.0)
            originalTime = convertBack(dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second)
            resList.append(resource+','+countList[i][0]+'\n')
    with open(args.output, 'w') as out:
        for i in range(0, len(resList)):
            out.write(resList[i])
    print("Write result to output file: ", args.output)