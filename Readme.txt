This is a reimplimentation of CritiRes in python

the directory structure should be something like this

top/critires_scripts
   /consurf_script
   /pdbidchain            e.g. 1fnfa
              /input.pdb   this is a single chain from a pdb file

if you cd into top/pdbidchain and run
        ../critires_scripts/critires.sh
then critires should run, the default is to also run a local version of consurf
which can be ignored by editing the critires.sh file to comment out a few lines and uncomment some

