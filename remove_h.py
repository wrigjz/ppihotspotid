#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
import sys

# A simple script to remove hydrogen atoms from a PDB file and renumber it from one
# at the same time while printing out the renumerbing scheme
#
# usage python3 remove_h.py input.pdb initial.pdb > renumber.txt

INFILE = open(sys.argv[1], "r")
OUTFILE = open(sys.argv[2], "w")

RESID = 0
PREVIOUS = -999
for LINE in INFILE:
    if LINE[0:4] != "ATOM": # If not an ATOM just print it out
        OUTFILE.write(LINE)
    else:
        temp1 = LINE[12:16] # Gets the atom type
        resname = LINE[17:20] # gets the residue type
        temp2 = LINE[22:27] # Gets the residue number
        word = temp1.strip()
        pdbresin = temp2.strip()
        if pdbresin != PREVIOUS: # increment the pdb number if a new reisdue
            RESID += 1
            PREVIOUS = pdbresin
            print("{:>4s}".format(resname), "{:>5s}".format(pdbresin), \
                  "{:>4s}".format(resname), "{:>4d}".format(RESID))
        if word[0:1] != "H":
            RESOUT = "{:>4s}".format(str(RESID))
            LINEOUT = LINE[0:22] + RESOUT + " " + LINE[27:80] + "\n"
            OUTFILE.write(LINEOUT)
