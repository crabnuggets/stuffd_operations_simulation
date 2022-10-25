# stuffd_operations_simulation
Simulation model of a Stuff'd outlet's original process flow against the proposed process flow utilizing kiosks for 
DAO2703 Operations and Technology Management's project component.

## Requirements
The simulation model requires Python versions 3.7 and above to run. In addition, the following packages are required:

* matplotlib
* scipy
* numpy

## Usage of the simulation model
To run the simulation, run the following command: 
```
python main.py
```
The above command will run one iteration of simulation for both the original process flow and the kiosk-based process 
flow with the same set of 300 randomly generated customers as inputs. The results of this iteration of simulation are
printed onto the terminal. In addition, plots of the respective results are saved in the 'plots' subdirectory of this
project.  

The user can also run 100 iterations of simulation and gather the averages of the results for each iteration of 
simulation. This can be done by commenting out the respective blocks of code segmented by '======' lines and 
uncommenting the respective blocks of code desired to run in `main.py`. Additional documentation within `main.py` has 
been provided for guidance.

> ⚠️WARNING: Running simulations over 100 iterations is computationally expensive and takes about 5 to 10 minutes. 