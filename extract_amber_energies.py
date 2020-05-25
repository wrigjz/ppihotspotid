#!/bin/python3
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################

# This file will read the AMBER MM_PBSA DECOMP files, it then calculates
# the difference from a standard value for each of the required energies for each residue
#
# to use try something like python3 find_stable_energy.py
#
# File will be: FINAL_DECOMP_MMPBSA_wt.dat
#

# Get a line count for the arrays we need
NUM_LINES = 0
NUM_LINES += sum(1 for lines in open("FINAL_DECOMP_MMPBSA_wt.dat", "r"))

WTTYPE = open("FINAL_DECOMP_MMPBSA_wt.dat", "r")
OUTPUT = open("stability.txt", "w")

INTTAB = { # We calc'd these outselves from Me-X-Me
    'ASP' : '54.694',
    'GLY' : '46.117',
    'PRO' : '53.813',
    'THR' : '6.259',
    'VAL' : '11.726',
    'ALA' : '53.426',
    'CYS' : '49.530',
    'HIS' : '72.126',
    'LEU' : '27.330',
    'TRP' : '73.243',
    'ARG' : '-230.979',
    'GLN' : '-8.076',
    'ILE' : '46.220',
    'LYS' : '84.899',
    'SER' : '45.320',
    'TYR' : '42.499',
    'ASN' : '-2.926',
    'GLU' : '61.324',
    'MET' : '50.490',
    'PHE' : '54.301',
    'HID' : '58.234',
    'HIE' : '72.126',
    'HIP' : '96.460',
    'CYX' : '49.045',
    'ACE' : '-24.169',
    'NME' : '22.672',
}

VDWTAB = { # We calc'd these outselves from Me-X-Me
    'ASP' : '-1.583',
    'GLY' : '-0.111',
    'PRO' : '-0.335',
    'THR' : '-0.989',
    'VAL' : '-0.791',
    'ALA' : '-0.512',
    'CYS' : '-0.860',
    'HIS' : '-2.230',
    'LEU' : '-1.176',
    'TRP' : '-3.143',
    'ARG' : '-1.909',
    'GLN' : '-1.311',
    'ILE' : '-0.706',
    'LYS' : '-1.403',
    'SER' : '-0.721',
    'TYR' : '-2.538',
    'ASN' : '-1.404',
    'GLU' : '-1.676',
    'MET' : '-1.363',
    'PHE' : '-2.391',
    'HID' : '-2.239',
    'HIE' : '-2.230',
    'HIP' : '-2.264',
    'CYX' : '-0.850',
    'ACE' : '-0.371',
    'NME' : '-0.175',
}

EELTAB = { # We calc'd these outselves from Me-X-Me
    'ASP' : '-38.577',
    'GLY' : '-49.556',
    'PRO' : '-37.941',
    'THR' : '-22.866',
    'VAL' : '-27.405',
    'ALA' : '-50.731',
    'CYS' : '-42.884',
    'HIS' : '-61.313',
    'LEU' : '-45.576',
    'TRP' : '-59.687',
    'ARG' : '107.379',
    'GLN' : '-42.179',
    'ILE' : '-43.065',
    'LYS' : '-40.996',
    'SER' : '-42.244',
    'TYR' : '-55.226',
    'ASN' : '-65.777',
    'GLU' : '-48.953',
    'MET' : '-47.829',
    'PHE' : '-49.973',
    'HID' : '-42.813',
    'HIE' : '-61.313',
    'HIP' : '-21.475',
    'CYX' : '-47.969',
    'ACE' : '-9.018',
    'NME' : '-17.830',
}

