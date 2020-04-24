#!/usr/bin/python3
###################################################################################################
## and Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
# Simple script to try to assemble data for the critires project
# In Backys method for the Energy values she takes the number of residues and divides by 10
# she then assigns the lowest 10% RANK 1, .. next lowest 10% RANK 2 .. to RANK 9
# then all the rest get assigned as value 10
# We set the Energy RANK of ACE/NME and their enighbours to 5 and their consuef values to 0
# to make sure these are not selected later on

# Here we try to block the energies into 9 equal sized energy ranges and assign residues to
# each range so it is more like a bell shaped curve

# Get a line count for the arrays we need
NUM_LINES = 1
NUM_LINES += sum(1 for lines in open("wild_relsasa.txt", "r"))

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
GAS_ENE = [0 for i in range(0, NUM_LINES)]
RANK = [0 for i in range(0, NUM_LINES)]
GRADE = [1 for i in range(0, NUM_LINES)]
POSITION = [0 for i in range(0, NUM_LINES)]
MAX_RESNUM = 0
MIN_RESNUM = NUM_LINES

# Get the number of residues from the sasa file and the relative sasa value
INFILE = open("wild_relsasa.txt", "r")
for LINE in INFILE:
    in1, in2, in3, *junk = [x.strip() for x in LINE.split(",")]
    resnum = int(in1)
    RESNUMBER[resnum] = int(in1)
    RESNAME[resnum] = in2
    RELSASA[resnum] = float(in3)
INFILE.close()

# Now we allocate the CONSURF values
INFILE = open("wild_consurf.txt", "r")
for LINE in INFILE:
    in1, in2 = [x.strip() for x in LINE.split()]
    resnum = int(in1)
    CONSURF[resnum] = int(in2)
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
    POSITION[resnum] = resnum
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

# Here try to sort the residues based on GAS_ENErgies, posiiton should now run from
# lowest E to highest E
#for j in range(0,i):
UNSORTED = 1
while UNSORTED == 1:
    UNSORTED = 0
    for k in range(0, MAX_RESNUM):
        if GAS_ENE[POSITION[k]] > GAS_ENE[POSITION[k+1]]:
            temp_pos = POSITION[k]
            POSITION[k] = POSITION[k+1]
            POSITION[k+1] = temp_pos
            UNSORTED = 1
    if UNSORTED == 0:
        break

# Now we need to GRADE according to the energies, equal # of residues in each band
BAND_WIDTH = (MAX_RESNUM-MIN_RESNUM)/10  # We are sorting into 10 groups
for k in range(0, 10):
    lower_loop = int(BAND_WIDTH * k)
    upper_loop = int(BAND_WIDTH * (k+1)) + 1
    #print("lower",lower_loop, upper_loop,k)
    for j in range(lower_loop, upper_loop):
        GRADE[POSITION[j]] = 10 - k

# Print out the results table
print("Resi Ty cons   int    vdw    ele    pol    npl   sasa  gas_e  rank grade max min")
for j in range(MIN_RESNUM, MAX_RESNUM+1):
    res_max = GRADE[j] + CONSURF[j]
    res_min = GRADE[j] - CONSURF[j]
    # We set ACE/NME max/min to 5 and CONSURF to 0 to ignore them
    if RESNAME[j] == "ACE" or RESNAME[j] == "NME":
        res_max = 5
        res_min = 5
        CONSURF[j] = 0
    print("{:>4}".format(RESNUMBER[j]), "{:>3}".format(RESNAME[j]), \
          "  {:>1}".format(CONSURF[j]), "{:6.1f}".format(INT_STAB[j]), \
          "{:6.1f}".format(VMD_STAB[j]), "{:6.1f}".format(ELE_STAB[j]), \
          "{:6.1f}".format(POL_STAB[j]), "{:6.1f}".format(NPL_STAB[j]), \
          "{:6.1f}".format(RELSASA[j]), "{:6.1f}".format(GAS_ENE[j]), \
          "  {:>2}".format(RANK[j]), "   {:>2}".format(GRADE[j]), \
          "{:>3}".format(res_max), "{:>3}".format(res_min))
