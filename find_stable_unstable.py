#!/usr/bin/python3
#########################################################################################################################
## and Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
#########################################################################################################################
# Simple script to try take the assembled data
# and then locate the top 4 (or equal) Max and bottom 4 (or equal) min values
# from column 14 and 15
# discard any that have a sasa < a cutoff
# then look for any Stable residues vdw bonded to an Unstable residue
# Then look for any other residues (SASA > cutoff) that is vdw bonded to the Stab/UnStab pairs

# Stable are the low numbers e.g. energy rank - high consurf = v negative (min)
# Unstable are the high numbers e.g. energy rank + high consurf = v positive (max)

#Resi Ty bind cons   int    vdw    ele    pol    npl   sasa  gas_e rank  rern max min cle
#  1 ACE    0   0   32.0   -0.6  -13.8   -0.3   -0.3   71.3   17.6    3     1   1   1   0
import sys
from pprint import pprint

index = 0
# Open the assemble file and create the needed arrays
INFILE = open("assemble.txt","r")
for LINE in INFILE:
    if LINE[0:4] != "Resi":
        index += 1
INFILE.seek(0)

# We initilize the arrays we need
resname   = [0 for i in range(0,index)]
resnumber = [0 for i in range(0,index)]
relsasa   = [0 for i in range(0,index)]
int_stab  = [0 for i in range(0,index)]
vdw_stab  = [0 for i in range(0,index)]
ele_stab  = [0 for i in range(0,index)]
pol_stab  = [0 for i in range(0,index)]
npl_stab  = [0 for i in range(0,index)]
consurf   = [0 for i in range(0,index)]
gas_ene   = [0 for i in range(0,index)]
rank      = [0 for i in range(0,index)]
grade    = [1 for i in range(0,index)]
max_value = [0 for i in range(0,index)]
min_value = [0 for i in range(0,index)]
stable_name     = [0 for i in range(0,index)]
stable_number   = [0 for i in range(0,index)]
unstable_name   = [0 for i in range(0,index)]
unstable_number = [0 for i in range(0,index)]
max_resnum = 0
min_resnum = 1000
sasa_cutoff = float(0.0)

index = -1
for LINE in INFILE:
    if LINE[0:4] != "Resi":
        index += 1
        resnumber[index], resname[index], in3, int_stab[index], vdw_stab[index], \
            ele_stab[index], pol_stab[index], npl_stab[index], in0, gas_ene[index], rank[index], \
            grade[index], in1, in2 = [x.strip() for x in LINE.split()]
        consurf[index]      = int(in3)
        relsasa[index]      = float(in0)
        max_value[index]    = int(in1)
        min_value[index]    = int(in2)
INFILE.close()

# Here we merge the resnumber, resname, max, min and relsasa into a tuple
# and then remove where sasa <= cutoff
merged_list_sasa = tuple(zip(resnumber, resname, max_value, min_value, relsasa))
merged_list      = list(filter(lambda a: a[4] > sasa_cutoff, merged_list_sasa)) # Remove 0 values from network list
merged_list_len  = len(merged_list)

# Here we sort that tuple by the max and min numbers
max_array = sorted(merged_list, key=lambda x: x[2], reverse=True)
min_array = sorted(merged_list, key=lambda x: x[3])

#pprint(min_array)

# At this point we need to print out at the very least the top 4 residues and then any residues with equal scores
# to make sure there is a minimum of 4 printed
# So get the max and min value for the 4rd ranked residue, 
# then look for residues with a higher or equal max value, and residue with a lower or equal min value
max_number = max_array[3][2]
min_number = min_array[3][3]
#print(max_number, min_number)
index_st = -1
index_un = -1

#print("Stable conserved")
for i in range(0,merged_list_len):
    if max_array[i][2] >= max_number:
        index_st += 1
        name   = max_array[i][1]
        number = max_array[i][0]
        print("{:>3},".format(name), "{:>3},".format(number),"Stable")
        stable_name[index_st]   = name
        stable_number[index_st] = int(number)

