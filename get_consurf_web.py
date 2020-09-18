#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
#
# Simple script to print out the consurf grades, taken from the web site and then renumbered
# to match the critires internal numbering scheme
#   1       N        ASN2:X      -0.329            6     -0.744,-0.136                       8,5
#     37/150        D,N,L
#
import sys
from r4s_pdb import R4S_2_PDB # Open the hash for sequence to pre_mini.pdb renumbering scheme

# Get the output name from the command line
if len(sys.argv) <= 2:
    print("Usage: get_consurf_web.py consurf_file output_file\n")
    sys.exit(0)

# Open input and output files
INFILE = open(sys.argv[1], "r")
OUTFILE = open(sys.argv[2], "w")

SEQNUM = 0
# go through the consurf.grades file match the numbering scheme with our pdb file
# and print out the residue with the grades
for TMLINE in INFILE:
    if TMLINE[18:19] == ":":
        SEQNUM += 1  # increment the consurf sequence number
        SEQNUM_STR = str(SEQNUM) # Done this way to be compatitble with Jon's own CS server
        original = (R4S_2_PDB.get(SEQNUM_STR)) # get the 'original' resnumber from
                                               # the post_mini.pdb file for CS
        score = TMLINE[31:32]
        OUTFILE.write(" {:>4}".format(original) + " {:>3}".format(score) + "\n")
