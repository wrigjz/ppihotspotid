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
#

if len(sys.argv) < 3:
    print("Please give input and output files")
    exit()

INPDB = open(sys.argv[1], "r")
OUTPDB = open(sys.argv[2], "w")

# Now process the PDB file,
# When we find the " H2 " line we need to convert this to "ACE  C" and change the resid number too
# We save this for the 2nd time we process the PDB file
INDEX = -1
ACE = [0 for i in range(0, 100)]
ACE_RESID = ["" for i in range(0, 100)]
for TMLINE in INPDB:
    if TMLINE[12:16] == " H2 ":  # This also covers the NPRO case
        INDEX += 1
        resid_long = TMLINE[22:26] # We shouldn't need to worry about A/B residues
        resid = resid_long.replace(" ", "") # Remove whitespace from resid
        resid = int(resid) - 1
        ACE[INDEX] = TMLINE[0:13] + "C   ACE  " + "{:>4}".format(resid) + "B" + TMLINE[27:66]
        ACE_RESID[INDEX] = resid


# We also need to find the H2 atom for 1st residue each time and change that to ACE
# When we find an OXT we convert that to NME
#ATOM    605  C   ACE    36B     68.635  22.680  59.599  1.00  0.00
INPDB.seek(0)
i = 0
OUTPDB.write(ACE[0]+"\n")
for TMLINE in INPDB:
    # If we find a ATOM line but it's not H1/2/3 OXT we write it out
    if TMLINE[0:4] == "ATOM" and TMLINE[13:16] != "OXT" and TMLINE[12:16] != " H2 " \
                             and TMLINE[12:16] != " H1 " and TMLINE[12:16] != " H3 ":
        saved_line = TMLINE
        OUTPDB.write(TMLINE)
        saved_id = int(TMLINE[22:26]) # We shouldn't need to worry about A/B residues
    # If we find a TER line we then write out the corresponding ACE #
    if TMLINE[0:3] == "TER":
        OUTPDB.write(TMLINE)
        for i in range(1, INDEX+1):  # This bit of code looks for previously saved ACE lines
                                     # and write out the right one
            resid_check = ACE_RESID[i]
            if resid_check == saved_id:
                OUTPDB.write(ACE[i]+"\n")
    if TMLINE[13:16] == "OXT":  # Change this to a NME group
        #resid_long  = TMLINE[22:26] # We shouldn't need to worry about A/B residues
        fred = TMLINE[0:13] + "N   NME  " + TMLINE[22:26] + "A" + TMLINE[27:66]
        OUTPDB.write(fred+"\n")
