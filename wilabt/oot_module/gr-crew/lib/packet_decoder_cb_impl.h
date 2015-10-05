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

#ifndef INCLUDED_CREW_packet_decoder_cb_IMPL_H
#define INCLUDED_CREW_packet_decoder_cb_IMPL_H

#include <crew/packet_decoder_cb.h>
#include <boost/crc.hpp>
#include <ctime>

namespace gr {
  namespace crew {

    class packet_decoder_cb_impl : public packet_decoder_cb
    {
        private:
            std::vector<gr_complex> d_symbols;                                  // preamble symbols
            float d_corr_thr ;                                                  // preamble detection threshold
            size_t d_pkt_size, d_header_size, d_payload_size, d_crc_size;       // sizes of all parts of the packet
            int d_state;                                                        // current state of the FSM 
            gr_complex sign_phase ;                                             // complex variable to store the phase rotation
            size_t wr_ptr, rd_ptr ;                                             // read and write pointers for buffers
            unsigned char *buffer_bit, *buffer_byte ;                           // addr pointers of buffers
            unsigned int count_pkt ;                                            // counting variables for packet statistics
            size_t d_bps ;                                                      // bits per symbol (if 1 bpsk, if 2 qpsk) 
            
            timeval time_ref ;                                                  // a variable to keep trap of the time

            char symbol2bit(gr_complex sign_phase, gr_complex in, int bps, bool header) ;             // function to turn symbol into bits
            int bit2byte(void *out_ptr, void *in_ptr, int d_pkt_size, int bps) ;         // function to turn bits into bytes
            int find_trigger_signal(                                            // function to find the start of the preamble and calculate phase difference
                gr_vector_const_void_star &input_items, 
                int pkt_size, 
                int ninput_items, 
                float d_corr_thr,
                gr_complex &sign_phase);
            
        public:                                                                 // clasical GNURadio functions
            packet_decoder_cb_impl(const std::vector<gr_complex> &symbols);
            ~packet_decoder_cb_impl();

            void forecast (int noutput_items, gr_vector_int &ninput_items_required);

            int general_work(int noutput_items,
               gr_vector_int &ninput_items,
               gr_vector_const_void_star &input_items,
               gr_vector_void_star &output_items);
        protected:      
            boost::crc_optimal<8, 0x07, 0xFF, 0x00, false, false>  d_crc_impl;  // 8 bit CRC object used to check the header 
            boost::crc_optimal<32, 0x04C11DB7, 0xFFFFFFFF, 0xFFFFFFFF, true, true>    d_crc_impl_pl; // 32 bit CRC object used to check the payload 
    };

  } // namespace crew
} // namespace gr

#endif /* INCLUDED_CREW_packet_decoder_cb_IMPL_H */

