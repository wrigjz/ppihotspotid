#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
# Simple script to try take the assembled data
# and then locate the top 4 (or equal) Max and bottom 4 (or equal) min values
# from column 14 and 15, we discard any that have a sasa < a cutoff
#
# We then look for any Stable residues vdw bonded to any Unstable residues (Matrix pair)
# Then look for any other residues (SASA > cutoff & Kc == 9) that are vdw bonded to
# either of the Stab/UnStab matrix pairs - we call these Bridge residues
#
# Stable are the low numbers e.g. energy rank - high consurf = v negative (min)
# Unstable are the high numbers e.g. energy rank + high consurf = v positive (max)
#
# Even though we read in the PDB numbers we have to use the internal scheme in order
# to remain consistent with hbplus

#Resi Ty bind cons   int    vdw    ele    pol    npl   sasa  gas_e rank  rern max min cle
#  1 ACE    0   0   32.0   -0.6  -13.8   -0.3   -0.3   71.3   17.6    3     1   1   1   0
#
# usage: python3 find_stable_unstable.py >| results_ambnum.txt
# files needed:
#    assemble.txt - comes from using the assemble_data.py script
#    vdw contact file - usually a nb2 file from hbplus
import sys

INDEX = 0
# Open the data file and create the needed arrays
INFILE = open("assemble.txt", "r")
for LINE in INFILE:
    if LINE[0:4] != "Resi":
        INDEX += 1
INFILE.seek(0)

# We initilize the arrays we need
RESNAME = [0 for i in range(0, INDEX)]
RESNUMBER = [0 for i in range(0, INDEX)]
RELSASA = [0 for i in range(0, INDEX)]
INT_STAB = [0 for i in range(0, INDEX)]
VDW_STAB = [0 for i in range(0, INDEX)]
ELE_STAB = [0 for i in range(0, INDEX)]
POL_STAB = [0 for i in range(0, INDEX)]
NPL_STAB = [0 for i in range(0, INDEX)]
CONSURF = [0 for i in range(0, INDEX)]
GAS_ENR = [0 for i in range(0, INDEX)]
RANK = [0 for i in range(0, INDEX)]
GRADE = [1 for i in range(0, INDEX)]
MAX_VALUE = [0 for i in range(0, INDEX)]
MIN_VALUE = [0 for i in range(0, INDEX)]
STABLE_NAME = [0 for i in range(0, INDEX)]
STABLE_NUMBER = [0 for i in range(0, INDEX)]
UNSTABLE_NAME = [0 for i in range(0, INDEX)]
UNSTABLE_NUMBER = [0 for i in range(0, INDEX)]
PDB = [0 for i in range(0, INDEX)]
RESIDUE_ST = [0 for i in range(0, INDEX)]
RESIDUE_UN = [0 for i in range(0, INDEX)]
BRIDGE = [0 for i in range(0, INDEX)]
MATRIXNB2 = [[0 for i in range(0, INDEX)] for j in range(0, INDEX)] # For HB2 results
RESIDUE1 = []
RESIDUE2 = []


# Are we critires or bindres?
if len(sys.argv) == 1:
    print("Needs a argument giving a either crit or bind\n")
    sys.exit(0)

if sys.argv[1] == "crit":
    SASA_CUTOFFST = float(0.0)
    SASA_CUTOFFUN = float(0.0)
    SASA_CUTOFFBR = float(0.0)
    CONSURF_CUTOFF = int(9)
elif sys.argv[1] == "bind":
    SASA_CUTOFFST = float(0.0)
    SASA_CUTOFFUN = float(30.0)
    SASA_CUTOFFBR = float(0.0)
    CONSURF_CUTOFF = int(8)
else:
    print("Needs a argument giving a either crit or bind\n")
    sys.exit(0)


INDEX = -1
for LINE in INFILE:
    if LINE[0:4] != "Resi":
        INDEX += 1
        RESNUMBER[INDEX], RESNAME[INDEX], in3, INT_STAB[INDEX], VDW_STAB[INDEX], \
            ELE_STAB[INDEX], POL_STAB[INDEX], NPL_STAB[INDEX], in0, GAS_ENR[INDEX], RANK[INDEX], \
            GRADE[INDEX], in1, in2, PDB[INDEX] \
                       = [x.strip() for x in LINE.split()]
        CONSURF[INDEX] = int(in3)
        RELSASA[INDEX] = float(in0)
        MAX_VALUE[INDEX] = int(in1)
        MIN_VALUE[INDEX] = int(in2)
INFILE.close()

# Here we merge the resnumber, resname, max, min and relsasa into a tuple
# and then remove where sasa <= cutoff
MERGED_LIST_SASA = tuple(zip(RESNUMBER, RESNAME, MAX_VALUE, MIN_VALUE, RELSASA))
MERGED_LIST_ST = list(filter(lambda a: a[4] > SASA_CUTOFFST, MERGED_LIST_SASA)) # ST where > ST_SASA
MERGED_LIST_UN = list(filter(lambda a: a[4] > SASA_CUTOFFUN, MERGED_LIST_SASA)) # UN where > UN_SASA
MERGED_LIST_LEN_ST = len(MERGED_LIST_ST)
MERGED_LIST_LEN_UN = len(MERGED_LIST_UN)

