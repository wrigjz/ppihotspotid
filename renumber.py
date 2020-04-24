#!bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
import sys

# Quick and dirty script to renumber Backy's output to the pdb2amb output

RENUMFILE = open(sys.argv[1], "r")
CRITIFILE = open(sys.argv[2], "r")

SAVED = [0 for i in range(0, 2000)]

for LINE in RENUMFILE:
    junk1, old, junk2, new = [x.strip() for x in LINE.split()]
    index = int(old)
    SAVED[index] = int(new)

for LINE in CRITIFILE:
    junk1, junk2, junk3, old = [x.strip() for x in LINE.split()]
    index = int(old)
    print(junk1, junk2, junk3, old, SAVED[index])
