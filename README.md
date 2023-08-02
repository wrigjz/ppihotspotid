# critires_python
###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
This is a reimplimentation of CritiRes in python ver 3+, such as anaconda

Requirements are AmberTools, hbplusi, FreeSASA and xssp
You will also need to provide conservation values for each residues, our conservation code
can be found at https://github.com/wrigjz/conservation_python

the directory structure should be something like this

top/critires_scripts

   /consurf_scripts (If you want to use our consurf implimentation)

   /pdbidchain    e.g. 1fnfa

              /input.pdb   this is a single chain from a pdb file

the pdb file can be prepared using the get_pdb_get_from_archive.py script by giving it a file with a list of pdb and chain codes in a format such as 1TSR B etc etc, you may need to edit the script to point to your own local pdb archive


Critires can take a commandline argument to give a minimum number of residues as a percentage to return
If all you want are the most and least stable then set the percentage to 0

cd into pdbidchain and to get the 5% most and least stable residues run
        ../critires_scripts/critires.sh 5

then critires should run, the default is to also run a local version of consurf,  which can be ignored by editing the critires.sh file to comment out a few lines and uncomment some others, you can also choose to run consurf and use the SEQRES records instead
