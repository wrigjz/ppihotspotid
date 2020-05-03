###################################################################################################
## Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
This is a reimplimentation of CritiRes in python ver 3+, such as anaconda

the directory structure should be something like this

top/critires_scripts
   /consurf_script
   /pdbidchain            e.g. 1fnfa
              /input.pdb   this is a single chain from a pdb file

the pdb file can be prepared using the get_pdb_get_from_archive.py script by giving it a file with
you may need to edit the script to point to your own local pdb archive
    pdbcode chain
    pdbcode chain
    etc etc

if you cd into top/pdbidchain and run
        ../critires_scripts/critires.sh
then critires should run, the default is to also run a local version of consurf
which can be ignored by editing the critires.sh file to comment out a few lines and uncomment some
others, you can also choose to run consurf and use the SEQRES records instead
