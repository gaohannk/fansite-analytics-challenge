from __future__ import print_function
import argparse
import operator
import re

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
            days = int(splits[0])
            ss = splits[2].split(':')
            hours = int(ss[1])
            minutes = int(ss[2])
            seconds = int(ss[3][0:2])
            time = days * 24 * 3600 + hours * 3600 + minutes * 60 + seconds
            timeDict[resource].append((subString, time))
    for resource, list in timeDict.items():
        countDict = {}
        head, end, count = 0, 0, 0
        while head < len(list) and end < len(list):
            if timeDict[resource][end][1] <= timeDict[resource][head][1] + 3600:
                count += 1
                end += 1
            else:
                # Only save the exactly same time for the first time appeared
                if list[head][0] not in countDict:
                    countDict[list[head][0]] = count
                count -= 1
                head += 1
        while head < len(list):
            if list[head][0] not in countDict:
                countDict[list[head][0]] = count
            count -= 1
            head += 1
        countList = [(key, value) for key, value in countDict.items()]
        countList.sort(key=operator.itemgetter(1), reverse=True)
        for i in range(0, min(3,len(countList))):
            resList.append(resource+','+countList[i][0]+'\n')
    with open(args.output, 'w') as out:
        for i in range(0, len(resList)):
            out.write(resList[i])
    print("Write result to output file: ", args.output)