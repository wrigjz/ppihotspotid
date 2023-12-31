#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
# Simple script to try to assemble data for the critires project
# In this method we take gas nergy values, calc's as the energy in the chain - the standard energy
# of the residue as a Me-X-Me triad
# Firstly we take the energy for each residue and sort them from lowest to highest
#
# We then do two different ways of ranking them:
#
# Rank: We take the gas energy range (highest gas energy - lowest gas energy) and divide that
# into 10 equal energy ranges, residues are then placed into the group that their gas energy
# falls into, the lowest gas energy residues into rank 10, the highest into rank 1
#
# Grade: Take the number of residues and devide by 10, we then assign the lowest gas energy
# 10% to grade 10, then next 10% to grade 9 and so on until all the remaining
# residues are assigned to grade 1
#
# When we calculate the Max/Min values we set the Energy Rank/grades of the ACE/NME to 5 and
# their consurf values to 0 to make sure these are not selected later on
#
# At the moment Max and Min are calculated using grade not rank
# usage: python3 assemble_data.py >| assemble.txt
# files needed:
#    relative sasa file
#    consurf grades files
#    stability file (comes from amber decomp after processing with extract_amber_energies.py)

import os.path
# Get the local dircetory and add it to the module search path
from res_numbers import RES_NUMBERS

# Get a line count for the arrays we need
NUM_LINES = 1
NUM_LINES += sum(1 for lines in open("post_mini.relsasa", "r"))

# And then setup the arrays
RESNAME = [0 for i in range(0, NUM_LINES)]
RESNUMBER = [0 for i in range(0, NUM_LINES)]
RELSASA = [0 for i in range(0, NUM_LINES)]
INT_STAB = [0 for i in range(0, NUM_LINES)]
VMD_STAB = [0 for i in range(0, NUM_LINES)]
ELE_STAB = [0 for i in range(0, NUM_LINES)]
POL_STAB = [0 for i in range(0, NUM_LINES)]
NPL_STAB = [0 for i in range(0, NUM_LINES)]
CONSURF = [0 for i in range(0, NUM_LINES)]
DSSP = ["L" for i in range(0, NUM_LINES)]
GAS_ENE = [0 for i in range(0, NUM_LINES)]
RANK = [0 for i in range(0, NUM_LINES)]
HOTSPOT = [0 for i in range(0, NUM_LINES)]
GRADE = [1 for i in range(0, NUM_LINES)]
MAX_RESNUM = 0
MIN_RESNUM = NUM_LINES

# Get the number of residues from the sasa file and the relative sasa value
INFILE = open("post_mini.relsasa", "r")
for LINE in INFILE:
    in1, in2, in3, *junk = [x.strip() for x in LINE.split(",")]
    resnum = int(in1)
    RESNUMBER[resnum] = int(in1)
    RESNAME[resnum] = in2
    RELSASA[resnum] = float(in3)
INFILE.close()

# Now allocate the hotspot residues if the file exists
# Need a reverse dictionary for this to work:
NUMBERS_REV = {v:k for k,v in RES_NUMBERS.items()}
if os.path.isfile("hotspots.txt"):
    INFILE = open("hotspots.txt", "r")
    for LINE in INFILE:
        resno = LINE.strip()
        ORIGINAL = (RES_NUMBERS_REV.get(resno))
        HOTSPOT[int(ORIGINAL)] = 1
    INFILE.close()

# Now we allocate the CONSURF values
INFILE = open("consurf.txt", "r")
for LINE in INFILE:
    in1, in2 = [x.strip() for x in LINE.split()]
    resnum = int(in1)
    CONSURF[resnum] = int(in2)
INFILE.close()

# Now we allocate the DSSP values
INFILE = open("post_mini_noh.dssp", "r")
RESFOUND = 0
for LINE in INFILE:
    if LINE[5:12] == "RESIDUE": # Look for the word RESIDUE in a sertain position
        RESFOUND = 1
        continue
    if RESFOUND == 1:
        TMP = LINE[6:11].strip()
        if TMP.isdigit():
            LIST = int(LINE[6:11].strip())
            if LINE[16:17] != " ":
                DSSP[LIST] = LINE[16:17]
INFILE.close()

