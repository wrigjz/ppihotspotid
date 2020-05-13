#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
##################################################################################################
#
# This script reads both a seqres fasta file and another one from the atoms and aligns them
# This allows us to use the seqres for a consurf run and obtain the results for the residues
# present in the pdb file from a third consurf results file calculated using our own consurf
# method
#
# usage:
# python3 select_seqs.py seqres.fasta atomlisted.fasta consurf.grades
# This requires that mk_fasta.py was used in order to create the atomlisted.faste
# and the r4s_pdb.py beforehand

import sys
#import shutil
from Bio import pairwise2
#from Bio.pairwise2 import format_alignment
# Read in the original PDB numbering scheme if the file exists
from r4s_pdb import R4S_2_PDB

if len(sys.argv) != 5:
    print("Please give seqres fasta file, the atoms fasta file, the grades files and output file.")
    exit()

TARGETFILE = open(sys.argv[1], "r")
INFILE = open(sys.argv[2], "r")
GRADESFILE = open(sys.argv[3], "r")
OUTFILE = open(sys.argv[4], "w")

INDEX = -1
TITLE0 = ""
TITLE1 = ""
SEQUENCE0 = ""
SEQUENCE1 = ""

# Read in the SEQRES version
for LINE in TARGETFILE:
    LINE = LINE.rstrip("\n") # remove the newline
    if LINE[0:1] == ">":
        TITLE0 = LINE
    else:
        SEQUENCE0 = SEQUENCE0 + LINE
TARGETFILE.close()
TARGET_LEN = len(SEQUENCE0)

# Now read in the ATOM version
for LINE in INFILE:
    LINE = LINE.rstrip("\n") # remove the newline
    if LINE[0:1] == ">":
        TITLE1 = LINE
    else:
        SEQUENCE1 = SEQUENCE1 + LINE
INFILE.close()

# Align them to get start to figure out the numbering
TEMP = pairwise2.align.localxx(SEQUENCE0, SEQUENCE1)

# Find the matching residues and print out the grades
SEQRES_INDEX = -1
ATOM_COUNT = 0
for i in TEMP[0][1]:
    SEQRES_INDEX += 1 # Increment the SEQRES_INDEX, we can not use i because it is a letter
    counter = SEQRES_INDEX + 1 # needed becasue python starts are zero
    if TEMP[0][1][SEQRES_INDEX] != "-": # Only consider ones that are aligned with the ATOMS
        GRADESFILE.seek(0) # Rewind the grades file
        for LINE in GRADESFILE: # Find the 'right' residue in the seqres.grades file
            number, single, triple, number1, grade, value = [x.strip() for x in LINE.split()]
            if number != "#": # Ignore the frist line of the grades file
                if int(number) == counter:
                    ATOM_COUNT += 1 # This is incremented when we have a match
                    TEMP1 = str(ATOM_COUNT)
                    # get the 'original' resnumber from the initial pdb file
                    original = (R4S_2_PDB.get(TEMP1))
                    # double check the Xs
                    print(original, grade, TEMP[0][1][SEQRES_INDEX], single, number, ATOM_COUNT)
                    output = "{:>4s} ".format(original) + "{:>3s}".format(grade) + "\n"
                    OUTFILE.write(output)
