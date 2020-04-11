#!/usr/bin/python3
import sys

# Simple script to add the chain id X to a PDB file

INFILE  = open(sys.argv[1],"r")
OUTFILE = open(sys.argv[2],"w")
for TMLINE in INFILE:
    if TMLINE[0:4] == "ATOM" or TMLINE[0:6] == "HETATM":
        output=TMLINE[0:21] + "X" + TMLINE[22:100]
        OUTFILE.write(output)
    else:
        OUTFILE.write(TMLINE)
