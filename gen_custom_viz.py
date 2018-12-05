#!/usr/bin/python

#
# Creates a custom html file for the csv and section passed.
# Uses the template2.html. You can also pass programs to filter the graph on (variable number, 11 is optimal)
# output will be in the same directory as the passed .csv file
#
# S. Helble
#

import os
import sys
import argparse
import csv
from shutil import copyfile
import fileinput

def create_visualization(csvfilename, section, programs, metric, threshold):
    modifiers = "-" + section + "-" + metric + "-t" + str(threshold) 
    new_csvfilename = os.path.splitext(csvfilename)[0] + modifiers + "_gen" + ".csv"

    template_file = "template2.html"
    html_file = os.path.splitext(csvfilename)[0] + modifiers + ".html"
    
    copyfile(template_file, html_file)
    
    if len(programs) == 0:
        print("\nNo programs selected; generating visualization for " + section + " section of all")
        # creating a smaller csv file now instead of making the javascript do all the work in the browser
        # this filters on the section selected
        with open(csvfilename) as csvfile:
            with open (new_csvfilename, 'wb') as n_csv:
                reader = csv.reader(csvfile)
                writer = csv.writer(n_csv)

                headers = next(reader)
                writer.writerow(headers)
                
                for row in reader:
                    if row[4] == section:
                        writer.writerow(row)
    else:
        print("\nGenerating visualization for " + section + " section of " + str(len(programs)) + " programs: ")
        print programs

        # creating a smaller csv file now instead of making the javascript do all the work in the browser
        # this filters on the programs and section selected
        with open(csvfilename) as csvfile:
            with open (new_csvfilename, 'wb') as n_csv:
                reader = csv.reader(csvfile)
                writer = csv.writer(n_csv)

                headers = next(reader)
                writer.writerow(headers)
                
                for row in reader:
                    if row[0].split('-')[0] in programs and row[1].split('-')[0] in programs and row[4] == section:
                        writer.writerow(row)
                    
    # Now replacing key strings in template with the values provided
    for line in fileinput.input(html_file, inplace=True):
        if "%CSV_FILENAME%" in line:
            print line.replace("%CSV_FILENAME%", os.path.basename(new_csvfilename))
        elif "%SECTION%" in line:
            print line.replace("%SECTION%", section)
        elif "%METRIC%" in line:
            print line.replace("%METRIC%", metric)
        elif "%THRESHOLD%" in line:
            print line.replace("%THRESHOLD%", str(threshold))
        else:
            print line

    print("\nDone. Output at " + html_file)
                              

def main():
    parser = argparse.ArgumentParser(description="Create a custom visualization")
    parser.add_argument('csv', type=str, help="csv to base off of")
    parser.add_argument('section', type=str, help="section to create visualization for")
    parser.add_argument('programs', nargs='*', help="programs to filter on (optimal is 11)")
    parser.add_argument('-m', dest='metric', help="name of column for similarity metric", default="metric")
    parser.add_argument('-t', dest='threshold', help="threshold for link", default=0) 

    args = parser.parse_args()

    if not args.section in ["rodata", "full", "text", "data"]:
        print("[ ERROR ] invalid section: "+args.section)
        sys.exit(-1)

    create_visualization(args.csv, args.section, args.programs, args.metric, args.threshold)
    
if __name__ == "__main__":
    main()
    
    
