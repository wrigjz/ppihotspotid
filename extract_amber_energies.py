#!/bin./python
#########################################################################################################################
## and Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
#########################################################################################################################
import sys

# This file will read the AMBER MM_PBSA DECOMP files, it then calculates 
# the difference from a standard value for each of the required energies for each residue
#
# to use try something like python3 find_stable_energy.py
# 
# File will be: FINAL_DECOMP_MMPBSA_wt.dat
#

# Get a line count for the arrays we need
num_lines = 0
num_lines += sum(1 for lines in open("FINAL_DECOMP_MMPBSA_wt.dat","r"))

WTTYPE  = open("FINAL_DECOMP_MMPBSA_wt.dat","r")
OUTPUT  = open("stability.txt","w")


EELTAB = {  # We calc'd these outselves from Me-X-Me
'ASP' : '-38.591',
'GLY' : '-49.555',
'PRO' : '-37.943',
'THR' : '-22.861',
'VAL' : '-27.471',
'ALA' : '-50.757',
'CYS' : '-42.982',
'HIE' : '-61.397',
'LEU' : '-45.581',
'TRP' : '-59.728',
'ARG' : '107.542',
'GLN' : '-42.194',
'ILE' : '-43.049',
'LYS' : '-40.891',
'SER' : '-42.255',
'TYR' : '-55.219',
'ASN' : '-65.785',
'GLU' : '-49.076',
'MET' : '-47.859',
'PHE' : '-50.074',
'HID' : '-42.864',
'HIE' : '-61.397',
'HIP' : '-21.521',
'CYX' : '-47.977',
'ACE' : '-9.049',
'NME' : '-17.801',
}

INTTAB = {  # We calc'd these outselves from Me-X-Me
'ASP' : '54.655',
'GLY' : '46.117',
'PRO' : '53.771',
'THR' : '6.258',
'VAL' : '11.833',
'ALA' : '53.451',
'CYS' : '49.609',
'HIE' : '72.191',
'LEU' : '27.334',
'TRP' : '73.269',
'ARG' : '-231.077',
'GLN' : '-8.094',
'ILE' : '46.220',
'LYS' : '84.830',
'SER' : '45.315',
'TYR' : '42.500',
'ASN' : '-2.957',
'GLU' : '61.338',
'MET' : '50.525',
'PHE' : '54.401',
'HID' : '58.295',
'HIE' : '72.191',
'HIP' : '96.529',
'CYX' : '49.062',
'ACE' : '-23.196',
'NME' : '23.456',
}

VDWTAB = {  # We calc'd these outselves from Me-X-Me
'ASP' : '-1.594',
'GLY' : '-0.123',
'PRO' : '-0.346',
'THR' : '-1.015',
'VAL' : '-0.863',
'ALA' : '-0.521',
'CYS' : '-0.869',
'HIE' : '-2.271',
'LEU' : '-1.192',
'TRP' : '-3.184',
'ARG' : '-1.962',
'GLN' : '-1.313',
'ILE' : '-0.736',
'LYS' : '-1.420',
'SER' : '-0.727',
'TYR' : '-2.590',
'ASN' : '-1.429',
'GLU' : '-1.687',
'MET' : '-1.422',
'PHE' : '-2.419',
'HID' : '-2.282',
'HIE' : '-2.271',
'HIP' : '-2.289',
'CYX' : '-0.861',
'ACE' : '-0.366',
'NME' : '-0.243',
}

NPOLTAB = {  # We calc'd these outselves from Me-X-Me
'ASP' : '1.230',
'GLY' : '0.669',
'PRO' : '1.113',
'THR' : '1.204',
'VAL' : '1.254',
'ALA' : '0.912',
'CYS' : '1.141',
'HIE' : '1.549',
'LEU' : '1.481',
'TRP' : '2.075',
'ARG' : '1.983',
'GLN' : '1.524',
'ILE' : '1.451',
'LYS' : '1.779',
'SER' : '1.026',
'TYR' : '1.856',
'ASN' : '1.296',
'GLU' : '1.417',
'MET' : '1.544',
'PHE' : '1.708',
'HID' : '1.528',
'HIE' : '1.549',
'HIP' : '1.581',
'CYX' : '1.111',
'ACE' : '0.905',
'NME' : '0.773',
}

