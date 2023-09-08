#!/bin/bash
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
# Simple script to perform a critires job
# You need to make sure that a input.pdb file exists in the directory
# and that you give a percentage for the number of residues to predict
# e.g. critires.sh 5

export hbplus=/home/programs/hbplus-3.06.linux/hbplus
export dssp=/home/programs/xssp-3.0.5/bin.linux/mkdssp
export freesasa=/home/programs/freesasa-2.03/linux/bin/freesasa
export scripts=../critires_scripts
export consurf_scripts=../consurf_scripts
source /home/programs/anaconda/linux_202307/init.sh
conda activate ag

if [ $# -eq 0 ]
    then
        echo "Please give a percentage for residues you want to predict as a total of the chain"
        echo "If you only want the most and least stable then set the percentage to 0"
        echo e.g. critires.sh 5
        exit
fi

# Start off by running checking for missing backbone atoms in the PDB file and running AMBER
python3 $scripts/check_bb.py input.pdb missing.txt
if [ -s missing.txt ] ; then
        echo "Input file has missing backbone atoms, please fix this"
        exit
fi
grep '^ATOM  ' input.pdb | tail -1 | cut -c22-22 >| original_chain.txt
$scripts/run_amber.sh

python3 $scripts/extract_amber_energies.py

# At this point we need to run consurf if we do not already have a consurf.grades file,
# use the two lines below to run it using the ATOM records to get the sequence
# This is the prefered option
$consurf_scripts/consurf_home.sh post_mini.pdb
PYTHONPATH=. python3 $scripts/get_consurf_home.py initial.grades consurf.txt

# Or if you want to run it locally using the SEQRES records use these lines
# But you make make sure that original.pdb and original_chain.txt exist
#$consurf_scripts/consurf_seqres.sh post_mini.pdb
#PYTHONPATH=. python3 $scripts/get_consurf_seqres.py seqres.fasta cons.fasta \
#             seqres.grades consurf.txt >| seqres.txt

# Or the alternative is to use the Consurf website grades, in which case use these
# lines below
#python3 ../$scripts/get_consurf_numbers.py post_mini.pdb
#PYTHONPATH=. python3 ../$scripts/get_consurf_web.py consurf.grades consurf.txt

# Just incase consurf failed create a dummy file
touch consurf.txt

# Sort out the SASA values
$freesasa --config-file $scripts/protor.config --format=seq post_minix.pdb >| post_mini.sasa
python3 $scripts/sasa_to_perc.py post_mini.sasa | awk '{print $3", "$4", "$8}' >| post_mini.relsasa

# Prepare a non-H atom version for hbplus
python3 $scripts/renum_rm_h.py post_minix.pdb post_mini_noh.pdb No
sed -i -e 's/CYX/CYS/' -e 's/CYM/CYS/' -e 's/HID/HIS/' -e 's/HIE/HIS/' -e 's/HIP/HIS/' post_mini_noh.pdb

# Run HBPLUS - needed for the vdw matrix
$hbplus post_mini_noh.pdb -h 2.9 -d 4 -N -c

# Run DSSP - needed for 2nd structure
$dssp -i post_mini_noh.pdb -o post_mini_noh.dssp

## This is for Jon's binding progrect
#touch wild_bind.txt # needed for checking on binding sites

# Pull all the data togeather, generate the numbering array
$scripts/set_numbers.sh
PYTHONPATH=. python3 $scripts/assemble_data.py >| assemble.txt

# Get the CritiRes stable/unstabla and results in the PDB numbering scheme
#python3 $scripts/find_stable_unstable.py crit >| results_ambnum.txt
python3 $scripts/find_stable_unstable_percent.py crit $1 >| results_ambnum.txt
PYTHONPATH=. python3 $scripts/print_results.py results_ambnum.txt | grep Stable   | sort -g -k 2 >| results.txt
PYTHONPATH=. python3 $scripts/print_results.py results_ambnum.txt | grep Unstable | sort -g -k 2 >> results.txt
PYTHONPATH=. python3 $scripts/print_results.py results_ambnum.txt | grep Neighbour   | sort -g -k 2 >> results.txt

# Get the BindRes stable/unstabla and results in the PDB numbering scheme
python3 $scripts/find_stable_unstable.py bind >| results_bind_ambnum.txt
PYTHONPATH=. python3 $scripts/print_results.py results_bind_ambnum.txt | grep Stable   | sort -g -k 2 >| results_bind.txt
PYTHONPATH=. python3 $scripts/print_results.py results_bind_ambnum.txt | grep Unstable | sort -g -k 2 >> results_bind.txt
PYTHONPATH=. python3 $scripts/print_results.py results_bind_ambnum.txt | grep Bridge   | sort -g -k 2 >> results_bind.txt