EPOLTAB = { # We calc'd these outselves from Me-X-Me
    'ASP' : '-86.076',
    'GLY' : '-7.833',
    'PRO' : '-7.317',
    'THR' : '-12.872',
    'VAL' : '-6.809',
    'ALA' : '-7.232',
    'CYS' : '-8.142',
    'HIS' : '-16.692',
    'LEU' : '-7.395',
    'TRP' : '-13.350',
    'ARG' : '-65.080',
    'GLN' : '-20.657',
    'ILE' : '-6.691',
    'LYS' : '-73.644',
    'SER' : '-14.459',
    'TYR' : '-13.858',
    'ASN' : '-15.893',
    'GLU' : '-80.191',
    'MET' : '-8.913',
    'PHE' : '-9.045',
    'HID' : '-17.293',
    'HIE' : '-16.692',
    'HIP' : '-69.133',
    'CYX' : '-6.976',
    'ACE' : '-7.045',
    'NME' : '-2.029',
}

NPOLTAB = { # We calc'd these outselves from Me-X-Me
    'ASP' : '1.230',
    'GLY' : '0.666',
    'PRO' : '1.123',
    'THR' : '1.211',
    'VAL' : '1.251',
    'ALA' : '0.905',
    'CYS' : '1.144',
    'HIS' : '1.543',
    'LEU' : '1.482',
    'TRP' : '2.075',
    'ARG' : '1.981',
    'GLN' : '1.528',
    'ILE' : '1.439',
    'LYS' : '1.782',
    'SER' : '1.029',
    'TYR' : '1.856',
    'ASN' : '1.296',
    'GLU' : '1.413',
    'MET' : '1.539',
    'PHE' : '1.703',
    'HID' : '1.531',
    'HIE' : '1.543',
    'HIP' : '1.579',
    'CYX' : '1.105',
    'ACE' : '0.903',
    'NME' : '0.776',
}


FOUND = 0
COUNT = 0
RES_ENERGY = [0 for i in range(0, NUM_LINES)]
RES_TYPE = [0 for i in range(0, NUM_LINES)]
RES_NUMBER = [0 for i in range(0, NUM_LINES)]
RES_SOLV = [0 for i in range(0, NUM_LINES)]

VDW_STD = [0 for i in range(0, NUM_LINES)]
ELEC_STD = [0 for i in range(0, NUM_LINES)]
INT_STD = [0 for i in range(0, NUM_LINES)]
POL_STD = [0 for i in range(0, NUM_LINES)]
NPOL_STD = [0 for i in range(0, NUM_LINES)]

# Process the MM_PBSA Decomp file and look for the residues

for WTENERGY in WTTYPE:
    test = len([x.strip() for x in WTENERGY.split()])
    if WTENERGY[0:20] == "--------------------": # looking for the start of the data section
        FOUND = 1
        continue
    if test < 10:  # Line is not long enough
        continue
    if FOUND == 1:
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
        RES_TYPE[COUNT] = resname
        RES_NUMBER[COUNT] = resid
        VDW_STD[COUNT] = float(vdw) - float(VDWTAB[resname])
        ELEC_STD[COUNT] = float(elec) - float(EELTAB[resname])
        INT_STD[COUNT] = float(internal) - float(INTTAB[resname])
        POL_STD[COUNT] = float(pol) - float(EPOLTAB[resname])
        NPOL_STD[COUNT] = float(npol) - float(NPOLTAB[resname])
        RES_ENERGY[COUNT] = VDW_STD[COUNT] + ELEC_STD[COUNT] + INT_STD[COUNT]
        RES_SOLV[COUNT] = POL_STD[COUNT] + NPOL_STD[COUNT]
        COUNT += 1

#print("wt_tot",wt_total_ener,residue_ave,"wt_solv",wt_solv_tot,ressolv_ave)

#print(eel_ttl, eel_100, COUNT)
for i in range(0, COUNT):
    OUTPUT.write(RES_TYPE[i] + " {:>4}".format(RES_NUMBER[i]) + " {:9.3f}".format(INT_STD[i]) + \
        "{:9.3f}".format(VDW_STD[i]) + "{:9.3f}".format(ELEC_STD[i]) + \
        "{:9.3f}".format(POL_STD[i]) + "{:9.3f}".format(NPOL_STD[i]) + \
        "{:9.3f}".format(RES_ENERGY[i]) + "\n")
