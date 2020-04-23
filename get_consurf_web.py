#!/usr/bin/python3
#########################################################################################################################
## and Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
#########################################################################################################################
import sys
import os

# Simple script to print out the consurf grades, taken from the web site and then renumbered
# to match the critires internal numbering scheme
#   1       N        ASN2:X      -0.329            6     -0.744,-0.136                       8,5                   37/150        D,N,L

# Get the output name from the command line
if len(sys.argv) <= 2:
    print("Usage: get_consurf_web.py consurf_file output_file\n")
    sys.exit(0)

# Open input and output files
INFILE  = open(sys.argv[1],"r")
OUTFILE = open(sys.argv[2],"w")

# Open the hash for sequence to wild-mini.pdb renumbering scheme
from r4s_pdb import R4S_2_PDB
seqnum = 0
for TMLINE in INFILE:
    if TMLINE[18:19] == ":":
        seqnum += 1  # increment the consurf sequence number
        seqnum_str = str(seqnum) # Done this way to be compatitble with Jon's own CS server
        original = (R4S_2_PDB.get(seqnum_str)) # get the 'original' resnumber from the wild_mini pdb file for CS
        score     = TMLINE[31:32]
        OUTFILE.write(" {:>4}".format(original) + " {:>3}".format(score) + "\n")
