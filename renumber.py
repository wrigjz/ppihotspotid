#!bin/python
#########################################################################################################################
## and Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
#########################################################################################################################
import sys

# Quick and dirty script to renumber Backy's output to the pdb2amb output

renumfile = open(sys.argv[1],"r")
critifile = open(sys.argv[2],"r")


saved = [0 for i in range(0,1000)]

for LINE in renumfile:
    junk1, old, junk2, new = [x.strip() for x in LINE.split()]
    index        = int(old)
    saved[index] = int(new)

for LINE in critifile:
    junk1, junk2, junk3, old = [x.strip() for x in LINE.split()]
    index=int(old)
    print(junk1, junk2, junk3, old, saved[index])
