# pc4cells_near_membrane

Experimental PhysiCell model for testing cell mechanics near a "membrane" (in this case, the x-axis (y=0)).

Compile, copy the executable to the root directory, run the GUI:
```
cd pc4cells_near_membrane/src
make
cp mymodel ..
cd ..
python bin/studio.py
```

In the GUI:
* in the Run tab, click `Run Simulation`. Note: the simulation is run *from* the `tmpdir` directory and that's where all output files will be written.
* in the Plot tab, click `Play`.
* edit params if you want then repeat: Run, Play.
