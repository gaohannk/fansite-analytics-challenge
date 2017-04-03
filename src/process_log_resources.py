from __future__ import print_function
import argparse
import operator
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Log', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', default=None, help='Input file path containing log')
    parser.add_argument('--output', default=None, help='Output file path to save top 10 resources')
    args = parser.parse_args()
    print("Reading data for input file: ", args.input)
    # {resource:byte}
    bandwidth = {}
    with open(args.input, 'r') as f:
        lastPass = 0
        for line in f:
            subString = line[line.find(']'):]
            lidx = subString.find('/')
            ridx = subString.rfind('HTTP')
            resource = subString[lidx: ridx-1]
            byte = line[line.rfind(' ') + 1:len(line) - 1]
            byte = 0 if byte == '-' else int(byte)
            if resource in bandwidth:
                bandwidth[resource] = bandwidth[resource] + byte
            else:
                bandwidth[resource] = byte
    bandwidthList = [(key, value) for key, value in bandwidth.items()]
    bandwidthList.sort(key=operator.itemgetter(1), reverse=True)
    with open(args.output, 'w') as out:
        for i in range(0, min(10,len(bandwidthList))):
            out.write(bandwidthList[i][0] + '\n')

    print("Write result to output file: ", args.output)
