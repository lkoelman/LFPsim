"""
LFP tracker class to keep track of a cell's LFP contributions.


CREDITS
-------

Author:         Lucas Koelman
Affiliations:   Neuromuscular Systems Lab, University College Dublin, Ireland
Email:          lucas.koelman@gmail.com
Last updated:   8-June-2018
"""

from neuron import h
import lfpsim # loads Hoc functions

class LfpTracker(object):
    """
    Python implementation of LfpTracker in lfp_tracker.hoc
    """

    def __init__(
        self, tracker_sec, use_fast_imem, lfp_scheme, sigma,
        electrode_coords, *args):
        """
        Add all segments in given SectionLists as LFP sources, using the given
        LFP approximation scheme

        ARGUMENTS
        ---------

        @param   $o1 : tracking_section <Section>
                 Section where LFP summator object should be inserted.
                 This has no influence on the section and is only necessary
                 because a POINT_PROCESS object needs a container.
        
        @param   $s2 : use_fast_imem <bool>
                 True if CVode.fast_imem should be used and 'extracellular' mechanism
                 should not be inserted.
        
        @param   $s3 : lfp_scheme <string>
                 LFP approximation scheme: "PSA", "LSA", or "RC"
        
        @param   $4 : sigma <float>
                 Conductivity of the extracellular medium.
        
        @param   $o5 : electrode_coords <Vector>
                 Vector of length 3 containing electrode x,y,z coordinates.
        
        @param   $o6 - $oN : tracked_seclist <SectionList>
                 SectionLists containing sections whose LFP contributions should
                 be summed.

        PRECONDITIONS
        -------------

        @pre     If the 'use_fast_imem' argument is True, cvode = h.CVode(); 
                 cvode.use_fast_imem(True) must be called before calling this function.
                 If not, the variable 'i_membrane_' is not created.

        PYTHON USAGE
        ------------
        
           >>> cell = MyCellTemplate()
           >>> soma = cell.soma              # Section
           >>> dendritic = cell.dendritic    # SectionList
           >>> sigma = 0.3
           >>> electrode_coords = h.Vector([10.0, 50.0, 20.0])
           >>> tracker = LfpTracker(soma, True, "PSA", sigma, electrode_coords, dendritic)
        """

        self.summator = h.LfpSumStep(tracker_sec(0.5))
        self.tracked_seclists = args
        self.use_fast_imem = use_fast_imem

        num_tracked_segs = sum((sec.nseg for sl in self.tracked_seclists for sec in sl))
        self.imemb_ptrs = h.PtrVector(num_tracked_segs)


        self.lfp_imemb_factors = h.calc_lfp_factors(
            use_fast_imem, lfp_scheme, sigma, electrode_coords, *args).as_numpy()

        i_seg = 0
        for sl in self.tracked_seclists:
            for sec in sl:
                for seg in sec:
                    if use_fast_imem:
                        h.setpointer(seg._ref_i_membrane_, 'temp_ptr', self.summator)
                        factor = self.lfp_imemb_factors[i_seg] * 1e2
                    else:
                        h.setpointer(seg._ref_i_membrane, 'temp_ptr', self.summator)
                        factor = self.lfp_imemb_factors[i_seg]

                        self.imemb_ptrs.pset(i_seg, seg._ref_i_membrane_)
                        self.summator.add_lfp_source(factor)
                        i_seg += 1

                        self.imemb_ptrs.ptr_update_callback(self.update_imemb_ptrs)


    def update_imemb_ptrs(self):
        """
        Callback function for when i_membrane range variables have changed.
        Re-establish pointers to each compartment's transmembrane current.
        """
        i_seg = 0
        for seclist in self.tracked_seclists:
            for sec in seclist:
                for seg in sec:
                    if self.use_fast_imem:
                        h.setpointer(seg._ref_i_membrane_, 'temp_ptr', self.summator)
                    else:
                        h.setpointer(seg._ref_i_membrane, 'temp_ptr', self.summator)

                        self.summator.update_imemb_ptr(i_seg)
                        i_seg += 1

                        print("Updated i_memb pointers for sectionlist {}".format(seclist))
