#!/usr/bin/python3
#########################################################################################################################
## and Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
#########################################################################################################################
import sys

# A simple script to remove hydrogen atoms from a PDB file

INFILE  = open(sys.argv[1],"r")
OUTFILE = open(sys.argv[2],"w")

for LINE in INFILE:
    if LINE[0:4] != "ATOM":
        OUTFILE.write(LINE)
    else:
       temp1 = LINE[12:16]
       word  = temp1.strip()
       if word[0:1] != "H":
           OUTFILE.write(LINE)

