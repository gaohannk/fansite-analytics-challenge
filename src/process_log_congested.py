from __future__ import print_function
import argparse
import operator
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Log', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', default=None, help='Input file path containing log')
    parser.add_argument('--output', default=None, help='Output file path to save top 10 congested 60-minute period.')
    args = parser.parse_args()
    timeList = []
    print("Reading data for input file: ", args.input)
    with open(args.input, 'r') as f:
        for line in f:
            subString = re.search('\[.*\]', line).group(0)
            splits = subString.split('/')
            days = int(splits[0][1:])
            ss = splits[2].split(':')
            hours = int(ss[1])
            minutes = int(ss[2])
            seconds = int(ss[3][0:2])
            time = days * 24 * 3600 + hours * 3600 + minutes * 60 + seconds
            byte = line[line.rfind(' ') + 1:len(line) - 1]
            byte = 0 if byte == '-' else int(byte)
            timeList.append((subString, time, byte))
    # {subString:count} where substring is time string in [] and count is the bandwidth in bytes consumed
    countDict = {}
    head, end, count = 0, 0, 0
    while head < len(timeList) and end < len(timeList):
        if timeList[end][1] <= timeList[head][1] + 3600:
            count += timeList[head][2]
            end += 1
        else:
            # Only save the exactly same time for the first time appeared
            if timeList[head][0] not in countDict:
                countDict[timeList[head][0]] = count
            count -= timeList[head][2]
            head += 1
    while head < len(timeList):
        if timeList[head][0] not in countDict:
            countDict[timeList[head][0]] = count
        count -= timeList[head][2]
        head += 1
    countList = [(key, value) for key, value in countDict.items()]
    countList.sort(key=operator.itemgetter(1), reverse=True)
    with open(args.output, 'w') as out:
        for i in range(0, min(10,len(countList))):
            out.write(countList[i][0] + ',' + str(countList[i][1]) + '\n')
    print("Write result to output file: ", args.output)