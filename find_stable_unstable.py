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
# Then look for any other residues (SASA > cutoff) that are vdw bonded to 
# either of the Stab/UnStab matrix pairs - we call these Bridge residues
#
# Stable are the low numbers e.g. energy rank - high consurf = v negative (min)
# Unstable are the high numbers e.g. energy rank + high consurf = v positive (max)

#Resi Ty bind cons   int    vdw    ele    pol    npl   sasa  gas_e rank  rern max min cle
#  1 ACE    0   0   32.0   -0.6  -13.8   -0.3   -0.3   71.3   17.6    3     1   1   1   0

INDEX = 0
# Open the assemble file and create the needed arrays
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
SASA_CUTOFF = float(0.0)

INDEX = -1
for LINE in INFILE:
    if LINE[0:4] != "Resi":
        INDEX += 1
        RESNUMBER[INDEX], RESNAME[INDEX], in3, INT_STAB[INDEX], VDW_STAB[INDEX], \
            ELE_STAB[INDEX], POL_STAB[INDEX], NPL_STAB[INDEX], in0, GAS_ENR[INDEX], RANK[INDEX], \
            GRADE[INDEX], in1, in2 = [x.strip() for x in LINE.split()]
        CONSURF[INDEX] = int(in3)
        RELSASA[INDEX] = float(in0)
        MAX_VALUE[INDEX] = int(in1)
        MIN_VALUE[INDEX] = int(in2)
INFILE.close()

# Here we merge the resnumber, resname, max, min and relsasa into a tuple
# and then remove where sasa <= cutoff
MERGED_LIST_SASA = tuple(zip(RESNUMBER, RESNAME, MAX_VALUE, MIN_VALUE, RELSASA))
MERGED_LIST = list(filter(lambda a: a[4] > SASA_CUTOFF, MERGED_LIST_SASA))
                   # Remove 0 values from network list
MERGED_LIST_LEN = len(MERGED_LIST)

# Here we sort that tuple by the max and min number
MAX_ARRAY = sorted(MERGED_LIST, key=lambda x: x[2], reverse=True)
MIN_ARRAY = sorted(MERGED_LIST, key=lambda x: x[3])

#pprint(MIN_ARRAY)

# At this point we need to print out at the very least the top 4 residues and then any
# residues with equal scores to make sure there is a minimum of 4 printed
# So get the max and min value for the 4rd ranked residue
# then look for residues with a higher or equal max value, and residue with a lower or
# equal min value
MAX_NUMBER = MAX_ARRAY[3][2]
MIN_NUMBER = MIN_ARRAY[3][3]
#print(MAX_NUMBER, MIN_NUMBER)
INDEX_ST = -1
INDEX_UN = -1

#print("Stable conserved")
for i in range(0, MERGED_LIST_LEN):
    if MAX_ARRAY[i][2] >= MAX_NUMBER:
        INDEX_ST += 1
        NAME = MAX_ARRAY[i][1]
        NUMBER = MAX_ARRAY[i][0]
        print("{:>3},".format(NAME), "{:>4},".format(NUMBER), "Stable")
        STABLE_NAME[INDEX_ST] = NAME
        STABLE_NUMBER[INDEX_ST] = int(NUMBER)

#print("Unstable conserved")
for i in range(0, MERGED_LIST_LEN):
    if MIN_ARRAY[i][3] <= MIN_NUMBER:
        INDEX_UN += 1
        NAME = MIN_ARRAY[i][1]
        NUMBER = MIN_ARRAY[i][0]
        print("{:>3},".format(NAME), "{:>4},".format(NUMBER), "Unstable")
        UNSTABLE_NAME[INDEX_UN] = NAME
        UNSTABLE_NUMBER[INDEX_UN] = int(NUMBER)

# Okay now we look for stable ----vdw --- unstable pairs
# Start by reading in the NB2 file

#X0002-PRO N   X0001-ACE CH3 2.46 MH  -2 -1.00  -1.0 -1.00  -1.0  27.8     1
# Get an idea of the potential number of lines we will be dealing with
INDEX_NB2 = -1
NB2FILE = open("post_mini_noh.nb2", "r")
for LINE in NB2FILE:
    if LINE[0:1] == "X":
        INDEX_NB2 += 1
RESIDUE1 = [0 for i in range(0, INDEX_NB2+1)]
RESIDUE2 = [0 for i in range(0, INDEX_NB2+1)]
NETWORK = [0 for i in range(0, INDEX_NB2+1)]
NB2FILE.seek(0)

