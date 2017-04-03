from __future__ import print_function
import argparse
import operator

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Log', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', default=None, help='Input file path containing log')
    parser.add_argument('--output', default=None, help='Output file path to save top 10 active hosts/IP addresse')
    args = parser.parse_args()
    print("Reading data for input file: ", args.input)
    count = {}
    with open(args.input, 'r') as f:
        for line in f:
            site = line[0:line.find(' - - ')]
            if site in count:
                count[site] = count[site] + 1
            else:
                count[site] = 1
    countList = [(key, value) for key, value in count.items()]
    countList.sort(key=operator.itemgetter(1), reverse=True)
    with open(args.output, 'w') as out:
        for i in range(0, min(10,len(countList))):
            out.write(countList[i][0] + ',' + str(countList[i][1]) + '\n')
    print("Write result to output file: ", args.output)
