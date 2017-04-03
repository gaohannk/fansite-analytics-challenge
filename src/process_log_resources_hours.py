from __future__ import print_function
import argparse
import operator
import re
import datetime
import util

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
            month = util.monthToNum[splits[1]]
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
        first = util.datetime_to_timestamp(timeDict[resource][0])
        last = util.datetime_to_timestamp(timeDict[resource][len(timeDict[resource]) - 1])
        head, end, count = 0, 0, 0
        for sec in range(first, last):
            while end < len(timeDict[resource]) and util.datetime_to_timestamp(timeDict[resource][end]) <= sec + 3600:
                count += 1
                end += 1
            countDict[sec] = count
            while head < len(timeDict[resource]) and util.datetime_to_timestamp(timeDict[resource][head]) == sec:
                count -= 1
                head += 1
        countList = [(key, value) for key, value in countDict.items()]
        countList.sort(key=operator.itemgetter(1), reverse=True)
        for i in range(0, min(3,len(countList))):
            dt = util.timestamp_to_datetime(countList[i][0] * 1.0)
            originalTime = util.convertBack(dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second)
            resList.append(resource+','+str(countList[i][0])+'\n')
    with open(args.output, 'w') as out:
        for i in range(0, len(resList)):
            out.write(resList[i])
    print("Write result to output file: ", args.output)