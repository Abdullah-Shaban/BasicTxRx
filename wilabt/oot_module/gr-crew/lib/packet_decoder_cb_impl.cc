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
#include "packet_decoder_cb_impl.h"
#define MAX_PAYLOAD 500
#define PI 3.1415926
namespace gr {
  namespace crew {

    enum demux_states_t {
      STATE_FIND_TRIGGER,       // "Idle" state (waiting for burst)
      STATE_HEADER,             // Decode the header
      STATE_PAYLOAD             // Copy payload
    };

    packet_decoder_cb::sptr
    packet_decoder_cb::make(const std::vector<gr_complex> &symbols)
    {
      return gnuradio::get_initial_sptr
        (new packet_decoder_cb_impl(symbols));
    }

    // create io signature for multiple outputs 
    static int ios[] = {sizeof(char), sizeof(float)};
    static std::vector<int> iosig(ios, ios+sizeof(ios)/sizeof(int));
    /*
     * The private constructor
     */
    packet_decoder_cb_impl::packet_decoder_cb_impl(const std::vector<gr_complex> &symbols)
      : gr::block("packet_decoder_cb",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::makev(1, 2, iosig))
    {
        d_symbols = symbols;
        d_corr_thr = 60 ; // TODO make the decision of the threshold automatic 

        d_bps = 2 ; // choose for qpsk 
        
        // sizes in bits 
        d_header_size = 4*8 ;
        d_payload_size = 50*8 ; // initial packet size (needed by the forecast function)
        d_crc_size = 4*8 ;
        d_pkt_size = d_symbols.size()*d_bps+d_header_size+d_payload_size+d_crc_size ;     

        
        // reset read and write pointers and packet counters and flag variable
        wr_ptr = 0 ; rd_ptr = 0 ;
        count_pkt = 0 ; 
        
        // initialize buffers 
        buffer_bit = (unsigned char*) malloc((MAX_PAYLOAD+20)*8) ; //  *8 to convert to bits 
        buffer_byte = (unsigned char*) malloc(MAX_PAYLOAD+20) ; 

        // store the time reference
        gettimeofday(&time_ref, 0);
        
        // initialize the state of FSM
        d_state = STATE_FIND_TRIGGER ; 
    }

    /*
     * Our virtual destructor.
     */
    packet_decoder_cb_impl::~packet_decoder_cb_impl()
    {
        free(buffer_bit);
        free(buffer_byte);
        std::cout << "INFO: Done! " <<  std::endl ; 
    }

    void
    packet_decoder_cb_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        
        ninput_items_required[0] = d_pkt_size/d_bps + d_symbols.size() ;
    }

    /*
     * Function to find the start of the preamble
     */    
    int
    packet_decoder_cb_impl::find_trigger_signal(
        gr_vector_const_void_star &input_items, 
        int pkt_size, 
        int nsp_in, 
        float d_corr_thr,
        gr_complex &sign_phase)
    {
        const gr_complex *in = (const gr_complex *) input_items[0]; 
        if(nsp_in < pkt_size+d_symbols.size() ) { // not enough samples to correlate 
            return -2 ;
        }else{             
            gr_complex corr_max = 0 ;
            int   corr_index = 0 ;
            for (int i=0; i<pkt_size ; i++){
                gr_complex accum = 0 ;
                for (int j=i; j < d_symbols.size()+i ; j++) {
                    accum += d_symbols[j-i]*in[j] ; 
                } 
                if(std::abs(corr_max) < std::abs(accum)){
                    corr_max = accum ;
                    corr_index = i ;
                }
            }
            
            if(std::abs(corr_max) < d_corr_thr) // compare the result against threshold
                corr_index = -1 ; 
            else{ // if above threshold, calculate the phase rotation
                if(d_bps == 1 ) {
                    if(std::arg(corr_max) <= PI/4 && std::arg(corr_max) > -PI/4)
                        sign_phase = gr_complex(-1,0) ;
                    else if(std::arg(corr_max) <= 3.0*PI/4 && std::arg(corr_max) > PI/4)
                        sign_phase = std::polar (1.0, PI/2) ; 
                    else if(std::arg(corr_max) <= -3.0*PI/4 || std::arg(corr_max) > 3.0*PI/4)
                        sign_phase = gr_complex(1,0) ; 
                    else if(std::arg(corr_max) <= -PI/4 && std::arg(corr_max) > -3.0*PI/4)
                        sign_phase = std::polar(1.0, -PI/2) ;
                    else{
                        sign_phase = gr_complex(-1,0) ;
                    }
                }else{
                    if(std::arg(corr_max) <= PI/4 && std::arg(corr_max) > -PI/4)
                        sign_phase = gr_complex(0,1) ; // 90 degree
                    else if(std::arg(corr_max) <= 3.0*PI/4 && std::arg(corr_max) > PI/4)
                        sign_phase = gr_complex(1.0, 0) ; // 0 
                    else if(std::arg(corr_max) <= -3.0*PI/4 || std::arg(corr_max) > 3.0*PI/4)
                        sign_phase = gr_complex(0,-1) ; //  
                    else if(std::arg(corr_max) <= -PI/4 && std::arg(corr_max) > -3.0*PI/4)
                        sign_phase = gr_complex(-1, 0) ; // 
                    else{
                        sign_phase = gr_complex(1,0) ;
                    }
                }
            }         
            return corr_index ;
        }
    }

