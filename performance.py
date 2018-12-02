#!/usr/bin/python

# Calculates performance metrics 
# Note: requires 'numpy' (pip install numpy) for histogram option
# For plots: requires 'matplotlib' (pip install matplotlib)
#       you also may need to install python-tk (sudo apt install python-tk)

import sys
import os
import csv
import argparse

CSV_FILE1 = 0
CSV_FILE2 = 1
CSV_FILE1_SIZE = 2
CSV_FILE2_SIZE = 3
CSV_SECTION = 4
CSV_FIRST_ALG = 5
CSV_TRUTH = 8

SUPPORTED_ALGS = ['ssdeep', 'tlsh', 'mvhash']

# Sorts comparison results into bins of variant comparisons
# e.g. bins comparisons between O0 and O1 variants separate from comparisons 
#   between O0 and O2 variants, for each of the three algs
def binVariants(args):
    with open(args.csv) as csvfile:
        next(csvfile)
        csvlist = csv.reader(csvfile, delimiter=',')

        bins = dict()

        for row in csvlist:
            truth = row[CSV_TRUTH] == 'yes'
            # Only consider either true or false positives
            if truth == args.falsePos: continue
            # If min size provided, only consider comparisons of files at least that size
            if args.minSize and (row[CSV_FILE1_SIZE] < args.minSize or \
                    row[CSV_FILE2_SIZE] < args.minSize): continue
            # Only consider sections if argument provided
            if not args.sections and row[CSV_SECTION] != 'full': continue

            file1_variant = row[CSV_FILE1].split('coreutils_')[1]
            file2_variant = row[CSV_FILE2].split('coreutils_')[1]

            comparison_category = [file1_variant, file2_variant]
            # Sort alphabetically so that order doesn't matter and combine into string
            comparison_category.sort()
            comparison_category = '  <--->  '.join(comparison_category)

            if comparison_category not in bins:
                bins[comparison_category] = [[] for i in range(len(SUPPORTED_ALGS))]

            for alg in range(len(SUPPORTED_ALGS)):
                if row[CSV_FIRST_ALG + alg]:
                    bins[comparison_category][alg].append(int(row[CSV_FIRST_ALG + alg]))

    return bins

def main():
    parser = argparse.ArgumentParser(description="Compute performances of each algorithm \
                    based on provided CSV. By default, calculates performance of true positives")
    parser.add_argument('csv', type=str, help="csv file to process")
    parser.add_argument('-f', '--falsePos', action='store_true',
                        help='calculate performance for comparisons labeled truth=no (false positives)')
    parser.add_argument('-s', '--sections', action='store_true',
                        help='include comparisons between individual sections in addition to full files')
    parser.add_argument('-m', '--minSize',
                        help='Only consider comparisons that were between files \
                                that meet this size threshold (in bytes)')
    parser.add_argument('--avg', action='store_true',
                        help='calculate average for each algorithm')
    parser.add_argument('--hist', action='store_true',
                        help='form histogram (10 buckets) for each algorithm')
    parser.add_argument('--plot', action='store_true', help='plot histograms')
    
    args = parser.parse_args()

    if not os.path.isfile(args.csv):
        print("[ ERROR ] Provided CSV is not a file")
        sys.exit(-1)

    bins = binVariants(args)

    if args.avg:  
        print("AVERAGES:")
        for category in bins:
            print("%s:" %category)
            for alg in range(len(SUPPORTED_ALGS)):
                mean = 0
                if len(bins[category][alg]):
                    mean = sum(bins[category][alg])/len(bins[category][alg])
                print("\t%s: %d" %(SUPPORTED_ALGS[alg], mean))

    if args.hist:
        print("HISTOGRAMS (10 even-width bins):")
        import numpy
        import matplotlib.pyplot as plt

        plot_count = 1
        for category in bins:
            print("%s:" %category)
            for alg in range(len(SUPPORTED_ALGS)):
                hist,_ = numpy.histogram(bins[category][alg])
                print("\t%s: %s" %(SUPPORTED_ALGS[alg], hist))

                # Plot with matplotlib
                if args.plot:
                    # Normalize so sum of bars = 1
                    weights = numpy.ones_like(bins[category][alg])/float(len(bins[category][alg]))

                    plt.figure(plot_count)
                    plt.title("%s: %s" %(SUPPORTED_ALGS[alg], category))
                    plt.xlim(0, 100)
                    plt.xticks([i*10 for i in range(11)])
                    plt.ylim(0, 1)

                    _,_,patches = plt.hist(bins[category][alg], range=(0, 100), weights=weights)

                    # red: score <= 10
                    patches[0].set_fc('r')
                    # yellow: 10 < score < 50
                    for i in range(1, 5):
                        patches[i].set_fc('y')
                    # green: score >= 50
                    for i in range(5, 10):
                        patches[i].set_fc('g')

                    plot_count += 1

        if args.plot: plt.show()

if __name__ == "__main__":
    main()