# Now we allocate the energy values
INFILE = open("stability.txt", "r")
for LINE in INFILE:
    j1, in0, in1, in2, in3, in4, in5, in6 = [x.strip() for x in LINE.split()]
    resnum = int(in0)
    INT_STAB[resnum] = float(in1)
    VMD_STAB[resnum] = float(in2)
    ELE_STAB[resnum] = float(in3)
    POL_STAB[resnum] = float(in4)
    NPL_STAB[resnum] = float(in5)
    if MAX_RESNUM < resnum:
        MAX_RESNUM = resnum
    if MIN_RESNUM > resnum:
        MIN_RESNUM = resnum
INFILE.close()

#At this point we need to go through the data and look for the upper and lower gas phase energies
for j in range(MIN_RESNUM, MAX_RESNUM+1):
    GAS_ENE[j] = INT_STAB[j] + VMD_STAB[j] + ELE_STAB[j]
    if j == MIN_RESNUM:
        upper = GAS_ENE[j]
    if j == MIN_RESNUM:
        lower = GAS_ENE[j]
    if GAS_ENE[j] > upper:
        upper = GAS_ENE[j]
    if GAS_ENE[j] < lower:
        lower = GAS_ENE[j]
ENE_RANGE = upper - lower
BIN_WIDTH = ENE_RANGE / 10
#print(upper,lower,ENE_RANGE, BIN_WIDTH)

# Here we sort them into 9 RANKs of equal energy widths in case we use this method
for j in range(MIN_RESNUM, MAX_RESNUM+1):
    RANK[j] = 10
    for k in range(0, 10):
        if GAS_ENE[j] > (lower + (BIN_WIDTH * k)):
            RANK[j] = 10 - k

# Here we use a tuple to sort the gas phase energies, remove any non resname elements
GAS_LIST = tuple(zip(RESNUMBER, GAS_ENE, RESNAME))
GAS_LIST1 = list(filter(lambda a: a[2] != 0, GAS_LIST))
# Sort that tuple by the gas energy value, and get number of elements
SORTED_GAS = sorted(GAS_LIST1, key=lambda x: x[1])
NUM_OF_ELEMENTS = len(SORTED_GAS)

# Now we need to GRADE according to the energies, equal nos of residues in each
# of the first 9 bands with all the rest of the residues put into the last
BAND_WIDTH = int(NUM_OF_ELEMENTS  / 10)  # We are sorting into 10 groups
#print(MAX_RESNUM,MIN_RESNUM,BAND_WIDTH)
for k in range(0, 10):
    lower_loop = int(BAND_WIDTH * k)
    upper_loop = int(BAND_WIDTH * (k+1))
    if k == 9:
        upper_loop = NUM_OF_ELEMENTS
    #print("lower",lower_loop, "upper",upper_loop,"round",k)
    for j in range(lower_loop, upper_loop):
        GRADE[SORTED_GAS[j][0]] = 10 - k # We want most stable to be 10, least to be 1

# Print out the results table
print("Resi Ty cons   int    vdw    ele    pol    npl   sasa     gas_e  rank grade max min  PDB  DSSP HS")
for j in range(MIN_RESNUM, MAX_RESNUM+1):
    RES_MAX = GRADE[j] + CONSURF[j]
    RES_MIN = GRADE[j] - CONSURF[j]
    # We set ACE/NME max/min to 5 and CONSURF to 0 to ignore them
    if RESNAME[j] == "ACE" or RESNAME[j] == "NME":
        RES_MAX = 5
        RES_MIN = 5
        CONSURF[j] = 0
        GRADE[j] = 5
        RANK[j] = 5
    RESNUMBER_STR = str(RESNUMBER[j])
    ORIGINAL = (RES_NUMBERS.get(RESNUMBER_STR))
    if ORIGINAL is None:
        ORIGINAL = "NaN"
    print("{:>4}".format(RESNUMBER[j]), "{:>3}".format(RESNAME[j]), \
          "  {:>1}".format(CONSURF[j]), "{:6.1f}".format(INT_STAB[j]), \
          "{:6.1f}".format(VMD_STAB[j]), "{:6.1f}".format(ELE_STAB[j]), \
          "{:6.1f}".format(POL_STAB[j]), "{:6.1f}".format(NPL_STAB[j]), \
          "{:6.1f}".format(RELSASA[j]), "{:9.3f}".format(GAS_ENE[j]), \
          "  {:>2}".format(RANK[j]), "   {:>2}".format(GRADE[j]), \
          "{:>3}".format(RES_MAX), "{:>3}".format(RES_MIN), " {:>4}".format(ORIGINAL),\
          "{:>3}".format(DSSP[j]), "{:>3}".format(HOTSPOT[j]))
