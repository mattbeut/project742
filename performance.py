#!/usr/bin/python

# Calculates performance metrics 
# Note: requires 'numpy' (pip install numpy) for histogram option
# For plots: requires 'matplotlib' (pip install matplotlib)
#       you also may need to install python-tk (sudo apt install python-tk)

import sys
import os
import csv
import argparse
import numpy
import matplotlib.pyplot as plt

CSV_FILE1 = 0
CSV_FILE2 = 1
CSV_FILE1_SIZE = 2
CSV_FILE2_SIZE = 3
CSV_SECTION = 4
CSV_FIRST_ALG = 5
CSV_TRUTH = 8

SUPPORTED_ALGS =  ['ssdeep', 'tlsh', 'mvhash']
NUM_ALGS = len(SUPPORTED_ALGS)

# Maximum FP rate (used for finding a normalized score threshold across all algs)
MAX_FP_RATE = .20

# Binaries which differ by name but considered to be equivalent
equivalent_utilities = [["ls", "dir", "vdir"], ["true", "false"]]

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
            # Only consider sections if argument provided
            if not args.sections and row[CSV_SECTION] != 'full': continue
            # If min size provided, only consider comparisons of files at least that size
            if args.minSize and (row[CSV_FILE1_SIZE] < args.minSize or \
                    row[CSV_FILE2_SIZE] < args.minSize): continue

            file1_variant = row[CSV_FILE1].split('coreutils_')[1]
            file2_variant = row[CSV_FILE2].split('coreutils_')[1]

            # Must be different build variants
            if file1_variant == file2_variant: continue

            comparison_category = [file1_variant, file2_variant]
            # Sort alphabetically so that order doesn't matter and combine into string
            comparison_category.sort()
            comparison_category = '  <--->  '.join(comparison_category)

            if comparison_category not in bins:
                bins[comparison_category] = [[] for i in range(NUM_ALGS)]

            for alg in range(NUM_ALGS):
                if row[CSV_FIRST_ALG + alg].isdigit():
                    bins[comparison_category][alg].append(int(row[CSV_FIRST_ALG + alg]))

    return bins

# Gets TP/FP rate for a list of scores as determined by scores 
#   which exceed the provided threshold
def getRate(scores, threshold):
    count = 0.0

    for score in scores:
        if score >= threshold: count += 1

    rate = count / len(scores)

    return rate

def combineScores(bins):
    allscores = [[] for i in range(NUM_ALGS)]

    for b in bins:
        for alg in range(NUM_ALGS):
            for score in bins[b][alg]:
                allscores[alg].append(score)

    return allscores

def plotRoc(tpScores, fpScores, plotName):
    # Track lowest thresholds that achieve FP rate below MAX_FP_RATE
    minThresholds = [100] * NUM_ALGS
    # TP rate corresponding to this minimum threshold
    minThresholds_tpRates = [0.0] * NUM_ALGS

    for alg in range(NUM_ALGS):
        tpRates = []
        fpRates = []
        for threshold in range(0, 100):
            tpRate = getRate(tpScores[alg], threshold)
            fpRate = getRate(fpScores[alg], threshold)

            tpRates.append(tpRate)
            fpRates.append(fpRate)

            if fpRate < MAX_FP_RATE and threshold < minThresholds[alg]:
                minThresholds[alg] = threshold
                minThresholds_tpRates[alg] = tpRate

        plt.plot(fpRates, tpRates, label=SUPPORTED_ALGS[alg])
        
    plt.title("ROC Curve: %s" %plotName)
    plt.legend()

    for alg in range(NUM_ALGS):
        print("%s: (%s) Minimum %s FP-rate threshold: %d (TP-rate = %s)" \
                    %(SUPPORTED_ALGS[alg],
                    plotName,
                    MAX_FP_RATE,
                    minThresholds[alg],
                    round(minThresholds_tpRates[alg], 2)))

                                                
