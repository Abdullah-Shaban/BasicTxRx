##################################################
# GNU Radio Python Flow Graph
# Title: packet generator
# Author: Wei Liu
# Description: generate packets with preabmle, header, and variable packet size, and gap
# Generated: Wed Aug 19 18:41:55 2015
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.digital.utils import tagged_streams
from gnuradio.filter import firdes
import numpy

class crew_packet_gen(gr.hier_block2):

    def __init__(self, gap=30000, packet_len=20):
        gr.hier_block2.__init__(
            self, "packet generator",
            gr.io_signature(1, 1, gr.sizeof_char*1),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.gap = gap
        self.packet_len = packet_len

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.nfilts = nfilts = 32
        self.eb = eb = 0.35
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), eb, 5*sps*nfilts)
        self.preamble = preamble = [1,-1,1,-1,1,1,-1,-1,1,1,-1,1,1,1,-1,1,1,-1,1,-1,-1,1,-1,-1,1,1,1,-1,-1,-1,1,-1,1,1,1,1,-1,-1,1,-1,1,-1,-1,-1,1,1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,1,1,1,1,1,1,-1,-1]
        self.length_tag_key = length_tag_key = "packet_len"
        self.header_len = header_len = 4
        self.crc_len = crc_len = 4
        self.constel = constel = digital.constellation_calcdist(([1,-1]), ([0,1]), 2, 1).base()

        ##################################################
        # Blocks
        ##################################################
        self.preamble_source = blocks.vector_source_b(map(lambda x: (-x+1)/2, preamble), True, 1, [])
        self.padded_bits = blocks.vector_source_b((0,0,0), True, 1, [])
        self.digital_packet_headergenerator_bb_default_0 = digital.packet_headergenerator_bb(header_len*8, length_tag_key)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, length_tag_key)
        self.digital_constellation_modulator_0 = digital.generic_mod(
          constellation=constel,
          differential=False,
          samples_per_symbol=sps,
          pre_diff_code=True,
          excess_bw=eb,
          verbose=False,
          log=False,
          )
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, packet_len, length_tag_key)
        self.blocks_stream_mux_0_0_0 = blocks.stream_mux(gr.sizeof_char*1, (len(preamble)/8,header_len,packet_len+crc_len,3))
        self.blocks_stream_mux_0_0 = blocks.stream_mux(gr.sizeof_gr_complex*1, ((len(preamble)+8*packet_len+8*crc_len+8*header_len+8*3)*sps, gap))
        self.blocks_pack_k_bits_bb_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_null_source_0_0 = blocks.null_source(gr.sizeof_gr_complex*1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_null_source_0_0, 0), (self.blocks_stream_mux_0_0, 1))    
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_stream_mux_0_0_0, 0))    
        self.connect((self.blocks_stream_mux_0_0, 0), (self, 0))    
        self.connect((self.blocks_stream_mux_0_0_0, 0), (self.digital_constellation_modulator_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.digital_crc32_bb_0, 0))    
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_stream_mux_0_0, 0))    
        self.connect((self.digital_packet_headergenerator_bb_default_0, 0), (self.blocks_pack_k_bits_bb_0_0, 0))    
        self.connect((self, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))    
        self.connect((self.padded_bits, 0), (self.blocks_stream_mux_0_0_0, 3))    
        self.connect((self.preamble_source, 0), (self.blocks_pack_k_bits_bb_0, 0))    
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_stream_mux_0_0_0, 2))    
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_packet_headergenerator_bb_default_0, 0))    
        self.connect((self.blocks_pack_k_bits_bb_0_0, 0), (self.blocks_stream_mux_0_0_0, 1))    


    def get_gap(self):
        return self.gap

    def set_gap(self, gap):
        self.gap = gap

    def get_packet_len(self):
        return self.packet_len

    def set_packet_len(self, packet_len):
        self.packet_len = packet_len
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len(self.packet_len)
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len_pmt(self.packet_len)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.eb, 5*self.sps*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.eb, 5*self.sps*self.nfilts))

    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.eb, 5*self.sps*self.nfilts))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.preamble_source.set_data(map(lambda x: (-x+1)/2, self.preamble))

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key

    def get_header_len(self):
        return self.header_len

    def set_header_len(self, header_len):
        self.header_len = header_len

    def get_crc_len(self):
        return self.crc_len

    def set_crc_len(self, crc_len):
        self.crc_len = crc_len

    def get_constel(self):
        return self.constel

    def set_constel(self, constel):
        self.constel = constel

