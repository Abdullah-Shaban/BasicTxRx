#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Tx Application
# Generated: Wed Dec  2 17:25:11 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.digital.utils import tagged_streams
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import numpy
import sip
import sys
import time

from distutils.version import StrictVersion
class tx_application(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Tx Application")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Tx Application")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "tx_application")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.preamble = preamble = [1,-1,1,-1,1,1,-1,-1,1,1,-1,1,1,1,-1,1,1,-1,1,-1,-1,1,-1,-1,1,1,1,-1,-1,-1,1,-1,1,1,1,1,-1,-1,1,-1,1,-1,-1,-1,1,1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,1,1,1,1,1,1,-1,-1]
        self.usrp_rf_freq = usrp_rf_freq = 2475e6
        self.sps = sps = 4
        self.samp_rate = samp_rate = 200000
        self.qpsk = qpsk = digital.constellation_rect(([0.25*(0.707+0.707j),0.25*( -0.707+0.707j),0.25*( -0.707-0.707j), 0.25*(0.707-0.707j)]), ([0, 1, 2, 3]), 4, 2, 2, 1, 1).base()
        self.preamble_qpsk = preamble_qpsk = map(lambda x: x*(1+1j)/pow(2,0.5), preamble)
        self.payload_size = payload_size = 100
        self.length_tag_key = length_tag_key = "packet_len"
        self.header_len = header_len = 4
        self.gain = gain = 26
        self.eb = eb = 0.35
        self.digital_gain = digital_gain = 1.0/4
        self.crc_len = crc_len = 4
        self.bps = bps = 2
        self.addr = addr = "addr=192.168.60.2"

        ##################################################
        # Blocks
        ##################################################
        self._usrp_rf_freq_range = Range(2400e6, 2500e6, 100e3, 2475e6, 200)
        self._usrp_rf_freq_win = RangeWidget(self._usrp_rf_freq_range, self.set_usrp_rf_freq, "Rx Frequency", "counter_slider")
        self.top_layout.addWidget(self._usrp_rf_freq_win)
        self._gain_range = Range(0, 31.5, 0.5, 26, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "Tx Gain", "counter_slider")
        self.top_layout.addWidget(self._gain_win)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
        	",".join((addr, "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_0.set_center_freq(usrp_rf_freq, 0)
        self.uhd_usrp_sink_0_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0_0.set_antenna("J1", 0)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	usrp_rf_freq, #fc
        	samp_rate, #bw
        	"QT GUI Plot", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-120, 20)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if complex == type(float()):
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qpsk_preamp_to_bits = blocks.vector_source_b(map(lambda x: int((x*(1j-1)/pow(2,0.5)).real+1), preamble_qpsk), True, 1, [])
        self.padded_bits = blocks.vector_source_b((0,0,0,0,0,0,0,0), True, 1, [])
        (self.padded_bits).set_block_alias("padded bits")
        self.digital_packet_headergenerator_bb_default_0 = digital.packet_headergenerator_bb(header_len*8, length_tag_key)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, length_tag_key)
        self.digital_constellation_modulator_0 = digital.generic_mod(
          constellation=qpsk,
          differential=False,
          samples_per_symbol=sps,
          pre_diff_code=True,
          excess_bw=eb,
          verbose=False,
          log=False,
          )
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        self.blocks_stream_to_tagged_stream_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, payload_size, length_tag_key)
        self.blocks_stream_mux_0_0_0 = blocks.stream_mux(gr.sizeof_char*1, (len(preamble)*bps/8,header_len,payload_size+crc_len,6))
        self.blocks_pack_k_bits_bb_0_1 = blocks.pack_k_bits_bb(8)
        self.blocks_pack_k_bits_bb_0_0 = blocks.pack_k_bits_bb(8)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((digital_gain, ))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, "/users/lwei/GITfolder/wirelessacademy/BasicTxRx/wilabt/file_sent.txt", True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_stream_to_tagged_stream_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0_0, 0))    
        self.connect((self.blocks_pack_k_bits_bb_0_1, 0), (self.blocks_stream_mux_0_0_0, 0))    
        self.connect((self.blocks_stream_mux_0_0_0, 0), (self.digital_constellation_modulator_0, 0))    
        self.connect((self.blocks_stream_to_tagged_stream_0_0, 0), (self.digital_crc32_bb_0, 0))    
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_pack_k_bits_bb_0_1, 0))    
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.digital_packet_headergenerator_bb_default_0, 0), (self.blocks_pack_k_bits_bb_0_0, 0))    
        self.connect((self.padded_bits, 0), (self.blocks_stream_mux_0_0_0, 3))    
        self.connect((self.qpsk_preamp_to_bits, 0), (self.blocks_unpack_k_bits_bb_0, 0))    
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_stream_mux_0_0_0, 2))    
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_packet_headergenerator_bb_default_0, 0))    
        self.connect((self.blocks_pack_k_bits_bb_0_0, 0), (self.blocks_stream_mux_0_0_0, 1))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tx_application")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble
        self.set_preamble_qpsk(map(lambda x: x*(1+1j)/pow(2,0.5), self.preamble))

    def get_usrp_rf_freq(self):
        return self.usrp_rf_freq

    def set_usrp_rf_freq(self, usrp_rf_freq):
        self.usrp_rf_freq = usrp_rf_freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.usrp_rf_freq, self.samp_rate)
        self.uhd_usrp_sink_0_0.set_center_freq(self.usrp_rf_freq, 0)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_freq_sink_x_0.set_frequency_range(self.usrp_rf_freq, self.samp_rate)
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_preamble_qpsk(self):
        return self.preamble_qpsk

    def set_preamble_qpsk(self, preamble_qpsk):
        self.preamble_qpsk = preamble_qpsk
        self.qpsk_preamp_to_bits.set_data(map(lambda x: int((x*(1j-1)/pow(2,0.5)).real+1), self.preamble_qpsk),[])

    def get_payload_size(self):
        return self.payload_size

    def set_payload_size(self, payload_size):
        self.payload_size = payload_size
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len(self.payload_size)
        self.blocks_stream_to_tagged_stream_0_0.set_packet_len_pmt(self.payload_size)

    def get_length_tag_key(self):
        return self.length_tag_key

    def set_length_tag_key(self, length_tag_key):
        self.length_tag_key = length_tag_key

    def get_header_len(self):
        return self.header_len

    def set_header_len(self, header_len):
        self.header_len = header_len

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0_0.set_gain(self.gain, 0)

    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb

    def get_digital_gain(self):
        return self.digital_gain

    def set_digital_gain(self, digital_gain):
        self.digital_gain = digital_gain
        self.blocks_multiply_const_vxx_0.set_k((self.digital_gain, ))

    def get_crc_len(self):
        return self.crc_len

    def set_crc_len(self, crc_len):
        self.crc_len = crc_len

    def get_bps(self):
        return self.bps

    def set_bps(self, bps):
        self.bps = bps

    def get_addr(self):
        return self.addr

    def set_addr(self, addr):
        self.addr = addr


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if(StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0")):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = tx_application()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
