#!/bin/bash
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
# This is a script to take a chain, find the gaps and terminal residues, cao
# them with ACE/NME, handle the protonation steate of HIS
# and then perform a energy minimization with amber
# followed by an internal energy evaluation for each residue

# set up the environment
source /home/programs/ambertools20/amber20/amber.sh
source /home/programs/anaconda/linux-5.3.6/init.sh
scripts=../critires_scripts

# Need to find broken ends and add TER and ACE and NME
/bin/rm -rf process.txt post_mini.pdb initial.pdb

# renumber the pdb and make it a standard name to start with, plus remove hydrogens
python3 $scripts/renum_rm_h.py input.pdb initial.pdb renumber.txt

# Run with --reduce to get an idea of HIS protonation states
$AMBERHOME/bin/pdb4amber --reduce --noter initial.pdb -o process.pdb >| process.txt 2>&1
python3 $scripts/find_gaps.py process.pdb process.txt process1.pdb

$AMBERHOME/bin/tleap -f $scripts/leapin0
python3 $scripts/add_ace_nme.py process2.pdb processed.pdb


# Generate the final leapin1 file
cat >| leapin1 << EOF2
source leaprc.protein.ff19SB
set default PBradii mbondi2
trx = loadpdb processed.pdb
EOF2
python3 $scripts/disu.py processed.pdb >> leapin1
cat >> leapin1 << EOF3
saveamberparm trx mini.top pre_mini.crd
quit
EOF3

# start the actual amber/fed process
$AMBERHOME/bin/tleap -f leapin1

# Run this to get the renumbering scheme we need later
$AMBERHOME/bin/pdb4amber processed.pdb -o pre_mini.pdb  >| pre_mini.txt 2>&1

# Check if we are on the cluster
if [ -z "$PBS_NODEFILE" ] ; then
    echo "Non cluster run"
    $AMBERHOME/bin/sander -O -i $scripts/sander.in -p mini.top -c pre_mini.crd -ref pre_mini.crd \
        -o post_mini.out -r post_mini.res
else
    echo "Cluster run"
    export mpirun=/usr/local/openmpi-2.0.0_gcc48/bin/mpirun
    $mpirun -n `wc -l < $PBS_NODEFILE` -machinefile $PBS_NODEFILE \
    $AMBERHOME/bin/sander.MPI -O -i $scripts/sander.in -p mini.top -c pre_mini.crd -ref pre_mini.crd \
        -o post_mini.out -r post_mini.res
fi

$AMBERHOME/bin/ambpdb -p mini.top -c post_mini.res >| post_mini.pdb
python $scripts/add_chain.py post_mini.pdb post_minix.pdb
$AMBERHOME/bin/MMPBSA.py -O -i $scripts/mm_pbsa.in -o FINAL_RESULTS_MMPBSA_wt.dat \
          -do FINAL_DECOMP_MMPBSA_wt.dat -cp mini.top -y post_mini.res
