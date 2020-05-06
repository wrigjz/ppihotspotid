#!/bin/bash
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
# This script sets up a HASH mapping the original pdb numbers to the amber numbers
# It is run after Amber has capped the gaps etc

echo "NUMBERS = {" >| numbers.py
grep -v ACE pre_mini_renum.txt |grep -v NME|paste - renumber.txt| \
       awk '{print "\x27"$4"\x27 : \x27"$6"\x27 ,"}' >> numbers.py
echo "}" >> numbers.py
