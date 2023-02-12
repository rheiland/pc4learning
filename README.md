# pc4learning

PhysiCell Studio application to explore one of several PhysiCell sample models.

Dependencies: g++ compiler that is recommended for building PhysiCell models. Python distribution containing required modules for the Studio (rf. requirements.txt). We typically recommend users install the Anaconda Python distribution. Rf. https://github.com/physicell-training/ws2022/tree/main/setup


Compile a particular set of sample models. Move those executables to a specific directory where the Studio expects them. Run the Studio.

Note: this repository has a directory structure and workflow that is amenable to nanoHUB.

```
cd pc4learning/src
make

# If you're in a Unix-based terminal/shell, move the executables into the directory where they are expected to be (rf. mv_all.sh bash script):

mv biorobots ../bin
mv celltypes ../bin
mv pred_prey ../bin
mv interactions ../bin

(On Windows, the executables will have the ".exe" suffix)

# Change directory to the Studio's root dir and run it from there using these command line arguments:
cd ..
python bin/pmb.py --studio --nanohub
```


In the Studio:
* select a model to test from the `Model` menu
* in the Run tab, click `Run Simulation`. (Note: on nanoHUB, the simulation is run *from* the `tmpdir` directory and that's where all output files will be written)
* in the Plot tab, click `Play`.
* edit model params in the Studio, re-Run, etc.
