#!/usr/bin/python3

# Simple script to try to assemble data for the critires project
# In Backys method for the Energy values she takes the number of residues and divides by 10
# she then assigns the lowest 10% rank 1, .. next lowest 10% rank 2 .. to rank 9 
# then all the rest get assigned as value 10
# We set the Energy rank of ACE/NME and their enighbours to 5 and their consuef values to 0
# to make sure these are not selected later on

# Here we try to block the energies into 9 equal sized energy ranges and assign residues to 
# each range so it is more like a bell shaped curve

import sys
# Get a line count for the arrays we need
num_lines = 1
num_lines += sum(1 for lines in open("wild_relsasa.txt","r"))

# And then setup the arrays
resname   = [0 for i in range(0,num_lines)]
resnumber = [0 for i in range(0,num_lines)]
relsasa   = [0 for i in range(0,num_lines)]
int_stab  = [0 for i in range(0,num_lines)]
vdw_stab  = [0 for i in range(0,num_lines)]
ele_stab  = [0 for i in range(0,num_lines)]
pol_stab  = [0 for i in range(0,num_lines)]
npl_stab  = [0 for i in range(0,num_lines)]
consurf   = [0 for i in range(0,num_lines)]
gas_ene   = [0 for i in range(0,num_lines)]
rank      = [0 for i in range(0,num_lines)]
rerank    = [1 for i in range(0,num_lines)]
position  = [0 for i in range(0,num_lines)]
max_resnum = 0
min_resnum = num_lines

# Get the number of residues from the sasa file and the relative sasa value
INFILE = open("wild_relsasa.txt","r")
for LINE in INFILE:
    in1, in2, in3, *junk  = [x.strip() for x in LINE.split(",")]
    resnum             = int(in1)
    resnumber[resnum]  = int(in1)
    resname[resnum]    = in2
    relsasa[resnum]    = float(in3)
INFILE.close()

# Now we allocate the consurf values
INFILE = open("wild_consurf.txt","r")
for LINE in INFILE:
    in1, in2 = [x.strip() for x in LINE.split()]
    resnum          = int(in1)
    consurf[resnum] = int(in2)
INFILE.close()


# Now we allocate the energy values
INFILE = open("stability.txt","r")
for LINE in INFILE:
    j1, in0, in1, in2, in3, in4, in5, in6 = [x.strip() for x in LINE.split()]
    resnum           = int(in0)
    int_stab[resnum] = float(in1)
    vdw_stab[resnum] = float(in2)
    ele_stab[resnum] = float(in3)
    pol_stab[resnum] = float(in4)
    npl_stab[resnum] = float(in5)
    position[resnum] = resnum
    if max_resnum < resnum: max_resnum = resnum
    if min_resnum > resnum: min_resnum = resnum
INFILE.close()

#At this point we need to go through the data and look for the upper and lower gas phase energies
for j in range(min_resnum,max_resnum+1):
    gas_ene[j] = int_stab[j] + vdw_stab[j] + ele_stab[j]
    if j == min_resnum: upper = gas_ene[j]
    if j == min_resnum: lower = gas_ene[j]
    if gas_ene[j] > upper: upper = gas_ene[j]
    if gas_ene[j] < lower: lower = gas_ene[j]
ene_range   = upper - lower
bin_width = ene_range / 10
#print(upper,lower,ene_range, bin_width)

# Here we sort them into 9 ranks of equal energy widths in case we use this method
for j in range(min_resnum,max_resnum+1):
    rank[j] = 10
    for k in range(0,10):
        if gas_ene[j] > (lower + (bin_width * k)):
            rank[j] = k +1

# Here try to sort the residues based on gas_energies, posiiton should now run from lowest E to highest E
#for j in range(0,i):
unsorted = 1
while unsorted == 1:
    unsorted = 0
    for k in range(0,max_resnum):
        if gas_ene[position[k]] > gas_ene[position[k+1]]:
            temp_pos       = position[k]
            position[k]    = position[k+1]
            position[k+1]  = temp_pos
            unsorted       = 1
    if unsorted == 0:
        break

# Now we need to rerank according to the energies, equal # of residues in each band
band_width = (max_resnum-min_resnum)/10  # We are sorting into 10 groups
for k in range(0,10):
    lower_loop=int(band_width * k)
    upper_loop=int(band_width * (k+1)) + 1
    #print("lower",lower_loop, upper_loop,k)
    for j in range(lower_loop,upper_loop):
        rerank[position[j]] = k +1
        

# Print out the results table
print("Resi Ty cons   int    vdw    ele    pol    npl   sasa  gas_e rank  rern max min")
for j in range(min_resnum,max_resnum+1):
        max = rerank[j] + consurf[j] 
        min = rerank[j] - consurf[j] 
        # We set ACE/NME max/min to 5 and consurf to 0 to ignore them
        if resname[j] == "ACE" or resname[j] == "NME":
            max = 5
            min =5
            consurf[j] = 0
        print("{:>4}".format(resnumber[j]), "{:>3}".format(resname[j]), "  {:>1}".format(consurf[j]),\
              "{:6.1f}".format(int_stab[j]), "{:6.1f}".format(vdw_stab[j]), "{:6.1f}".format(ele_stab[j]), "{:6.1f}".format(pol_stab[j]),\
              "{:6.1f}".format(npl_stab[j]), "{:6.1f}".format(relsasa[j]),"{:6.1f}".format(gas_ene[j]), "  {:>2}".format(rank[j]),\
              "   {:>2}".format(rerank[j]), "{:>3}".format(max),  "{:>3}".format(min))
