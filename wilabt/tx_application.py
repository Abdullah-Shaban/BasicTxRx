#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Tx Application
# Generated: Tue Mar 10 21:13:38 2015
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import time

class tx_application(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Tx Application")

        ##################################################
        # Variables
        ##################################################
        self.usrp_rf_freq = usrp_rf_freq = 2405000000
        self.samp_rate = samp_rate = 390625
        self.qpsk = qpsk = digital.constellation_rect(([0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j]), ([0, 1, 2, 3]), 4, 2, 2, 1, 1).base()

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("addr=192.168.20.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(usrp_rf_freq, 0)
        self.uhd_usrp_sink_0.set_gain(10, 0)
        self.digital_constellation_modulator_0 = digital.generic_mod(
          constellation=qpsk,
          differential=True,
          samples_per_symbol=4,
          pre_diff_code=True,
          excess_bw=0.35,
          verbose=False,
          log=False,
          )
        self.blocks_vector_source_x_0_0 = blocks.vector_source_b((255,255), True, 1, [])

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.uhd_usrp_sink_0, 0))



    def get_usrp_rf_freq(self):
        return self.usrp_rf_freq

    def set_usrp_rf_freq(self, usrp_rf_freq):
        self.usrp_rf_freq = usrp_rf_freq
        self.uhd_usrp_sink_0.set_center_freq(self.usrp_rf_freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = tx_application()
    tb.start()
    raw_input('Press Enter to quit: ')
    tb.stop()
    tb.wait()
