# pc4learning

GUI to explore one of several PhysiCell sample models.

Compile (all provided sample models), copy the executable(s) you want to run to the root directory, run the GUI:
```
cd pc4learning/src
make

# move the executables into the root folder
mv biorobots ..
mv celltypes ..
mv pred_prey ..
mv interactions ..

# Change directory to the root dir and run the GUI from there
cd ..
python bin/studio.py
```

In the GUI:
* select the model to test from the `Model` menu
* in the Run tab, click `Run Simulation`. Note: on nanoHUB, the simulation is run *from* the `tmpdir` directory and that's where all output files will be written.
* in the Plot tab, click `Play`.
* edit params if you want then repeat: Run, Play.
