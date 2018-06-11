"""

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


Authors:        Harilal Parasuram & Shyam Diwakar
Affiliations:   Computational Neuroscience & Neurophysiology Lab, 
                School of Biotechnology, Amrita University, India.
Email:          harilalp@am.amrita.edu; shyam@amrita.edu
Website:        www.amrita.edu/compneuro
Last updated:   12-March-2016


Modified by:    Lucas Koelman
Affiliations:   Neuromuscular Systems Lab, University College Dublin, Ireland
Email:          lucas.koelman@gmail.com
Last updated:   8-June-2018
"""
# override modules to export
# __all__ = ["module_a", "module_b", "module_c"]

# make classes available at package level
# from . import submodule as submodule_alias
# from .submodule import myclass

import neuron
import os.path

here = os.path.abspath(os.path.dirname(__file__))
neuron.load_mechanisms(here)

neuron.h.load_file(os.path.join(here, 'lfp_lib.hoc'))
print("\n[LFPsim] Functions in <lfp_lib.hoc> loaded into Hoc")
