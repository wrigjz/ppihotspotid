#!/usr/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
#
# This program reads a freesasa output file and then gives a percentage instead
# The standard values were taken from freesasa

import sys

SASATAB = { # This is the total SASA in the G-X-G tripeptide, we calc'd this ourselves
    'ASP' : '160.46',
    'GLY' : '86.07',
    'PRO' : '142.79',
    'THR' : '152.87',
    'VAL' : '162.36',
    'ALA' : '115.28',
    'CYS' : '145.10',
    'HIS' : '198.65',
    'LEU' : '193.09',
    'TRP' : '263.02',
    'ARG' : '254.28',
    'GLN' : '196.21',
    'ILE' : '188.05',
    'LYS' : '219.01',
    'SER' : '125.30',
    'TYR' : '235.78',
    'ASN' : '167.91',
    'GLU' : '187.27',
    'MET' : '201.98',
    'PHE' : '221.01',
    'HID' : '199.07',
    'HIE' : '198.65',
    'HIP' : '199.04',
    'CYX' : '144.44',
    'ACE' : '121.14',
    'NME' : '99.49',
}

# Get the input name from the command line
if len(sys.argv) == 1:
    print("Needs a argument with a output file\n")
    sys.exit(0)

# Open the sasa file,
SASAFILE = open(sys.argv[1], "r")
i = int(0)

for SASALINE in SASAFILE:
    if SASALINE[0:3] != "SEQ":
        continue
    SASALINE = SASALINE.rstrip()     # Perl Chomp
    SASASPLIT = SASALINE.split(":")   # separate at the :
    residue = SASALINE[12:15]
    temp = SASASPLIT[1].replace(" ", "")
    sasadom = (SASATAB.get(residue))
    relsasa = (float(temp) / sasadom)*100       # calculate the relative sasa
    print(SASALINE[0:10], SASALINE[11:24], " : {:7.2f}".format(relsasa))