    char
    packet_decoder_cb_impl::symbol2bit(gr_complex sign_phase, gr_complex in, int bps, bool header)
    {
        // bpsk         
        if(bps == 1){        
            if((sign_phase*in).real() > 0){
                return 1 ;
            }else{
                return 0 ;
            }
        // qpsk 
        // note that the header and payload has different endien ... therefore need the boolean variable 
        }else{
            gr_complex sample = sign_phase * in ; 
            if (sample.imag() >= 0 and sample.real() >= 0) {
              return 0x00;
            }
            else if (sample.imag() >= 0 and sample.real() < 0) {
              if (header) 
                return 0x02 ;
              else
                return 0x01;
            }
            else if (sample.imag() < 0 and sample.real() < 0) {
              if(header)
                return 0x01 ; 
              else
                return 0x02;

            }
            else if (sample.imag() < 0 and sample.real() >= 0) {
              return 0x03;
            }
        }
        
    }

    int
    packet_decoder_cb_impl::bit2byte(void *out_ptr, void *in_ptr, int total_bit,int bps)
    {
        const char *in = (char*) in_ptr ;
        char *out = (char*) out_ptr ;
        int num_byte = total_bit / 8 ; 
        for (int i=0 ; i<num_byte; i++){

            char temp = 0 ;
            for(int j=i*8; j< i*8+8; j+=bps){
                temp = temp | in[j/bps] << (8-bps-(j%8)) ;
            }
            out[i] = temp ; 
        }
    }

