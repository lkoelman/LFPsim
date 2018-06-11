COMMENT

Sum LFP sources from other compartments and assign the summed LFP signal
to a recordable variable.

Written by Lucas Koelman

ENDCOMMENT


NEURON {
    POINT_PROCESS LfpSummator
    POINTER temp_ptr
    POINTER donotuse_sources
    RANGE sample_period, summed
}


VERBATIM

// Linked list node for storing refs to observed hoc variables
typedef struct node {
    double factor;      // spatial / conductivity factor
    double* hoc_ref;    // hoc reference to observed LFP source variable
    struct node* next;  // next node in linked list
} LfpSource;

ENDVERBATIM


UNITS {
    (nV) = (nanovolt)
}


PARAMETER {
    sample_period = 0.05 (ms)
}


ASSIGNED {
    on
    temp_ptr
    donotuse_sources
    summed (nV)
}


CONSTRUCTOR {
VERBATIM {
    // Snippet based on pattern.mod
    LfpSource** sources = (LfpSource**)(&(_p_donotuse_sources));

    LfpSource* first_node = emalloc(sizeof(LfpSource));
    first_node->factor = 0.0;
    first_node->hoc_ref = NULL;
    first_node->next = NULL;
    
    *sources = first_node;

}
ENDVERBATIM
}


DESTRUCTOR {
VERBATIM {

    // Free memory occupied by linked list
    LfpSource* this_node = (LfpSource*)(_p_donotuse_sources);
    LfpSource* next_node;
    while (this_node != NULL) {
        next_node = this_node->next;
        free(this_node);
        this_node = next_node;
    }

}
ENDVERBATIM
}


INITIAL {
    on = 0
    net_send(sample_period, 1)  : turn on and start sampling
}


: Add observed LFP source.
:
: PYTHON USAGE
: ------------
: 
: >>> summator = LfpSummator(soma(0.5))
: >>> for sec in h.allsec():
: >>>     for seg in sec:
: >>>         factor = calculate_lfp_factor()
: >>>         h.setpointer(seg._ref_i_membrane, 'temp_ptr', summator)
: >>>         summator.add_source(factor)
:
:
FUNCTION add_lfp_source(factor) {
VERBATIM
    
    // Look for end of linked list and append observed variable
    LfpSource* current = (LfpSource*)(_p_donotuse_sources);
    while (current->hoc_ref != NULL) {
        current = current->next;
    }
    current->hoc_ref = _p_temp_ptr;
    current->factor = _lfactor;

    // Allocate node for next call
    current->next = emalloc(sizeof(LfpSource)); // for next call
    current->next->hoc_ref = NULL;

    // fprintf(stderr, "Added ref to group %d\n", group_id);
ENDVERBATIM
}


VERBATIM
/**
 * Sum all observed LFP sources and assign to 'summed'
 *
 * @note    called every sample_period so function call overhead 
 *          might be significant -> inline
 */
static inline void sum_lfp_sources() {
    LfpSource* current = (LfpSource*)(_p_donotuse_sources);
    summed = 0.0;
    while (current != NULL) {
        if (current->hoc_ref != NULL) {
            double i_membrane = *(current->hoc_ref);
            summed += i_membrane * current->factor;
        }
        current = current->next;
    }

}
ENDVERBATIM


NET_RECEIVE (w) {

    if (flag == 0) { : 0 is used for external events
VERBATIM
        fprintf(stderr, "Received event with weight %f\n", _args[0]);
ENDVERBATIM
    }
    if (flag == 1) { : message from INITIAL
        if (on == 0) { : turn on and start sampling
            on = 1
VERBATIM
            sum_lfp_sources();
ENDVERBATIM
            net_send(sample_period, 2)
        } else {
            on = 0
        }
    }
    if (flag == 2 && on == 1) { : self-message to sample variables
VERBATIM
        sum_lfp_sources();
ENDVERBATIM
        net_send(sample_period, 2)
    }
}