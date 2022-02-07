#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
import sys
import math

# This script takes a PDB file as it's input and looks for potential Zinc binding CYS residues
# python find_cym.py input.pdb output.pdb
CUTOFF = 2.9

if len(sys.argv) < 3:
    print("Please give input & output pdb file")
    sys.exit()

INPDB = open(sys.argv[1], "r")
OUTPDB = open(sys.argv[2], "w")

RESID = []
XPOS = []
YPOS = []
ZPOS = []
ZN_RESID = []
ZN_XPOS = []
ZN_YPOS = []
ZN_ZPOS = []
LIG_RESID = []

#ATOM  16350  SG  CYS    19    -101.448  -6.936 -25.149  1.00 64.73      INSB
# Now process the PDB file,
INDEX = -1
ZN_INDEX = -1
LIG_INDEX = -1
for TMLINE in INPDB:
    if TMLINE[13:15] == "SG" and TMLINE[17:20] == "CYS":
        INDEX += 1
        RESID.append(TMLINE[22:26])
        XPOS.append(TMLINE[30:38])
        YPOS.append(TMLINE[38:46])
        ZPOS.append(TMLINE[46:54])
    if TMLINE[12:14] == "ZN" and TMLINE[17:19] == "ZN":
        ZN_INDEX += 1
        ZN_RESID.append(TMLINE[22:26])
        ZN_XPOS.append(TMLINE[30:38])
        ZN_YPOS.append(TMLINE[38:46])
        ZN_ZPOS.append(TMLINE[46:54])

# Now loop over the ZNs and CYS SG's and look for potential bonds
for I in range(0,ZN_INDEX+1):
    for J in range(0,INDEX+1):
        xdist = (float(ZN_XPOS[I]) - float(XPOS[J]))**2
        ydist = (float(ZN_YPOS[I]) - float(YPOS[J]))**2
        zdist = (float(ZN_ZPOS[I]) - float(ZPOS[J]))**2
        dist = math.sqrt(xdist + ydist + zdist)
        if dist <= CUTOFF:
            OUTPUT = "CYM RESIDUE " + RESID[J] + " " + ZN_RESID[I]
            print(OUTPUT)
            LIG_INDEX += 1
            LIG_RESID.append(RESID[J])

# Now we need to re-read the PDB file and change any CYS to CYM as needed
INPDB.seek(0)
for TMLINE in INPDB:
    CHANGED = 0
    for I in range(0,LIG_INDEX+1):
        if TMLINE[22:26] == LIG_RESID[I]:
            CHANGED = 1
    if CHANGED == 1:
        OUTPUT = TMLINE[0:17] + "CYM" + TMLINE[20:80] + "\n"
        OUTPDB.write(OUTPUT)
    else:
        OUTPDB.write(TMLINE)

