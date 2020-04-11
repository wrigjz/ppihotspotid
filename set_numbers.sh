#1/bin/bash

# This script sets up a HASH mapping the original pdb numbers to the amber numbers
# It is run after Amber has capped the gaps etc

echo "NUMBERS = {" >| numbers.py
grep -v ACE wild_renum.txt |grep -v NME|paste - process_renum.txt|awk '{print "\x27"$4"\x27 : \x27"$6"\x27 ,"}' >> numbers.py
echo "}" >> numbers.py
