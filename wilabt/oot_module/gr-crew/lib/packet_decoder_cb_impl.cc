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
#define PER_WINDOW  1000
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
        d_corr_thr = 28 ; // TODO make the decision of the threshold automatic 
        
        // sizes in bits 
        d_header_size = 4*8 ;
        d_payload_size = 50*8 ; // initial packet size (needed by the forecast function)
        d_crc_size = 4*8 ;
        d_pkt_size = d_symbols.size()+d_header_size+d_payload_size+d_crc_size ; 
        
        // reset read and write pointers and packet counters and flag variable
        wr_ptr = 0 ; rd_ptr = 0 ;
        wr_ptr_per = 0 ; rd_ptr_per = 0 ;
        count_pkt = 0 ; 
        count_err = 0 ; 
        last_seq = -1 ;
        continuous_failed = 0 ; 
        updated = false ; 

        // initialize buffers 
        buffer_bit = (unsigned char*) malloc((MAX_PAYLOAD+20)*8) ; //  *8 to convert to bits 
        buffer_byte = (unsigned char*) malloc(MAX_PAYLOAD+20) ; 
        buffer_per = (unsigned char*) malloc(PER_WINDOW*2) ; 

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
        free(buffer_per);
        std::cout << "INFO: Done! " <<  std::endl ; 
    }

    void
    packet_decoder_cb_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        
        ninput_items_required[0] = d_pkt_size + d_symbols.size() ;
    }

    /*
     * Fundtion to find the start of the preamble
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
            }         
            return corr_index ;
        }
    }

    char
    packet_decoder_cb_impl::symbol2bit(gr_complex sign_phase, gr_complex in)
    {
        if((sign_phase*in).real() > 0){
            return 1 ;
        }else{
            return 0 ;
        }
    }

    int
    packet_decoder_cb_impl::bit2byte(void *out_ptr, void *in_ptr, int d_pkt_size)
    {
        const char *in = (char*) in_ptr ;
        char *out = (char*) out_ptr ;
        int num_byte = d_pkt_size / 8 ; 
        for (int i=0 ; i<num_byte; i++){
            char temp = 0 ;
            for(int j=i*8; j< i*8+8; j++){
                temp = temp | in[j] << (7-(j%8)) ;
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
        unsigned int lost_pkt = 0 ;

        // implement FSM 
        switch (d_state) {        
            case STATE_FIND_TRIGGER:
                corr_index = find_trigger_signal( input_items, d_pkt_size, nsp_in, d_corr_thr, sign_phase) ;
                if(corr_index >= 0) {
                    d_state = STATE_PAYLOAD ;
                    rd_ptr = corr_index + d_symbols.size() ;
                    wr_ptr = 0 ;
                    count_pkt ++ ;
                    updated = true ; 
                    // fall through
                }else if(corr_index == -2){
                    consume_each(0) ;
                    break ;
                }else{
                    consume_each(d_pkt_size) ;
                    break ;
                }

                
            case STATE_HEADER:
                while( wr_ptr < d_header_size && rd_ptr < nsp_in) {
                    buffer_bit[wr_ptr] = symbol2bit(sign_phase,in[rd_ptr]) ; 
                    wr_ptr ++ ; 
                    rd_ptr ++ ;        
                }
                if(wr_ptr >= d_header_size) { // complete header received
                    unsigned int packet_len_rx = 0 ; 
                    unsigned int seq_number = 0 ; 
                    unsigned char crc_rx = 0 ; 
                    // decode packet length and sequence number
                    for(int i = 0 ; i<12 ; i++){
                        packet_len_rx = packet_len_rx | (buffer_bit[i] << i) ; 
                        seq_number = seq_number | (buffer_bit[i+12] << i) ;
                    }
                    packet_len_rx &= 0x0FFF ; 
                    seq_number &= 0x0FFF ;  
                    // decode header crc
                    for(int i = 0 ; i<8 ; i++){
                        crc_rx = crc_rx | (buffer_bit[i+24] << i) ; 
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

                        // check if there are missed packets using the continuous sequence number
                        if(last_seq == -1){
                            last_seq = seq_number ;
                            lost_pkt = 0 ;
                        }else if(last_seq == 0xFFFF){
                            lost_pkt = seq_number ; 
                            last_seq = seq_number ;
                        }else{
                            lost_pkt = seq_number - last_seq - 1 ;
                            last_seq = seq_number ;
                        }

                        if(lost_pkt > continuous_failed) {
                            int pkt_not_detected = lost_pkt - continuous_failed ; 
                            std::cout << pkt_not_detected<< " packets not detected " << std::endl ; 
                            count_pkt += pkt_not_detected ; 
                            count_err += pkt_not_detected ; 
                            buffer_per[wr_ptr_per] = pkt_not_detected ; 
                            wr_ptr_per++ ;
                            if(wr_ptr_per >= PER_WINDOW*2)
                                wr_ptr_per = 0 ;

                        }else if( lost_pkt < continuous_failed) {
                            int pkt_falsealarm = continuous_failed - lost_pkt ; 
                            std::cout << pkt_falsealarm << " packets detected are not true " << std::endl ; 
                            count_pkt -= pkt_falsealarm ;
                            count_err -= pkt_falsealarm ; 
                            if(wr_ptr_per >= pkt_falsealarm) 
                                wr_ptr_per -= pkt_falsealarm ;
                            else
                                wr_ptr_per += PER_WINDOW*2 - pkt_falsealarm ;
                        }

                        // check if the payload size is below the maximum
                        if(packet_len_rx-d_crc_size/8 <= MAX_PAYLOAD){
                            d_payload_size = packet_len_rx * 8 - d_crc_size ; // update the real payload size                            
                        }else{ // if not return 
                            d_payload_size = MAX_PAYLOAD ;
                            std::cout << "ERROR: payload size larger than " << MAX_PAYLOAD << std::endl ;
                            return WORK_DONE ; 
                        }
                        d_pkt_size = d_symbols.size()+d_header_size+d_payload_size+d_crc_size ;  
                        // fall through
                    }else{ // header crc incorrect
                        std::cout << "failed to decode header ! " << std::endl ;
                        d_state = STATE_FIND_TRIGGER ; 
                        consume_each(rd_ptr) ;
                        rd_ptr = 0 ;
                        wr_ptr = 0 ;
                        // increase packet error counter 
                        count_err++ ; 
                        continuous_failed ++ ;
                        buffer_per[wr_ptr_per] = 1 ;
                        wr_ptr_per++ ;
                        if(wr_ptr_per >= PER_WINDOW*2)
                            wr_ptr_per = 0 ;
                        break ; 
                    }        

                }else{ // not complete header, continue next time
                    consume_each(rd_ptr) ;
                    rd_ptr = 0 ;
                    break ; 
                }


           	case STATE_PAYLOAD:
                while( wr_ptr + d_header_size < d_pkt_size && rd_ptr < nsp_in) {
                    buffer_bit[wr_ptr] = symbol2bit(sign_phase,in[rd_ptr]) ; 
                    wr_ptr ++ ;
                    rd_ptr ++ ;        
                }
      
                if(wr_ptr + d_header_size >= d_pkt_size){ // one packet is complete
                    bit2byte(buffer_byte, buffer_bit, d_pkt_size-d_header_size);

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
                        // update the per buffer  
                        buffer_per[wr_ptr_per] = 0 ;
                        continuous_failed = 0 ;
                    }else{
                        std::cout << "payload crc incorrect ! " << std::endl ; 
                        // increase packet error counter and update the per buffer
                        count_err++ ; 
                        continuous_failed ++ ;
                        buffer_per[wr_ptr_per] = 1 ;
                    }
                    // update the per buffer write pointer
                    wr_ptr_per++ ;
                    if(wr_ptr_per >= PER_WINDOW*2)
                        wr_ptr_per = 0 ;

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
        
        // if required to have the per output
        if(output_items.size() == 2 && updated ){
            // reset the flag 
            updated = false ; 
            // calculate the per
            float pkt_err_rate = (float) count_err / count_pkt * 100.0 ;
            // copy the per to the output
            memcpy((void *) err, (void *) &pkt_err_rate, sizeof(float));
            produce(1,1) ;
            // if the packet counter is above the per window
            if( count_pkt > PER_WINDOW ) {
                // move the sliding window on the per buffer
                count_pkt = PER_WINDOW ;
                count_err -= (unsigned int) buffer_per[rd_ptr_per] ; 
                rd_ptr_per ++ ;
                if(rd_ptr_per >= PER_WINDOW*2)
                    rd_ptr_per = 0 ;  
            }         
        }
        
        return WORK_CALLED_PRODUCE;
        
    }



  } /* namespace crew */
} /* namespace gr */

