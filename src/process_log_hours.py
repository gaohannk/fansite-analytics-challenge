from __future__ import print_function
import argparse
import operator
import re
import datetime
import util


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Log', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', default=None, help='Input file path containing log')
    parser.add_argument('--output', default=None, help='Output file path to save top 10 busiest 60-minute period.')
    args = parser.parse_args()
    # [(subString, time)] where subString is time string in [] and time is converted second format
    timeList = []
    print("Reading data for input file: ", args.input)
    with open(args.input, 'r') as f:
        for line in f:
            subString = re.search('\[.*\]', line).group(0)
            subString = subString[1:len(subString) - 1]
            splits = subString.split('/')
            days = int(splits[0])
            month = util.monthToNum[splits[1]]
            ss = splits[2].split(':')
            year = int(ss[0])
            hours = int(ss[1])
            minutes = int(ss[2])
            seconds = int(ss[3][0:2])
            dt = datetime.datetime(year, month, days, hours, minutes, seconds)
            # time = (days - 1) * 24 * 3600 + hours * 3600 + minutes * 60 + seconds
            timeList.append(dt)
    # {subString:count} where substring is time string in [] and count is the visit times
    countDict = {}
    first = util.datetime_to_timestamp(timeList[0])
    last = util.datetime_to_timestamp(timeList[len(timeList) - 1])
    head, end, count = 0, 0, 0
    for sec in range(first, last):
        while end < len(timeList) and util.datetime_to_timestamp(timeList[end]) <= sec + 3600:
            count += 1
            end += 1
        countDict[sec] = count
        while head < len(timeList) and util.datetime_to_timestamp(timeList[head]) == sec:
            count -= 1
            head += 1
    countList = [(key, value) for key, value in countDict.items()]
    countList.sort(key=operator.itemgetter(1), reverse=True)
    with open(args.output, 'w') as out:
        for i in range(0, min(10, len(countList))):
            dt = util.timestamp_to_datetime(countList[i][0] * 1.0)
            originalTime = util.convertBack(dt.day, dt.month, dt.year, dt.hour, dt.minute, dt.second)
            out.write(originalTime + ',' + str(countList[i][1]) + '\n')
    print("Write result to output file: ", args.output)