#print("Unstable conserved")
for i in range(0,merged_list_len):
    if min_array[i][3] <= min_number:
        index_un += 1
        name   = min_array[i][1]
        number = min_array[i][0]
        print("{:>3},".format(name), "{:>3},".format(number),"Unstable")
        unstable_name[index_un]   = name
        unstable_number[index_un] = int(number)

# Okay now we look for stable ----vdw --- unstable pairs
# Start by reading in the NB2 file

#X0002-PRO N   X0001-ACE CH3 2.46 MH  -2 -1.00  -1.0 -1.00  -1.0  27.8     1
# Get an idea of the potential number of lines we will be dealing with
index_nb2 = -1
NB2FILE = open("wild_noh.nb2","r")
for LINE in NB2FILE:
    if LINE[0:1] == "X":
        index_nb2 += 1
residue1 = [0 for i in range(0,index_nb2+1)]
residue2 = [0 for i in range(0,index_nb2+1)]
network  = [0 for i in range(0,index_nb2+1)]
NB2FILE.seek(0)

# Now read in the vdw pairs fro the nb2 file and discard duplicates
index_nb2 = -1
for LINE in NB2FILE:
    if LINE[0:1] == "X":
        temp1 = int(LINE[1:5])
        temp2 = int(LINE[15:19])
        # Check if this pairing has been seen before
        marker = 0
        for i in range(0,index_nb2+1):
            if temp1 == residue1[i] and temp2 == residue2[i]:
                marker = 1
        # This is a new pair so we will save it
        if marker == 0:
            index_nb2 += 1
            residue1[index_nb2] = temp1
            residue2[index_nb2] = temp2

# Set up an array to save the pairs for the network residues
saved_residue1 = [0 for i in range(0,index_nb2+1)]
saved_residue2 = [0 for i in range(0,index_nb2+1)]
#print(index_st, index_un, index_nb2)

# Now we do the actual search for the Stable/Unstable vdw bonded pairs (Matrix residues)
matrix_number = -1
for k in range(0,index_nb2+1):
        for i in range(0,index_st+1):
            for j in range(0,index_un+1):
                if (stable_number[i] == residue1[k] and unstable_number[j] == residue2[k]) or \
                   (stable_number[i] == residue2[k] and unstable_number[j] == residue1[k]):
                       #print("Matrix Pair", stable_name[i], stable_number[i], unstable_name[j], unstable_number[j])
                       matrix_number += 1
                       saved_residue1[matrix_number] = stable_number[i]
                       saved_residue2[matrix_number] = unstable_number[j]

# New we need to look for the network residues which are connected to either one of the 
# Stable / Unstable Matrix pairs
#print("Network residues")
index_net = -1
for i in range(0,matrix_number+1):
    for j in range(0,index_nb2+1):
        if saved_residue1[i] == residue1[j] or saved_residue2[i] == residue1[j]:
            #print(residue2[j])
            index_net += 1
            network[index_net] = int(residue2[j])
        if saved_residue1[i] == residue2[j] or saved_residue2[i] == residue2[j]:
            #print(residue1[j])
            index_net += 1
            network[index_net] = int(residue1[j])

# Now try to remove network residues that are duplicates of the stable residues
for i in range(0,index_net+1):
    for j in range(0,index_st+1):
        if network[i] == stable_number[j]:
            #print("Forgotten Stable",network[i])
            network[i] = 0

# Now try to remove network residues that are duplicates of the unstable residues
for i in range(0,index_net+1):
    for j in range(0,index_un+1):
        if network[i] == unstable_number[j]:
            #print("Forgotten Unstable",network[i])
            network[i] = 0

# Now try to remove any duplicate network residues
for i in range(0,index_net+1):
    for j in range(i+1,index_net+1):
        if network[i] == network[j]:
            #print("Forgotten Network",network[i])
            network[i] = 0

# Now we order the Network residues, disgard any that are not 0, print what is left
network1 = list(filter(lambda a: a != 0, network)) # Remove 0 values from network list
network1.sort()  # sort network list
for line in network1:
    # Need to use -1 below because python arrays start at 0
    if relsasa[line-1] > sasa_cutoff and consurf[line-1] == 9 : # only print if relasas > cutoff, and consurf = 9
        print("{:>3},".format(resname[line-1]), "{:>3},".format(resnumber[line-1]),"Bridge")
