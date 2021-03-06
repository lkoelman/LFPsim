# LFPsim for Python

This a modified version of the original LFPsim package by Parasuram et al. 
(2016) for use with Python and large network simulations using MPI.

## Installation

```sh
git clone https://github.com/lkoelman/LFPsim.git
cd LFPsim

# Installation via symboling link to download directory:
python setup.py develop
python setup.py build_mechs
```

## Usage

See examples in file `lfp_lib.hoc`.

```python
from neuron import h
h.load_file('my_model.hoc')

cell = h.MyCellTemplate() # Hoc Template or Python object with SectionList attributes 'somatic', 'dendritic' etc.
sigma = 0.3
electrode_coords = h.Vector([10.0, 50.0, 20.0])
summator = h.insert_lfp_summator(cell.somatic[0])
h.add_lfp_sources(summator, "PSA", sigma, electrode_coords, cell.dendritic)

# Now you can record from summator._ref_summed variable:
vec = h.Vector()
rec_dt = 0.05
vec.record(summator, summator._ref_summed, rec_dt)
```

For MPI simulations you __must__ use LfpTracker from `lfp_tracker.hoc` and set
the following options before creating it and running your simulation:


```python
cvode = h.CVode()
cvode.use_fast_imem(True) # optional, if you don't use mechanism 'extracellular'
cvode.cache_efficient(True) # necessary, or pointers become invalid
```

--------------------------------------------------------------------------------

# Original README

In this version of LFPsim, the ion channel distribution density and size of the individual compartments was considered in the LFP calculation.

This is the README for the model associated with the paper:

Parasuram H, Nair B, D'Angelo E, Hines M, Naldi G, Diwakar
S. Computational Modeling of Single Neuron Extracellular Electric
Potentials and Network Local Field Potentials using LFPsim,
Front. Comp. Neurosc., June 13, 2016, 10.3389/fncom.2016.00065
available at
http://journal.frontiersin.org/article/10.3389/fncom.2016.00065/abstract

LFPsim - Simulation scripts to compute Local Field Potentials (LFP)
from cable compartmental models of neurons and networks implemented in
NEURON simulation environment.

LFPsim works reliably on biophysically detailed multi-compartmental
neurons with ion channels in some or all compartments.

Associated Paper:
Parasuram H, Nair B, D'Angelo E, Hines M, Naldi G, Diwakar
S. Computational Modeling of Single Neuron Extracellular Electric
Potentials and Network Local Field Potentials using LFPsim,
Front. Comp. Neurosc., June 13, 2016, 10.3389/fncom.2016.00065
available at
http://journal.frontiersin.org/article/10.3389/fncom.2016.00065/abstract

Last updated 01-Feb-2017
Developed by : Harilal Parasuram & Shyam Diwakar
Computational Neuroscience & Neurophysiology Lab, School of Biotechnology, Amrita University, India.
Email: harilalp@am.amrita.edu; shyam@amrita.edu
www.amrita.edu/compneuro 

## How to use LFPsim (Graphical version)

1. Copy all LFPsim files and the directory into your NEURON model
directory downloaded from ModelDB. Copy lfp.mod and mea.mod from
LFPsim to the mechanism directory of the NEURON model.

2. Compile the model; if you had already compiled the model without
LFPsim, include the LFPsim mod files and re-compile using "nrnivmodl"
or "mknrndll".

3. Load your neuron or network model in NEURON.

4. On the terminal type: xopen("extracellular_electrode.hoc") to
initiate LFPsim GUI interface.

5. Set the electrode properties in the GUI.

6. Run the simulation to reconstruct LFP.

A detailed step-by-step procedure is also listed in the
How-To-LFPsim.pdf document.
