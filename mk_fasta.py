#!/usr/bin/python

#This take a PDB file and then creates a file with a fasta format for a single chain
# It will ouput ACE/NME as X
# and write another file that allows for the final consurf numbering
# to be related back to the initial PDB file

import sys
import os

# Set initial values for a few variables
previous_resno       = "-999"
previous_resno_short = "-999"

# Look up table for converting 3 letter AA codes to single letter codes
RESIDUETAB = {
    'ALA' : 'A',
    'CYS' : 'C',
    'ASP' : 'D',
    'GLU' : 'E',
    'PHE' : 'F',
    'GLY' : 'G',
    'HIS' : 'H',
    'ILE' : 'I',
    'LYS' : 'K',
    'LEU' : 'L',
    'MET' : 'M',
    'ASN' : 'N',
    'PRO' : 'P',
    'GLN' : 'Q',
    'ARG' : 'R',
    'SER' : 'S',
    'THR' : 'T',
    'VAL' : 'V',
    'TYR' : 'Y',
    'TRP' : 'W',
    'CYS' : 'C',
    'CYX' : 'C',
    'HSP' : 'H',
    'HSD' : 'H',
    'HSE' : 'H',
    'HIP' : 'H',
    'HID' : 'H',
    'HIE' : 'H',
    'ACE' : 'X',
    'NME' : 'X',
}

# Get the output name from the command line
if len(sys.argv) == 1:
    print("Needs a argument with the list of PDB files to extract the chain from\n")
    sys.exit(0)

# Open the file,
INFILE = open(sys.argv[1],"r")
OUTFILE = open("r4s_pdb.py","w")
print (">PDB_ATOM")
index=0
r4sindex=0
OUTFILE.write("R4S_2_PDB={\n")
# Loop over each line of the input file splitting it into different columns
for TMLINE in INFILE:
    if TMLINE[0:4] == "ATOM" or TMLINE[0:6] == "HETATM":
    # Save the info we need for later
        resname     = TMLINE[17:20]
        atom_name   = TMLINE[12:16]
        chain       = TMLINE[21:22]
        resid_long  = str(TMLINE[23:27])
        # This block looks for a change in the residue number  , and prints out the 1 letter codes
        if previous_resno != resid_long:
            index += 1
            # Make a note of the residue number for the next line we look at
            previous_resno        = resid_long
            # Convert from 3 letter code to single letter code and print it out
            if resname in RESIDUETAB:
                single = str(RESIDUETAB.get(resname))
                print (single, end = "")
            else: 
                print (".", end = "")
            if single !="X": r4sindex+=1
            outline = "    '" + "{:>d}".format(r4sindex) + "' : '" + "{:>d}".format(index) + "' ,\n"
            OUTFILE.write(outline)
print ("") # print a newline to end the sequence output
OUTFILE.write("}")
