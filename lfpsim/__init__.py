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

# Expose some Hoc functions through this module but wrap them so there
# is documentation
def insert_lfp_summator(section):
    """
    Insert point process that keeps track of the cell's LFP contributions
    and sums them into one of its variables.
    
    @param   $o1 : Section
             Section where LfpSummator should be inserted
    
    """
    return neuron.h.insert_lfp_summator(section)


def add_lfp_sources(*args):
    """
    Add all segments in given SectionLists as LFP sources, using the given
    LFP approximation scheme.
   

    @param   $o1 : LfpSummator
             LfpSummator object that will track all the LFP sources
   

    @param   $s2 : string
             LFP approximation scheme: "PSA", "LSA", or "RC"
   

    @param   $3 : sigma
             Conductivity of the extracellular medium.
   

    @param   $o4 : Vector
             Vector of length 3 containing electrode x,y,z coordinates.
   

    @param   $o5 - $oN : SectionList
             SectionLists containing sections whose LFP contributions should
             be summed.
   

    USAGE
    -----
    
       >>> cell = MyCellTemplate()
       >>> soma = cell.soma              # Section
       >>> dendritic = cell.dendritic    # SectionList
       >>> summator = h.insert_lfp_summator(soma)
       >>> sigma = 0.3
       >>> electrode_coords = h.Vector([10.0, 50.0, 20.0])
       >>> add_lfp_sources(summator, "PSA", sigma, electrode_coords, dendritic)
    
    """
    return neuron.h.add_lfp_sources(*args)