def roc(tpBins, fpBins, bucketName, plotResults):
    plot_count = 1
    # Form plot of each individual comparison category
    for b in tpBins:
        plt.figure(plot_count)
        plotRoc(tpBins[b], fpBins[b], b)

        plot_count += 1

    # Combine all scores for each algorithm to get single combined plot
    tpScores = combineScores(tpBins)
    fpScores = combineScores(fpBins)
 
    plotName = bucketName + " bucket"
    plt.figure(plot_count)
    plotRoc(tpScores, fpScores, plotName)

    if plotResults: plt.show()
    
def main():
    parser = argparse.ArgumentParser(description="Compute performances of each algorithm \
                    based on provided CSV. By default, calculates performance of true positives")
    parser.add_argument('csv', type=str, help="csv file to process")
    parser.add_argument('-f', '--falsePos', action='store_true',
                        help='calculate performance for comparisons labeled truth=no (false positives)')
    parser.add_argument('-s', '--sections', action='store_true',
                        help='include comparisons between individual sections in addition to full files')
    parser.add_argument('-m', '--minSize', type=int,
                        help='Only consider comparisons that were between files \
                                that meet this size threshold (in bytes)')
    parser.add_argument('--avg', action='store_true',
                        help='calculate average for each algorithm')
    parser.add_argument('--hist', action='store_true',
                        help='form histogram (10 buckets) for each algorithm')
    parser.add_argument('--plot', action='store_true', help='plot histograms/roc curves')
    parser.add_argument('--roc', action='store_true', help='perform roc analysis (with plots)')
    
    args = parser.parse_args()

    if not os.path.isfile(args.csv):
        print("[ ERROR ] Provided CSV is not a file")
        sys.exit(-1)
    
    bins = binVariants(args)

    if args.roc:
        # Assume name of bucket is name of csv
        # (this is only used to display the bucket's name in ROC curves)
        bucketName = os.path.basename(args.csv).split('.')[0]

        args.falsePos = False
        tpBins = binVariants(args)

        args.falsePos = True
        fpBins = binVariants(args)

        roc(tpBins, fpBins, bucketName, args.plot)

    if args.avg:  
        print("AVERAGES:")
        for category in bins:
            print("%s:" %category)
            for alg in range(NUM_ALGS):
                mean = 0
                if len(bins[category][alg]):
                    mean = sum(bins[category][alg])/len(bins[category][alg])
                print("\t%s (count: %d): %d" %(SUPPORTED_ALGS[alg],
                            len(bins[category][alg]), mean))

        if args.hist: print()

    if args.hist:
        print("HISTOGRAMS (10 even-width bins):")

        plot_count = 1
        for category in bins:
            print("%s:" %category)

            for alg in range(NUM_ALGS):
                # Normalize so sum of bars = 1
                weights = numpy.ones_like(bins[category][alg])/float(len(bins[category][alg]))

                # Get histogram data (not-normalized)
                hist,_ = numpy.histogram(bins[category][alg], range=(0, 100))
                intHist = [int(n) for n in hist]
                print("\t%s: %s" %(SUPPORTED_ALGS[alg], intHist))

                plt.figure(plot_count)
                plt.title("%s (count: %d): %s" %(SUPPORTED_ALGS[alg],
                            len(bins[category][alg]), category))
                plt.xlim(0, 100)
                plt.xticks([i*10 for i in range(11)])
                plt.ylim(0, 1)

                # Get normalized histogram for visual
                _,_,patches = plt.hist(bins[category][alg], range=(0, 100), weights=weights)

                # Color differently for true and false positives:
                #   red: bad (TP < 10, FP > 50)
                #   yellow: ok (10 < (TP or FP) < 50)
                #   green: good (TP > 50, FP < 10)

                for i in range(1, 5):
                    patches[i].set_fc('y')

                # False Positives
                if args.falsePos:
                    patches[0].set_fc('g')
                    for i in range(5, 10):
                        patches[i].set_fc('r')

                # True Positives
                else:
                    patches[0].set_fc('r')
                    for i in range(5, 10):
                        patches[i].set_fc('g')

                plot_count += 1

        # Plot with matplotlib
        if args.plot: plt.show()

if __name__ == "__main__":
    main()

