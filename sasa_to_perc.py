#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
#
# This program reads a freesasa output file and then gives a percentage instead
# The "standard" values were taken using freesasa on Amber minimized Me-X-Me tripeptides
# to be consistent with the unfilding energies used elsewhere

import sys

SASATAB = {
    'ASP' : float(160.46),
    'GLY' : float(86.07),
    'PRO' : float(142.79),
    'THR' : float(152.87),
    'VAL' : float(162.36),
    'ALA' : float(115.28),
    'CYS' : float(145.10),
    'HIS' : float(198.65),
    'LEU' : float(193.09),
    'TRP' : float(263.02),
    'ARG' : float(254.28),
    'GLN' : float(196.21),
    'ILE' : float(188.05),
    'LYS' : float(219.01),
    'SER' : float(125.30),
    'TYR' : float(235.78),
    'ASN' : float(167.91),
    'GLU' : float(187.27),
    'MET' : float(201.98),
    'PHE' : float(221.01),
    'HID' : float(199.07),
    'HIE' : float(198.65),
    'HIP' : float(199.04),
    'CYX' : float(90.87),
    'CYM' : float(143.45),
    'ACE' : float(121.14),
    'NME' : float(99.49),
}

# Get the input name from the command line
if len(sys.argv) == 1:
    print("Needs a argument giving a freesasa output file\n")
    sys.exit(0)

# Open the sasa file,
SASAFILE = open(sys.argv[1], "r")
#i = int(0)

for SASALINE in SASAFILE:
    if SASALINE[0:3] != "SEQ":
        continue
    SASALINE = SASALINE.rstrip()     # Remove spaces at end of line, newline etc
    SASASPLIT = SASALINE.split(":")   # separate at the :
    residue = SASALINE[12:15]
    calcsasa = SASASPLIT[1].replace(" ", "") # Remove any spaces
    tripsasa = (SASATAB.get(residue))
    relsasa = (float(calcsasa) / tripsasa)*100       # calculate the relative sasa
    print(SASALINE[0:10], SASALINE[11:24], " : {:7.2f}".format(relsasa))
