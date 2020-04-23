# set up the environment
###################################################################################################
## and Jon Wright, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## These files are licensed under the GLP ver 3, essentially you have the right
## to copy, modify and distribute this script but all modifications must be offered
## back to the original authors
###################################################################################################
source /home/programs/amber18/amber.sh
source /home/programs/anaconda/linux-5.3.6/init.sh
scripts=../critires_scripts

export mpirun=/usr/local/openmpi-2.0.0_gcc48/bin/mpirun
$mpirun -n `wc -l < $PBS_NODEFILE` -machinefile $PBS_NODEFILE \
      $AMBERHOME/bin/sander.MPI -O -i $scripts/sander_md.in -p an_mini.top -c an_mini.crd \
                -ref an_mini.crd -o an_md.out -r an_md.res
