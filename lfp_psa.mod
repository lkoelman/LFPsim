: lfp.mod

COMMENT
LFPsim - Simulation scripts to compute Local Field Potentials (LFP) from cable compartmental models of neurons and networks implemented in NEURON simulation environment.

LFPsim works reliably on biophysically detailed multi-compartmental neurons with ion channels in some or all compartments.

Last updated 12-March-2016
Developed by : Harilal Parasuram & Shyam Diwakar
Computational Neuroscience & Neurophysiology Lab, School of Biotechnology, Amrita University, India.
Email: harilalp@am.amrita.edu; shyam@amrita.edu
www.amrita.edu/compneuro 
ENDCOMMENT


NEURON {
	SUFFIX lfp_psa
	POINTER transmembrane_current
	RANGE lfp_point, summation_factor
	
}


PARAMETER {
	summation_factor : must be set once
}


ASSIGNED {
	transmembrane_current 
	lfp_point
}


BREAKPOINT { 

	:Point Source Approximation 	
	lfp_point = transmembrane_current * summation_factor * 1e-1   : So the calculated signal will be in nV

}