EPOLTAB = {  # We calc'd these outselves from Me-X-Me
'ASP' : '-86.015',
'GLY' : '-7.832',
'PRO' : '-7.245',
'THR' : '-12.858',
'VAL' : '-6.825',
'ALA' : '-7.225',
'CYS' : '-8.115',
'HIE' : '-16.681',
'LEU' : '-7.399',
'TRP' : '-13.347',
'ARG' : '-65.120',
'GLN' : '-20.627',
'ILE' : '-6.696',
'LYS' : '-73.659',
'SER' : '-14.447',
'TYR' : '-13.850',
'ASN' : '-15.846',
'GLU' : '-80.076',
'MET' : '-8.932',
'PHE' : '-9.031',
'HID' : '-17.288',
'HIE' : '-16.681',
'HIP' : '-69.157',
'CYX' : '-6.974',
'ACE' : '-7.025',
'NME' : '-2.039',
}


found      = 0
count      = 0
res_energy = [0 for i in range(0,num_lines)]
res_type   = [0 for i in range(0,num_lines)]
res_number = [0 for i in range(0,num_lines)]
res_solv   = [0 for i in range(0,num_lines)]

vdw_std    = [0 for i in range(0,num_lines)]
elec_std   = [0 for i in range(0,num_lines)]
int_std    = [0 for i in range(0,num_lines)]
pol_std    = [0 for i in range(0,num_lines)]
npol_std   = [0 for i in range(0,num_lines)]

# Process the MM_PBSA Decomp file and look for the residues

for WTENERGY in WTTYPE:
    test = len([x.strip() for x in WTENERGY.split()])
    if WTENERGY[0:20] == "--------------------": # looking for the start of the data section
        found = 1
        continue
    if test < 10:  # Line is not long enough
        continue
    if found == 1:
# We can not use split here because the number of residues can be > 10000
        temp1 = WTENERGY[0:3]
        temp2 = temp1.strip()
        resname = str(temp2)
        temp1 = WTENERGY[3:8]
        temp2 = temp1.strip()
        resid = int(temp2)
        temp1 = WTENERGY[9:19]
        temp2 = temp1.strip()
        internal = float(temp2)
        temp1 = WTENERGY[31:41]
        temp2 = temp1.strip()
        vdw = float(temp2)
        temp1 = WTENERGY[53:63]
        temp2 = temp1.strip()
        elec = float(temp2)
        temp1 = WTENERGY[75:85]
        temp2 = temp1.strip()
        pol = float(temp2)
        temp1 = WTENERGY[97:107]
        temp2 = temp1.strip()
        npol = float(temp2)
        #print(resname,resid,internal,vdw,elec,pol,npol)
        res_type[count]   = resname
        res_number[count] = resid
        vdw_std[count]    = float(vdw)      - float(VDWTAB[resname])
        elec_std[count]   = float(elec)     - float(EELTAB[resname])
        int_std[count]    = float(internal) - float(INTTAB[resname])
        pol_std[count]    = float(pol)      - float(EPOLTAB[resname])
        npol_std[count]   = float(npol)     - float(NPOLTAB[resname])
        res_energy[count] = vdw_std[count] + elec_std[count] + int_std[count]
        res_solv[count]   = pol_std[count] + npol_std[count]
        count            += 1

#print("wt_tot",wt_total_ener,residue_ave,"wt_solv",wt_solv_tot,ressolv_ave)

#print(eel_ttl, eel_100, count)
for i in range(0,count):
     OUTPUT.write(res_type[i] + " {:>4}".format(res_number[i]) + " {:8.2f}".format(int_std[i]) + "{:8.2f}".format(vdw_std[i]) + "{:8.2f}".format(elec_std[i]) + "{:8.2f}".format(pol_std[i]) + "{:8.2f}".format(npol_std[i]) + "{:8.2f}".format(res_energy[i]) + "\n")
