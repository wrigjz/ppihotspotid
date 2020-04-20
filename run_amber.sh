#!/bin/bash
#########################################################################################################################
## and Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
#########################################################################################################################
# This is a script to take a chain, find the gaps and terminal residues, cao 
# them with ACE/NME, handle the protonation steate of HIS
# and then perform a energy minimization with amber
# followed by an internal energy evaluation for each residue

# set up the environment
source /home/programs/amber18/amber.sh
source /home/programs/anaconda/linux-5.3.6/init.sh
scripts=../critires_scripts

# Need to find broken ends and add TER and ACE and NME
/bin/rm -rf process.txt an_mini.pdb pre.pdb
# copy the pdb to a standard name to start with and remove hydrogens
#cp input.pdb pre.pdb   # copy the pdb to a standard name to start with
python3 $scripts/remove_h.py input.pdb pre.pdb
$AMBERHOME/bin/pdb4amber --reduce pre.pdb -o process.pdb > process.txt 2>&1
python $scripts/find_gaps.py process.pdb process.txt process1.pdb
$AMBERHOME/bin/tleap -f $scripts/leapin0
python3 $scripts/find_terminal.py process2.pdb processed.pdb
$AMBERHOME/bin/pdb4amber processed.pdb -o wild.pdb > wild 2>&1
sed -i -e 's/CYX/CYS/' -e 's/HID/HIS/' -e 's/HIE/HIS/' -e 's/HIP/HIS/' wild.pdb 
python $scripts/add_chain.py wild.pdb temp.pdb; mv temp.pdb wild.pdb

# start the actual amber/fed process
$AMBERHOME/bin/tleap -f $scripts/leapin1

export mpirun=/usr/local/openmpi-2.0.0_gcc48/bin/mpirun
$mpirun -n `wc -l < $PBS_NODEFILE` -machinefile $PBS_NODEFILE \
    $AMBERHOME/bin/sander.MPI -O -i $scripts/sander.in -p an.top -c an.crd -ref an.crd -o an_mini.out -r an_mini.res
#$AMBERHOME/bin/sander -O -i $scripts/sander.in -p an.top -c an.crd -ref an.crd -o an_mini.out -r an_mini.res

$AMBERHOME/bin/ambpdb -p an.top -c an_mini.res > an_mini.pdb
python $scripts/add_chain.py an_mini.pdb wild_mini.pdb
$AMBERHOME/bin/tleap -f $scripts/leapin2
$AMBERHOME/bin/MMPBSA.py -O -i $scripts/mm_pbsa.in -o FINAL_RESULTS_MMPBSA_wt.dat -do FINAL_DECOMP_MMPBSA_wt.dat -cp an_mini.top -y an_mini.crd


# to mutate $AMBERHOME/bin/pdb4amber an.pdb -m 17-ALA -o processed.pdb
# After processing may need to remove the TER