# Now read in the vdw pairs from the nb2 file and discard duplicates
INDEX_NB2 = -1
for LINE in NB2FILE:
    if LINE[0:1] == "X":
        temp1 = int(LINE[1:5])
        temp2 = int(LINE[15:19])
        # Check if this pairing has been seen before
        marker = 0
        for i in range(0, INDEX_NB2+1):
            if temp1 == RESIDUE1[i] and temp2 == RESIDUE2[i]:
                marker = 1
        # This is a new pair so we will save it
        if marker == 0:
            INDEX_NB2 += 1
            RESIDUE1[INDEX_NB2] = temp1
            RESIDUE2[INDEX_NB2] = temp2

# Set up an array to save the pairs for the network residues
SAVED_RESIDUE1 = [0 for i in range(0, INDEX_NB2+1)]
SAVED_RESIDUE2 = [0 for i in range(0, INDEX_NB2+1)]
#print(INDEX_ST, INDEX_UN, INDEX_NB2)

# Now we do the actual search for the Stable/Unstable vdw bonded pairs (Matrix residues)
MATRIX_NUMBER = -1
for k in range(0, INDEX_NB2+1):
    for i in range(0, INDEX_ST+1):
        for j in range(0, INDEX_UN+1):
            if (STABLE_NUMBER[i] == RESIDUE1[k] and UNSTABLE_NUMBER[j] == RESIDUE2[k]) or \
               (STABLE_NUMBER[i] == RESIDUE2[k] and UNSTABLE_NUMBER[j] == RESIDUE1[k]):
                   #print("Matrix Pair", STABLE_NAME[i], STABLE_NUMBER[i], UNSTABLE_NAME[j], \
                   # UNSTABLE_NUMBER[j])
                MATRIX_NUMBER += 1
                SAVED_RESIDUE1[MATRIX_NUMBER] = STABLE_NUMBER[i]
                SAVED_RESIDUE2[MATRIX_NUMBER] = UNSTABLE_NUMBER[j]

# New we need to look for the network residues which are connected to either one of the
# Stable / Unstable Matrix pairs
#print("Network residues")
INDEX_NET = -1
for i in range(0, MATRIX_NUMBER+1):
    for j in range(0, INDEX_NB2+1):
        if SAVED_RESIDUE1[i] == RESIDUE1[j] or SAVED_RESIDUE2[i] == RESIDUE1[j]:
            #print(RESIDUE2[j]) # Non-matching one
            INDEX_NET += 1
            NETWORK[INDEX_NET] = int(RESIDUE2[j]) # Save the non-matching residue
        if SAVED_RESIDUE1[i] == RESIDUE2[j] or SAVED_RESIDUE2[i] == RESIDUE2[j]:
            #print(RESIDUE1[j]) # Non-matching one
            INDEX_NET += 1
            NETWORK[INDEX_NET] = int(RESIDUE1[j]) # Save the non-matching residue

# Now try to remove network residues that are duplicates of the stable residues
for i in range(0, INDEX_NET+1):
    for j in range(0, INDEX_ST+1):
        if NETWORK[i] == STABLE_NUMBER[j]:
            #print("Forgotten Stable",NETWORK[i])
            NETWORK[i] = 0

# Now try to remove network residues that are duplicates of the unstable residues
for i in range(0, INDEX_NET+1):
    for j in range(0, INDEX_UN+1):
        if NETWORK[i] == UNSTABLE_NUMBER[j]:
            #print("Forgotten Unstable",NETWORK[i])
            NETWORK[i] = 0

# Now try to remove any duplicate network residues
for i in range(0, INDEX_NET+1):
    for j in range(i+1, INDEX_NET+1):
        if NETWORK[i] == NETWORK[j]:
            #print("Forgotten Network",NETWORK[i])
            NETWORK[i] = 0

# Now we order the Network residues, disgard any that are not 0, print what is left
NETWORK1 = list(filter(lambda a: a != 0, NETWORK)) # Remove 0 values from network list
NETWORK1.sort()  # sort network list
for line in NETWORK1:
    # Need to use -1 below because python arrays start at 0
    if RELSASA[line-1] > SASA_CUTOFF and CONSURF[line-1] == 9: # only print if relasas > cutoff,
                                                                # and consurf = 9
        print("{:>3},".format(RESNAME[line-1]), "{:>4},".format(RESNUMBER[line-1]), "Bridge")
