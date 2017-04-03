from __future__ import print_function
import argparse
import operator
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Log', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input', default=None, help='Input file path containing log')
    parser.add_argument('--output', default=None, help='Output file path to save blocked request')
    args = parser.parse_args()
    timeList = []
    print("Reading data for input file: ", args.input)
    # {site:(beginTime,count,flag)}
    # beginTime is the time of first failed login or the begin of block time or the time of success login
    # count is failed login times at current time
    # flag indicate if in blocked status
    siteDict = {}
    resList = []
    with open(args.input, 'r') as f:
        for line in f:
            site = line[0:line.find(' - - ')]
            code = line[line.rfind(' ') - 3:line.rfind(' ')]
            subString = re.search('\[.*\]', line).group(0)
            splits = subString.split('/')
            days = int(splits[0][1:])
            ss = splits[2].split(':')
            hours = int(ss[1])
            minutes = int(ss[2])
            seconds = int(ss[3][0:2])
            time = days * 24 * 3600 + hours * 3600 + minutes * 60 + seconds
            # First appear
            if site not in siteDict:
                if code == "401":
                    siteDict[site] = (time, 1, False)
                    continue
                else:
                    siteDict[site] = (time, 0, False)
                    continue
            # Blocked status
            if siteDict[site][2] is True:
                # Still in blocked window
                if siteDict[site][0] + 300 >= time:
                    resList.append(line)
                    continue
            # Not blocked status or pass block window
            # Failed login
            if code == "401":
                # 20 Seconds already Pass
                if siteDict[site][0] + 20 < time:
                    siteDict[site] = (time, 1, False)
                elif siteDict[site][1] == 0:
                    siteDict[site] = (time, 1, False)
                elif siteDict[site][1] == 1:
                    siteDict[site] = (siteDict[site][0], 2, False)
                elif siteDict[site][1] == 2:
                    siteDict[site] = (time, 0, True)
            # Success
            else:
                siteDict[site] = (time, 0, False)
    with open(args.output, 'w') as out:
        for res in resList:
            out.write(res)
    print("Write result to output file: ", args.output)
