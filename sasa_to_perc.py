#!/usr/bin/python

#
# This program reads a freesasa output file and then gives a percentage instead
# The standard values were taken from freesasa

import sys
import os

# This is the total SASA in the G-X-G tripeptide, we calc'd this ourselves
SASAHAS={
    'ASP' : int(160.32),
    'GLY' : int(87.75),
    'ACE' : int(121.09),
    'NME' : int(99.32),
    'PRO' : int(142.52),
    'THR' : int(149.97),
    'VAL' : int(160.21),
    'ALA' : int(116.69),
    'CYS' : int(141.27),
    'HIS' : int(192.75),
    'LEU' : int(193.72),
    'TRP' : int(257.93),
    'ARG' : int(250.60),
    'GLN' : int(193.09),
    'ILE' : int(185.80),
    'LYS' : int(214.48),
    'SER' : int(126.58),
    'TYR' : int(229.04),
    'ASN' : int(163.73),
    'GLU' : int(181.59),
    'MET' : int(199.65),
    'PHE' : int(214.27),
    'HID' : int(193.24),
    'HIE' : int(192.75),
    'HIP' : int(192.60),
    'CYX' : int(141.12),
}

# Get the input name from the command line
if len(sys.argv) == 1:
    print("Needs a argument with a output file\n")
    sys.exit(0)

# Open the sasa file,
SASAFILE = open(sys.argv[1],"r")

# simple way to assign result as an array sized 10000 with initial value -1
result = [-1] * 10000
i = int(0)

for SASALINE in SASAFILE:
    if SASALINE[0:3] != "SEQ":
        continue
    SASALINE     = SASALINE.rstrip()     # Perl Chomp
    SASASPLIT    = SASALINE.split(":")   # separate at the :
    residue      = SASALINE[12:15]
    temp         = SASASPLIT[1].replace(" ","")
    sasadom      = (SASAHAS.get(residue))
    relsasa      = (float(temp) / sasadom)*100       # calculate the relative sasa
    print(SASALINE[0:10],SASALINE[11:24]," : {:7.2f}".format(relsasa))
    
    


