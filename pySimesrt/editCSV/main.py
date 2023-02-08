import sys
import csv
import statistics as stat
from csvsplitmodule import split_data

def read_data_from_file(path):

    with open(path, 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',',)

        return list(map(lambda x: list(map(float, x)), list(spamreader)[1:]))

def calculate_statistics(data):
    ndata = []
    for i in data:
        d = [*map(lambda x: x[1], i)]
        ndata += [[len(i), stat.fmean(d), stat.mode(d), stat.median(d)]]
    return ndata

if __name__ == "__main__":
    print(sys.argv)
    fname = sys.argv[1]

    d = read_data_from_file(fname)
    d = split_data(d)
    result = calculate_statistics(d)

    for j in ["(len)", "(statistics.mean)", "(statistics.mode)", "(statistics.median)"]:
        print(j, end=" " * (25 - len(j)))
    print()

    for i in result[int(sys.argv[2]):int(sys.argv[3])]:
        for j in i:
            s = str(j)
            print(s, end=" "*(25-len(s)))
        print()
