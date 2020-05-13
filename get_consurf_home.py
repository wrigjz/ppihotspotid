#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
import sys
# THis script retrieves the consurf grades and matches them with the pdb file
# that we used with our own version of consurf

# Open the hash for sequence to pre_mini.pdb renumbering scheme
from r4s_pdb import R4S_2_PDB

# Simple script to print out the consurf grades
#  # SEQ 3LETT PDB COLOUR  SCORE
#  1  H  HIS    2    6   -0.162

INFILE = open(sys.argv[1], "r")
OUTFILE = open(sys.argv[2], "w")
for LINE in INFILE:
    in1, in2, in3, pdbnum, grade, in6 = [x.strip() for x in LINE.split()]
    if in1 != "#":
        original = (R4S_2_PDB.get(pdbnum)) # get the consurf input pdb' resnumber
        OUTFILE.write(" {:>4}".format(original) + " {:>3}".format(grade) + "\n")
