TITLE Source for Local Field Potential signal

COMMENT
DESCRIPTION
-----------

Source for Local Field Potential signal.

USAGE
-----

- Insert this mechanism into section in combination with the 'extracellular'
  mechanism.

- Make this mechanism's 'transmembrane_current' pointer point to 
  extracellular's 'i_membrane'. 

- Set the summation factor according to the approximation scheme you want to
  use (see associated functions in 'lfp_lib.hoc')

CREDITS
-------

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
ENDCOMMENT

UNITS {
    (nV) = (nanovolt)
}


NEURON {
    SUFFIX lfp_src
    POINTER transmembrane_current
    RANGE contrib, summation_factor
    
}


PARAMETER {
    summation_factor : Multiplicative factor for contribution to total LFP.
                     : Must be set once at initialization.
}


ASSIGNED {
    transmembrane_current  : Pointer to this segment's transmembrane current
    contrib (nV)           : Contribution of this segment to total LFP (nV)
}


BREAKPOINT { 
    : Factor 1e-1 makes units of 'contrib' nV (nano Volts)
    contrib = transmembrane_current * summation_factor * 1e-1

}


