/* -*- c++ -*- */

#define CREW_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "crew_swig_doc.i"

%{
#include "crew/packet_decoder_cb.h"
%}


%include "crew/packet_decoder_cb.h"
GR_SWIG_BLOCK_MAGIC2(crew, packet_decoder_cb);
