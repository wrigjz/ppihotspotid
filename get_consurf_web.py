#!/usr/bin/python3
import sys

# Simple script to print out the consurf grades
#   1       N        ASN2:X      -0.329            6     -0.744,-0.136                       8,5                   37/150        D,N,L

INFILE  = open(sys.argv[1],"r")
OUTFILE = open(sys.argv[2],"w")
for TMLINE in INFILE:
    if TMLINE[18:20] == ":X":
        namechain = TMLINE[11:18].strip()    # read in the name, resid number
        length    = len(namechain)           # find the combined length of the name/number
        number    = namechain[3:length]      # extract the number only
        score     = TMLINE[31:32]
        OUTFILE.write(" {:>3}".format(number) + " {:>3}".format(score) + "\n")