    int
    packet_decoder_cb_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        // define variables        
        const gr_complex *in = (const gr_complex *) input_items[0];
        char *out = (char *) output_items[0];
        float *err = NULL ; 
        if(output_items.size() == 2)
            err = (float*) output_items[1] ;
        int nsp_in = ninput_items[0] ; 
        int corr_index = 0 ; 
        // implement FSM 
        switch (d_state) {        
            case STATE_FIND_TRIGGER:
                corr_index = find_trigger_signal( input_items, d_pkt_size/d_bps, nsp_in, d_corr_thr, sign_phase) ; // d_pkt_size should be the packet size in symbol 
                if(corr_index >= 0) {
                    d_state = STATE_PAYLOAD ;
                    rd_ptr = corr_index + d_symbols.size() ;
                    wr_ptr = 0 ;
                    // fall through
                }else if(corr_index == -2){
                    consume_each(0) ;
                    break ;
                }else{
                    consume_each(d_pkt_size/d_bps) ;
                    break ;
                }

                
            case STATE_HEADER:
                while( wr_ptr < d_header_size/d_bps && rd_ptr < nsp_in) {
                    buffer_bit[wr_ptr] = symbol2bit(sign_phase,in[rd_ptr],d_bps, true) ; 
                    wr_ptr ++ ; 
                    rd_ptr ++ ;        
                }
                if(wr_ptr >= d_header_size/d_bps) { // complete header received
                    unsigned int packet_len_rx = 0 ; 
                    unsigned int seq_number = 0 ; 
                    unsigned char crc_rx = 0 ; 
                    // decode packet length and sequence number
                    for(int i = 0 ; i<12 ; i+=d_bps){
                        packet_len_rx = packet_len_rx | (buffer_bit[i/d_bps] << i ) ; 
                        seq_number = seq_number | (buffer_bit[(i+12)/d_bps] << i ) ;
                    }
                    packet_len_rx &= 0x0FFF ; 
                    seq_number &= 0x0FFF ; 
                    // decode header crc
                    for(int i = 0 ; i<8 ; i+=d_bps){
                        crc_rx = crc_rx | (buffer_bit[(i+24)/d_bps] << i) ; 
                    }
                    // calculate header crc 
                    d_crc_impl.reset();
                    d_crc_impl.process_bytes((void const *) &packet_len_rx, 2);
                    d_crc_impl.process_bytes((void const *) &seq_number, 2);
                    unsigned char crc = d_crc_impl();
                    // check header crc
                    if (crc == crc_rx){ // header crc correct 
                        // update state and pointer
                        d_state = STATE_PAYLOAD ; 
                        wr_ptr = 0 ; 
                        // check if the payload size is below the maximum
                        if(packet_len_rx-d_crc_size/8 <= MAX_PAYLOAD){
                            d_payload_size = packet_len_rx * 8 - d_crc_size ; // update the real payload size 
                            //d_payload_size = packet_len_rx * 8  ;
                        }else{ 
                            d_state = STATE_FIND_TRIGGER ; 
                            consume_each(rd_ptr) ;
                            rd_ptr = 0 ;
                            wr_ptr = 0 ;
                            std::cout << "ERROR: payload size larger than " << MAX_PAYLOAD << std::endl ;
                            break ; 
                            //return WORK_DONE ; 
                        }
                        d_pkt_size = d_symbols.size()*d_bps+d_header_size+d_payload_size+d_crc_size ;  
                        // fall through
                    }else{ // header crc incorrect
                        d_state = STATE_FIND_TRIGGER ; 
                        consume_each(rd_ptr) ;
                        rd_ptr = 0 ;
                        wr_ptr = 0 ;
                        break ; 
                    }        

                }else{ // not complete header, continue next time
                    consume_each(rd_ptr) ;
                    rd_ptr = 0 ;
                    break ; 
                }


           	case STATE_PAYLOAD:
                while( d_symbols.size() + wr_ptr + d_header_size/d_bps < d_pkt_size/d_bps && rd_ptr < nsp_in) {
                    buffer_bit[wr_ptr] = symbol2bit(sign_phase,in[rd_ptr],d_bps, false) ; 
                    wr_ptr ++ ;
                    rd_ptr ++ ;     
                }
                if(d_symbols.size() + wr_ptr + d_header_size/d_bps >= d_pkt_size/d_bps ){ // one packet is complete
                    bit2byte(buffer_byte, buffer_bit, d_payload_size + d_crc_size ,d_bps);
                    // calculate payload crc
                    d_crc_impl_pl.reset();
                    d_crc_impl_pl.process_bytes(buffer_byte, d_payload_size/8);
                    unsigned int crc_cal = d_crc_impl_pl();
                    // decode payload crc 
                    unsigned int crc_rx ; 
                    memcpy((void*) &crc_rx, (void *) (buffer_byte+d_payload_size/8), 4) ;
                    // check payload crc                    
                    if(crc_cal == crc_rx) { 
                        // if crc correct, copy the payload to the output
                        memcpy((void *) out, (void *) buffer_byte, d_payload_size/8);
                        produce(0,d_payload_size/8);
                        count_pkt ++ ; 
                    }else{
                        std::cout << "payload crc incorrect ! " << std::endl ; 
                    }

                    // consume the samples 
                    consume_each(rd_ptr) ; 

                    // reset the state and pointers
                    d_state = STATE_FIND_TRIGGER ;
                    rd_ptr = 0 ; wr_ptr = 0 ; 

                }else{ // not complete packet is detected
                    consume_each(rd_ptr) ;
                    rd_ptr = 0 ;
                }   
                
                break ; 
        
          
	        default:
	            throw std::runtime_error("invalid state"); 

        }
        
        // if required to have the packet reception rate output
        
        if(output_items.size() == 2 ){
            long mtime, seconds, useconds; 
            timeval now ;  
            gettimeofday(&now, 0);
            seconds  = now.tv_sec  - time_ref.tv_sec;
            useconds = now.tv_usec - time_ref.tv_usec;
            mtime = ((seconds) * 1000 + useconds/1000.0) + 0.5;

            float pkt_received = count_pkt ; //needed for type cast ? 
            if(mtime >= 1000){
                // copy the count_pkt to the output
                memcpy((void *) err, (void *) &pkt_received, sizeof(float));
                produce(1,1) ;
                // reset the time reference 
                gettimeofday(&time_ref, 0);  
                // reset the packet counter 
                count_pkt = 0 ; 
            }
        }
        
        return WORK_CALLED_PRODUCE;
        
    }



  } /* namespace crew */
} /* namespace gr */

