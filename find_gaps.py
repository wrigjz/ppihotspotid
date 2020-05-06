#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
import sys

# This file will read the process.txt file from pdb4amber and
# look for the gaps, it will then add the TER line after each gap
# Because of the size of the ACE and NME groups we only take gaps >= 3.3Angs

if len(sys.argv) < 4:
    print("Please give input pdb file, pdb4amber output and output file")
    exit()

INPDB = open(sys.argv[1], "r")
PROCESS = open(sys.argv[2], "r")
OUTPDB = open(sys.argv[3], "w")

INDEX = -1
UPPER = [0 for i in range(0, 10000)]

# Process the pdb4amber output and look for the gaps
# take the UPPER residue for each gap
for LINE in PROCESS:
    test = len([x.strip() for x in LINE.split()])
    if test != 10:
        continue
    gap, of, dist, angs, between, resna1, resid1, junk, resna2, resid2 = \
         [x.strip() for x in LINE.split()]
    if gap == "gap" and resid1 != resid2:
        if float(dist) >= 3.3:  # big enough gap to terminal with ACE/NME
            INDEX += 1
            UPPER[INDEX] = str(resid2)
            print("Terminating INDEX: ", INDEX, " Before: ", UPPER[INDEX])

# Now process the PDB file, when we find the UPPER residue for the 1st time
# We print and "TER" line
for TMLINE in INPDB:
    if TMLINE[0:6] == "CONECT":
        continue
    if TMLINE[0:4] == "ATOM":
        resid_long = TMLINE[22:26] # We shouldn't need to worry about A/B residues
        resid = resid_long.replace(" ", "") # Remove whitespace from resid
        for i in range(0, INDEX+1):
            if str(resid) == UPPER[i] and TMLINE[12:15] == " N ":
                OUTPDB.write("TER\n")
                print("Performing: ", i)
        OUTPDB.write(TMLINE)
    else:
        OUTPDB.write(TMLINE)
    # gap of 4.045442 A between ASP 120 and ARG 121
