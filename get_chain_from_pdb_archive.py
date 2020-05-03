#!/usr/bin/python
# Simple program to read PDB codes with chain eg 1tsr B and then copies that pdb file
# and extracts the chain to a new pdb file in a directory named
# after the pdb code and chain e.g. for 1STR chain B your would get
# 1tsrb/original.pdb 1tsrb/1tsrb.pdb


import sys
import os

if len(sys.argv) == 1:
    print("Needs a argument with the list of PDB files to extract the chain from")
    sys.exit(0)

LISTFILE = open(sys.argv[1], "r")

# Process the pdb id chain id list file
for LIST in LISTFILE:
    PDB, CHAIN, *junk = [x.strip() for x in LIST.split()]
    pdblc = PDB.lower()
    chainlc = CHAIN.lower()
    chainuc = CHAIN.upper()
    pdbchain = pdblc + chainlc
    tempin = pdbchain + "/original.pdb"
    middle = pdblc[1:3]
    tempout = pdbchain + "/initial.pdb"
    if not os.path.exists(pdbchain):
        os.mkdir(pdbchain)
    if os.path.exists(tempin):
        os.remove(tempin)
#/home/programs/pdb_copy/pdb/ts/pdb1tsr.ent.gz
    tempcmd = "gunzip -c /home/programs/pdb_copy/pdb/" + middle + "/pdb" + pdblc + \
              ".ent.gz" + " > " + pdbchain + "/original.pdb"
    os.system(tempcmd)
# loop over all the lines in the pdb file looking for what we want
    INFILE = open(tempin, "r")
    OUTFILE = open(tempout, "w")
    ENDMDL = 0
    for LINE in INFILE:
        if LINE[0:6] == "ENDMDL" and found_chain == 1:# We're found the chain and now ENDMDL
            print("All done")
            break
        if LINE[0:4] == "ATOM" or LINE[0:3] == "TER":
            if LINE[21:22] == chainuc:  # We only want our chain
                found_chain = 1         # we only want the first NMR model too
                if LINE[16:17] == " ": # We only want the A or only atomic positions
                    OUTFILE.write(LINE)
                if LINE[16:17] == "A":
                    LINE = LINE[:16] + " " + LINE[17:]
                    OUTFILE.write(LINE)
    INFILE.close()
    OUTFILE.close()
