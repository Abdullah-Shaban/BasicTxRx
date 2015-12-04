/* -*- c++ -*- */
/* 
 * Copyright 2015 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "gap_gen_cc_impl.h"

namespace gr {
  namespace crew {
    enum demux_states_t {
      STATE_IDLE,       // "Idle" state (waiting for burst)
      STATE_FIND_PKTID,             // Decode the header
      STATE_FIND_PL_OFFSET,          
      STATE_FIND_PKT_OFFSET,
      STATE_CHECK_SP,
      STATE_SENT
    };


    gap_gen_cc::sptr
    gap_gen_cc::make(bool running)
    {
      return gnuradio::get_initial_sptr
        (new gap_gen_cc_impl(running));
    }

    /*
     * The private constructor
     */
    gap_gen_cc_impl::gap_gen_cc_impl(bool running)
      : gr::block("gap_gen_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
    	d_running = running ; 
    	d_state = STATE_IDLE; 
    	work_called = 0 ; 
    	pkt_id = 0 ;
    	pkt_len = (64 + 32 + 50*8 + 4*8 +3*8)*4 ; 
    	bps = 2 ; // bit per symbol, use 1 for bpsk, 2 for qpsk 
    }

    /*
     * Our virtual destructor.
     */
    gap_gen_cc_impl::~gap_gen_cc_impl()
    {
    }

    void
    gap_gen_cc_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        //ninput_items_required[0] = 4096 ; 
        if(d_running){
        	ninput_items_required[0] = 3000 ;
        }else{
        	ninput_items_required[0] = 0 ; 
        }
    }

    void 
    gap_gen_cc_impl::set_status(bool status){
    	// only allow to set true
    	// TODO, change to send_pkt()
    	//std::cout <<"call back ! " << std::endl ; 
		if(status == true && status != d_running){	
			//std::cout << "status updated ! " << std::endl ; 		
	  		d_running = status ; 
		}
    }
    
    bool 
    gap_gen_cc_impl::get_status(){
      	return  d_running ; 
    }
    
    void 
    gap_gen_cc_impl::print_state(int d_state){
      	switch (d_state) {
      		case STATE_IDLE:
      			std::cout << "state idle " << std::endl ;
      			break ;
      		case STATE_FIND_PKTID:
      			std::cout << "state find packet id  " << std::endl ;
      			break ;
      		case STATE_FIND_PL_OFFSET:
      			std::cout << "state find payload offset " << std::endl ;
      			break ;     
      		case STATE_FIND_PKT_OFFSET:
      			std::cout << "state find pkt offset " << std::endl ;
      			break ;      			 			
      		case STATE_CHECK_SP:
      			std::cout << "state check sample " << std::endl ;
      			break ;
      		case STATE_SENT:
      			std::cout << "state sent " << std::endl ;
      			break ;
  			default:
  				std::cout << "unknown state " << std::endl ; 
      			
      	}
    }
      
    void 
    gap_gen_cc_impl::produce_idle_output(gr_vector_void_star &output_items, int noutput_items){
    	gr_complex *out = (gr_complex *) output_items[0];
		for(int i=0; i<noutput_items ; i++){
			out[i] = 0 ; 
		}
    }
    
      
    int
    gap_gen_cc_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const gr_complex *in = (const gr_complex *) input_items[0];
        gr_complex *out = (gr_complex *) output_items[0];
        int nsp_in = ninput_items[0] ;  
        int output_produced = 0 ;
        int input_consumed = 0 ; 
        unsigned pkt_offset = 0 ;
		unsigned pld_offset = 0 ;
		std::vector<tag_t> tags_pktid ; 
		std::vector<tag_t> tags;
	  	get_tags_in_range(tags, 0, nitems_read(0), nitems_read(0)+noutput_items, pmt::string_to_symbol("packet_len") );
    	get_tags_in_range(tags_pktid, 0, nitems_read(0), nitems_read(0)+noutput_items, pmt::string_to_symbol("pktid") ) ;
    	
		switch(d_state) {
			case STATE_IDLE:
				if (d_running){
					//TODO: currently when searching for new packet, the delay is too big, skip this and send any packets in the queue
					// d_state = STATE_FIND_PKTID ; 
					d_state = STATE_FIND_PKT_OFFSET ; 
				}else{
					produce_idle_output(output_items, noutput_items); 
					output_produced = noutput_items ; 
					input_consumed = 0 ; 
					break ; 
				}

			case STATE_FIND_PKTID:
				//print_state(d_state) ;
				for (int i=0 ; i< tags_pktid.size() ; i++){
					unsigned pkt_id_new = pmt::to_uint64(tags_pktid[i].value) ; 
					if (pkt_id_new != pkt_id ) {
						std::cout << "packet id " << pkt_id_new << std::endl ; 
						pkt_id = pkt_id_new ; 
						d_state = STATE_FIND_PL_OFFSET ; 
						break ;
					}
				}
				if(d_state == STATE_FIND_PKTID)	{
					input_consumed = nsp_in ; 
					output_produced = noutput_items ; 
					produce_idle_output(output_items, output_produced);
					break ;		
				}	
				// else fall through 
					
			
			case STATE_FIND_PL_OFFSET:
				//print_state(d_state) ;
				for (int i=0 ; i< tags_pktid.size() ; i++){
					unsigned pkt_id_new = pmt::to_uint64(tags_pktid[i].value) ; 
					if (pkt_id_new == pkt_id ) {
						pld_offset = tags_pktid[i].offset - nitems_read(0) ;
						d_state = STATE_FIND_PKT_OFFSET ; 
						break ;
					}
				}
				if(d_state == STATE_FIND_PL_OFFSET){
					input_consumed = nsp_in ; 
					output_produced = noutput_items ; 
					produce_idle_output(output_items, output_produced);					
					break ; 
				}
				
			case STATE_FIND_PKT_OFFSET:
				print_state(d_state) ;
				for(int i=0; i<tags.size(); i++ ){
					pkt_len = pmt::to_uint64(tags[i].value) * 4 * 8 /bps ; 
					unsigned pkt_offset_temp = tags[i].offset - nitems_read(0) ; 
					// temp solution
					pkt_offset = pkt_offset_temp ; 
					d_state = STATE_CHECK_SP ;
					//std::cout << "packet len " << pkt_len << std::endl ; 
					break ; 
					//Temperary disabled the parts below
//					if( (pkt_offset_temp + 12*8*4 - pld_offset) % pkt_len == 0 ){
//						pkt_offset = pkt_offset_temp ; 
//						d_state = STATE_CHECK_SP ; 
//						break ; 
//					}						
				}
				if(d_state == STATE_FIND_PKT_OFFSET) {
					input_consumed = nsp_in ; 
					// temp disabled 
					// d_state = STATE_FIND_PL_OFFSET ; // go back to find payload offset 
					output_produced = noutput_items ; 
					produce_idle_output(output_items, output_produced);					
					break ; 
				}
			
			
			case STATE_CHECK_SP:
				print_state(d_state) ;
				if( nsp_in >= pkt_offset + pkt_len){
					for(int i=0; i<pkt_len ; i++){
						out[i] = in[pkt_offset+i] ; 
					}				
	  				//std::cout << "packet sent ! " << std::endl ; 	  				
	  				d_state = STATE_SENT ;  
				}else{
					input_consumed = pkt_offset ; 
					output_produced = noutput_items ; 
					produce_idle_output(output_items, output_produced);	
					d_state = STATE_FIND_PL_OFFSET ; 
					break ; 
				}
			
			
			case STATE_SENT:
				print_state(d_state) ;
				d_running = false ; 
				output_produced = pkt_len ; 
				input_consumed = pkt_len+pkt_offset;
				d_state = STATE_IDLE ; 	  
			
				break ;
			
			default:
				throw std::runtime_error("invalid state"); 
			 

	
		} // end switch 


        consume_each (input_consumed) ;
        return output_produced;
    }

  } /* namespace crew */
} /* namespace gr */

