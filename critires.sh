#!/bin/bash
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
# Simple script to perform a critires job
# You need to make sure that a input.pdb file exists in the directory

export freesasa=/home/programs/freesasa-2.03/linux/bin/freesasa
export scripts=/home/programs/critires_scripts
export consurf_scripts=/home/programs/consurf_scripts
export agpath=$scripts/AutogluonModels/ag-20230915_030535
export dssp=/home/programs/xssp-3.0.5/bin.linux/mkdssp
source /home/programs/anaconda/linux_202307/init.sh
conda activate ag

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

# Prepare a non-H atom version for dssp
python3 $scripts/renum_rm_h.py post_minix.pdb post_mini_noh.pdb No
sed -i -e 's/CYX/CYS/' -e 's/CYM/CYS/' -e 's/HID/HIS/' -e 's/HIE/HIS/' -e 's/HIP/HIS/' post_mini_noh.pdb

# Run DSSP - needed for 2nd structure
$dssp -i post_mini_noh.pdb -o post_mini_noh.dssp

# Pull all the data togeather, generate the numbering array
$scripts/set_numbers.sh
PYTHONPATH=. python3 $scripts/assemble_data.py >| assemble.txt

# Get the results in the PDB numbering scheme
python3 $scripts/scoring.py $agpath >| results_ambnum.txt
PYTHONPATH=. python3 $scripts/print_results.py results_ambnum.txt | grep -E -v 'ACE|NME' >| results.txt
