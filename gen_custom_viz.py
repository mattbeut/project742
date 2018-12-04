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
from shutil import copyfile
import fileinput

def create_visualization(csvfilename, section, programs, metric):
    if len(programs) == 0:
        print("\nNo programs selected; generating visualization for " + section + " section of all")
    else:
        print("\nGenerating visualization for " + section + " section of " + str(len(programs)) + " programs (remember 11 is optimal for color scheme) : ")
        print programs
        
    template_file = "template2.html"

    html_file = os.path.join(os.path.splitext(csvfilename)[0] + "-" + section + ".html")

    copyfile(template_file, html_file)
    
    for line in fileinput.input(html_file, inplace=True):
        if "%CSV_FILENAME%" in line:
            print line.replace("%CSV_FILENAME%", os.path.basename(csvfilename))
        elif "%SECTION%" in line:
            print line.replace("%SECTION%", section)
        elif "%METRIC%" in line:
            print line.replace("%METRIC%", metric)
        elif "%PROGRAMS_CONDITIONAL%" in line:
            if len(programs) == 0 :
                print line.replace("%PROGRAMS_CONDITIONAL%", "if (true) ")
            else :
                a = "[\"" + "\", \"".join(str(x) for x in programs) + "\"]"
                str_replace = "var progs = " + a + "\n"
                str_replace += "if (progs.includes(prog1) && progs.includes(prog2)) "
                print line.replace("%PROGRAMS_CONDITIONAL%", str_replace)
        else:
            print line

    print("\nDone. Output at " + html_file)
                              

def main():
    parser = argparse.ArgumentParser(description="Create a custom visualization")
    parser.add_argument('csv', type=str, help="csv to base off of")
    parser.add_argument('section', type=str, help="section to create visualization for")
    parser.add_argument('programs', nargs='*', help="programs to filter on (optimal is 11)")
    parser.add_argument('-m', dest='metric', help="name of column for similarity metric", default="metric") 

    args = parser.parse_args()

    if not args.section in ["rodata", "full", "text", "data"]:
        print("[ ERROR ] invalid section: "+args.section)
        sys.exit(-1)

    create_visualization(args.csv, args.section, args.programs, args.metric)
    
if __name__ == "__main__":
    main()
    
    