# Here we sort that tuple by the max and min number
MAX_ARRAY = sorted(MERGED_LIST_ST, key=lambda x: x[2], reverse=True)
MIN_ARRAY = sorted(MERGED_LIST_UN, key=lambda x: x[3])

#pprint(MIN_ARRAY)

# At this point we need to print out at the very least the top 4 residues and then any
# residues with equal scores to make sure there is a minimum of 4 printed
# So get the max and min value for the 4rd ranked residue
# then look for residues with a higher or equal max value, and residue with a lower or
# equal min value
# First we check that there are more than 4 elecments for each array, if les than 4 we
# take all of them
NO_OF_MAX=len(MAX_ARRAY)
NO_OF_MIN=len(MIN_ARRAY)
#print(NO_OF_MAX,NO_OF_MIN)
if NO_OF_MAX >= 4:
    MAX_NUMBER = MAX_ARRAY[3][2]
else:
    MAX_NUMBER = MAX_ARRAY[NO_OF_MAX-1][2]
if NO_OF_MIN >= 4:
    MIN_NUMBER = MIN_ARRAY[3][3]
else:
    MIN_NUMBER = MIN_ARRAY[NO_OF_MIN-1][3]
#print(MAX_NUMBER, MIN_NUMBER)
INDEX_ST = -1
INDEX_UN = -1

#print("Stable conserved")
for i in range(0, MERGED_LIST_LEN_ST):
    if MAX_ARRAY[i][2] >= MAX_NUMBER:
        INDEX_ST += 1
        NAME = MAX_ARRAY[i][1]
        NUMBER = MAX_ARRAY[i][0]
        print("{:>3},".format(NAME), "{:>4},".format(NUMBER), "Stable")
        STABLE_NAME[INDEX_ST] = NAME
        STABLE_NUMBER[INDEX_ST] = int(NUMBER)
        TEMP1 = int(NUMBER) -1
        RESIDUE_ST[TEMP1] = 1
        #print(RESIDUE_ST[TEMP1], NUMBER, TEMP1)

#print("Unstable conserved")
for i in range(0, MERGED_LIST_LEN_UN):
    if MIN_ARRAY[i][3] <= MIN_NUMBER:
        INDEX_UN += 1
        NAME = MIN_ARRAY[i][1]
        NUMBER = MIN_ARRAY[i][0]
        print("{:>3},".format(NAME), "{:>4},".format(NUMBER), "Unstable")
        UNSTABLE_NAME[INDEX_UN] = NAME
        UNSTABLE_NUMBER[INDEX_UN] = int(NUMBER)
        TEMP1 = int(NUMBER) -1
        RESIDUE_UN[TEMP1] = 1
        #print(RESIDUE_UN[TEMP1], NUMBER, TEMP1)

# Okay now we look for stable ----vdw --- unstable pairs
# Start by reading in the NB2 file
#X0002-PRO N   X0001-ACE CH3 2.46 MH  -2 -1.00  -1.0 -1.00  -1.0  27.8     1

# Now read in the vdw pairs from the nb2 file and form a matrix of elements duplicates
NB2FILE = open("post_mini_noh.nb2", "r")
INDEX_NB2 = -1
for LINE in NB2FILE:
    if LINE[0:1] == "X":
        temp1 = int(LINE[1:5])   # get the mini_mini resid and convert to internal
        temp2 = int(LINE[15:19]) # get the mini_mini resid and convert to internal
        temp1 = temp1 -1
        temp2 = temp2 -1
        if temp1 != temp2:
            MATRIXNB2[temp1][temp2] = 1 # Set the matrix for this residue pair to 1
            MATRIXNB2[temp2][temp1] = 1 # Set the matrix for this residue pair to 1

# Here we try to find residues that form stable/unstable pairs
for i in range(0, INDEX +1): # for each of the residues
    for j in range(0, INDEX +1):
        if (RESIDUE_ST[i] == 1 and RESIDUE_UN[j] == 1) or \
           (RESIDUE_ST[j] == 1 and RESIDUE_UN[i] == 1): # check if residue make a pairing
            if MATRIXNB2[i][j]:
                RESIDUE1.append(i)
                RESIDUE1.append(j)
                #print("Paired:",i,j)

# Here we try to find residues that are attached to one of a parted couple
i = -1
for each in RESIDUE1:
    i += 1
    for j in range(0, INDEX +1):
        if MATRIXNB2[RESIDUE1[i]][j] == 1:
            #print("{:>3},".format(RESNAME[j]), "{:>4},".format(RESNUMBER[j]), "Bridge")
            BRIDGE[j] = 1

# Look for bridge residues, ignore those duplicatig Stable/Unstable, only consider C=8 or 9
for i in range(0, INDEX +1):
    if RELSASA[i] > SASA_CUTOFFBR and CONSURF[i] >= CONSURF_CUTOFF and BRIDGE[i] == 1 and \
        RESIDUE_ST[i] == 0 and RESIDUE_UN[i] == 0:
        print("{:>3},".format(RESNAME[i]), "{:>4},".format(RESNUMBER[i]), "Bridge")
