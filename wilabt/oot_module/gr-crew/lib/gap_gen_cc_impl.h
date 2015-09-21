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

#ifndef INCLUDED_CREW_GAP_GEN_CC_IMPL_H
#define INCLUDED_CREW_GAP_GEN_CC_IMPL_H

#include <crew/gap_gen_cc.h>

namespace gr {
  namespace crew {

    class gap_gen_cc_impl : public gap_gen_cc
    {
     private:
      bool d_running ; 
      unsigned int work_called ; 
      size_t pkt_len ; 
      size_t pkt_id ; 
      int d_state;  

     public:
      gap_gen_cc_impl(bool running);
      ~gap_gen_cc_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
		       gr_vector_int &ninput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items);
		       
      // set commands
      void set_status(bool status) ;
      bool get_status() ;
      void print_state(int d_state) ;
      void produce_idle_output(gr_vector_void_star &output_items, int noutput_items) ; 
      
      // get 
    };

  } // namespace crew
} // namespace gr

#endif /* INCLUDED_CREW_GAP_GEN_CC_IMPL_H */

