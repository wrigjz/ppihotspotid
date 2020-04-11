#!/bin./python
import sys

# This file will read the process.txt file from pdb4amber and 
# look for the gaps, it will then add the TER line after each gap
# Because of the size of the ACE and NME groups we only take gaps >= 3.3Angs 

if len(sys.argv) < 4:
    print ("Please give input pdb file, pdb4amber output and output file")
    exit()

INPDB   = open(sys.argv[1],"r")
PROCESS = open(sys.argv[2],"r")
OUTPDB  = open(sys.argv[3],"w")

index = -1
upper = [0 for i in range(0,10000)]

# Process the pdb4amber output and look for the gaps
# tore the upper residue for each gap
for LINE in PROCESS:
    test = len([x.strip() for x in LINE.split()])
    if test != 10:
        continue
    gap, of, dist, angs, between, resna1, resid1, junk, resna2, resid2 = [x.strip() for x in LINE.split()]
    if gap == "gap" and resid1 != resid2:
        if float(dist) >= 3.3:  # big enough gap to terminal with ACE/NME
            index += 1
            upper[index] = int(resid2)
            print("Terminating index: ", index, " Before: ", upper[index])

# Now process the PDB file, when we find the upper residue for the 1st time
# We print and "TER" line
for TMLINE in INPDB:
    if TMLINE[0:6] == "CONECT":
            continue
    if TMLINE[0:4] == "ATOM":
        resid_long  = TMLINE[23:27]
        resid       = resid_long.replace(" ","") # Remove whitespace from resid
        for i in range(0,index+1):
            if int(resid) == upper[i] and TMLINE[12:15] == " N ":
                OUTPDB.write("TER\n")
                print("Performing: ", i)
        OUTPDB.write(TMLINE)
    else:
        OUTPDB.write(TMLINE)
    # gap of 4.045442 A between ASP 120 and ARG 121
