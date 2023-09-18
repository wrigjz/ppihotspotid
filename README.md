# critires_python
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
This is a reimplimentation of CritiRes in python ver 3+, such as anaconda with the autogluon ML library
This code has been tested on Centos 7.x and Ubuntu 22.04

Requirements are AmberTools, FreeSASA and xssp
You will also need to provide conservation values for each residues, our conservation code
can be found at https://github.com/wrigjz/conservation_python

Each CR run must be done in a separate directory and the PDB input file must be called input.pdb

The pdb file can be prepared using the get_pdb_get_from_archive.py script by giving it a file with a list of pdb and chain codes in a format such as 1TSR B etc etc, you may need to edit the script to point to your own local pdb archive

to run:
% cd $DIR_CONTAINING_input.pdb
% $PATH_TO_CR/critires.sh

Then critires should run, the default is to also run a local version of consurf,  which can be ignored by editing the critires.sh file to comment out a few lines and uncomment some others, you can also choose to run consurf and use the SEQRES records instead
