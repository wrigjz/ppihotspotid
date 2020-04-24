#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
import sys

# Simple script to print out the consurf grades
#  # SEQ 3LETT PDB COLOUR  SCORE
#  1  H  HIS    2    6   -0.162

INFILE = open(sys.argv[1], "r")
OUTFILE = open(sys.argv[2], "w")
for LINE in INFILE:
    in1, in2, in3, pdbnum, grade, in6 = [x.strip() for x in LINE.split()]
    if in1 != "#":
        OUTFILE.write(" {:>3}".format(pdbnum) + " {:>3}".format(grade) + "\n")
