# pc4learning

Dependencies: Python distribution containing required modules for the Studio (rf. requirements.txt). We typically recommend users install the Anaconda Python distribution.

PhysiCell Studio application to explore one of several PhysiCell sample models.

Compile a particular set of sample models. Move those executables to a specific directory where the Studio expects them. Run the Studio.
```
cd pc4learning/src
make

# If you're in a Unix-based terminal/shell, move the executables into the root folder (rf. mv_all.sh bash script):

mv biorobots ../bin
mv celltypes ../bin
mv pred_prey ../bin
mv interactions ../bin
# maybe others in the future

# Change directory to the Studio's root dir and run it from there:
cd ..
python bin/pmb.py --studio
```

Note: this repository has a directory structure and workflow that is amenable to nanoHUB.

In the Studio:
* select a model to test from the `Model` menu
* in the Run tab, click `Run Simulation`. (Note: on nanoHUB, the simulation is run *from* the `tmpdir` directory and that's where all output files will be written)
* in the Plot tab, click `Play`.
* edit model params in the Studio, re-Run, etc.
