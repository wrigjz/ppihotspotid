#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################

# This script take the stable/unstable results and then maps them back to the original PDB numbers

# Get the local dircetory and add it to the module search path
from numbers import NUMBERS

CHAINFILE = open("original_chain.txt")
for CHAINLINE in CHAINFILE:
    chain = CHAINLINE.strip()
CHAINFILE.close()

#GLU,  84, Unstable
INFILE = open("results_ambnum.txt")
for LINE in INFILE:
    resname, resnumber, crititype = [x.strip() for x in LINE.split(",")]
    original = (NUMBERS.get(resnumber))
    if original is None:
        original = "NaN"
    print("{:3s}".format(resname), "{:>4}".format(original), "{:1s}".format(chain), \
          "{:8s}".format(crititype))
INFILE.close()
