#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
import sys
import math

# This script takes a PDB file as it's input and looks for potential disulphide bridges
CUTOFF = 2.9

if len(sys.argv) < 2:
    print("Please give input pdb file")
    sys.exit()

INPDB = open(sys.argv[1], "r")

SEGI = []
RESID = []
XPOS = []
YPOS = []
ZPOS = []
COUNTER = -1

SEGID = "UNK"
if sys.argv[1] == "processed_rec.pdb":
    SEGID = "receptor"
if sys.argv[1] == "processed_lig.pdb":
    SEGID = "ligand"
if sys.argv[1] == "processed.pdb":
    SEGID = "trx"

#ATOM  16350  SG  CYX    19    -101.448  -6.936 -25.149  1.00 64.73      INSB
# Now process the PDB file,
# When we find the " H2 " line we need to convert this to "ACE  C" and change the resid number too
# We save this for the 2nd time we process the PDB file
INDEX = -1
for TMLINE in INPDB:
    # Keep a count of ACE and NME residues
    if TMLINE[13:14] == "C" and TMLINE[17:20] == "ACE":
        COUNTER += 1
    if TMLINE[13:14] == "N" and TMLINE[17:20] == "NME":
        COUNTER += 1
    if TMLINE[13:15] == "SG" and TMLINE[17:20] == "CYX":
        INDEX += 1
        SEGI.append(TMLINE[72:76])
        TEMP = int(TMLINE[22:26])
        TEMP += COUNTER
        RESID.append(TEMP)
        XPOS.append(TMLINE[30:38])
        YPOS.append(TMLINE[38:46])
        ZPOS.append(TMLINE[46:54])

# Now loop over the CYS SG's and look for potential disu bonds
for I in range(0,INDEX):
    for J in range(I+1,INDEX+1):
        xdist = (float(XPOS[I]) - float(XPOS[J]))**2
        ydist = (float(YPOS[I]) - float(YPOS[J]))**2
        zdist = (float(ZPOS[I]) - float(ZPOS[J]))**2
        dist = math.sqrt(xdist + ydist + zdist)
        if dist <= CUTOFF:
            OUTPUT = "bond " + SEGID + "." + str(RESID[I]) +\
                ".SG " + SEGID + "." + str(RESID[J]) + ".SG"
            print(OUTPUT)
