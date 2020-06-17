#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
# This script reads a PDB file and checks that each residue has a N, C, CA and O atom
# Any residues that are missing one of these are flagged up to an output file
#
# Usage:
# python3 check_bb.py input.pdb missing.txt

import sys

if len(sys.argv) < 3:
    print("Please give input pdb file and output txt file")
    exit()

# Open the in and out files
INPDB = open(sys.argv[1], "r")
OUTTXT = open(sys.argv[2], "w")

# Set up the backbone arrays
NATOM = []
CATOM = []
OATOM = []
CAATOM = []
RESNUM = []

PREVIOUS = "PREV"
INDEX = -1
PREV_CHAIN = "#"
# Read in the pdb file and process it
for TMLINE in INPDB:
    if TMLINE[0:4] == "ATOM":
        chain = TMLINE[21:22]
        if PREV_CHAIN == "#":
            chain_count = 1
            PREV_CHAIN = chain
        elif PREV_CHAIN != chain:
            chain_count += 1
        resid_long = TMLINE[22:27] # Need to include A/B/C residues
        resid = resid_long.replace(" ", "") # Remove whitespace from resid
        if resid != PREVIOUS: # New residue append to the arrays
            INDEX += 1         # Increment the index
            NATOM.append("0")
            CATOM.append("0")
            OATOM.append("0")
            CAATOM.append("0")
            RESNUM.append(resid)
            PREVIOUS = resid
        in1, in2, in3, *junk = [x.strip() for x in TMLINE.split()] # Fine the atom type
        if in3 == "N":
            NATOM[INDEX] = "1" # IF we find the 'right' one set to '1'
        if in3 == "C":
            CATOM[INDEX] = "1"
        if in3 == "O":
            OATOM[INDEX] = "1"
        if in3 == "CA":
            CAATOM[INDEX] = "1"

# Now make a tuple from the atoms and the residue numbers
NMERGED = tuple(zip(NATOM, RESNUM))
CMERGED = tuple(zip(CATOM, RESNUM))
OMERGED = tuple(zip(OATOM, RESNUM))
CAMERGED = tuple(zip(CAATOM, RESNUM))

# Remove all the ones where we found the atoms we wanted
NMERGED_LIST = list(filter(lambda a: a[0] == "0", NMERGED))
CMERGED_LIST = list(filter(lambda a: a[0] == "0", CMERGED))
OMERGED_LIST = list(filter(lambda a: a[0] == "0", OMERGED))
CAMERGED_LIST = list(filter(lambda a: a[0] == "0", CAMERGED))

# Find how many are missing backbone atoms
NLEN = len(NMERGED_LIST)
CLEN = len(CMERGED_LIST)
OLEN = len(OMERGED_LIST)
CALEN = len(CAMERGED_LIST)
#print(CLEN, NLEN, OLEN, CALEN)

# And then print them out
if CLEN != 0 or NLEN != 0 or OLEN != 0 or CALEN != 0:
    OUTTXT.write("Missing backbone atoms:\n")
    for i in range(0, NLEN):
        OUTTXT.write("Missing N atom on residue: ")
        OUTTXT.write(NMERGED_LIST[i][1])
        OUTTXT.write("\n")
    for i in range(0, CLEN):
        OUTTXT.write("Missing C atom on residue: ")
        OUTTXT.write(CMERGED_LIST[i][1])
        OUTTXT.write("\n")
    for i in range(0, OLEN):
        OUTTXT.write("Missing O atom on residue: ")
        OUTTXT.write(OMERGED_LIST[i][1])
        OUTTXT.write("\n")
    for i in range(0, CALEN):
        OUTTXT.write("Missing CA atom on residue: ")
        OUTTXT.write(CAMERGED_LIST[i][1])
        OUTTXT.write("\n")
INPDB.close()
if chain_count > 1:
    OUTTXT.write("Too many chains: ")
    OUTTXT.write(str(chain_count))
    OUTTXT.write("\n")
OUTTXT.close()
