#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Tx Application
# Generated: Thu Aug 20 17:18:04 2015
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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from crew_packet_gen import crew_packet_gen
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sip
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
        self.usrp_rf_freq = usrp_rf_freq = 2495000000
        self.samp_rate = samp_rate = 200000
        self.preamble = preamble = [1,-1,1,-1,1,1,-1,-1,1,1,-1,1,1,1,-1,1,1,-1,1,-1,-1,1,-1,-1,1,1,1,-1,-1,-1,1,-1,1,1,1,1,-1,-1,1,-1,1,-1,-1,-1,1,1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,1,1,1,1,1,1,-1,-1]
        self.payload_size = payload_size = 500
        self.gap = gap = 20000
        self.gain = gain = 26
        self.fine_freq = fine_freq = 0
        self.digital_gain = digital_gain = 1.0/8
        self.addr = addr = "addr=192.168.10.2"

        ##################################################
        # Blocks
        ##################################################
        self._payload_size_range = Range(50, 500, 10, 500, 200)
        self._payload_size_win = RangeWidget(self._payload_size_range, self.set_payload_size, "payload size in byte", "counter_slider")
        self.top_grid_layout.addWidget(self._payload_size_win, 3,0,1,1)
        self._gap_range = Range(100, 50000, 100, 20000, 200)
        self._gap_win = RangeWidget(self._gap_range, self.set_gap, "Interpacket interval (in samples)", "counter_slider")
        self.top_grid_layout.addWidget(self._gap_win, 2,1,1,1)
        self._gain_range = Range(0, 31.5, 0.5, 26, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "Tx Gain", "counter_slider")
        self.top_grid_layout.addWidget(self._gain_win, 2,0,1,1)
        self._fine_freq_range = Range(-10e3, 10e3, 10, 0, 200)
        self._fine_freq_win = RangeWidget(self._fine_freq_range, self.set_fine_freq, "Fine Frequency", "counter_slider")
        self.top_grid_layout.addWidget(self._fine_freq_win, 3,1,1,1)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
        	",".join((addr, "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0_0.set_center_freq(usrp_rf_freq+fine_freq, 0)
        self.uhd_usrp_sink_0_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0_0.set_antenna("J1", 0)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	usrp_rf_freq+fine_freq, #fc
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
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 0,0,1,2)
        self.crew_packet_gen_0 = crew_packet_gen(
            gap=gap,
            packet_len=payload_size,
        )
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((digital_gain, ))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, "/users/lwei/GITfolder/wirelessacademy/BasicTx/wilabt/file_sent.txt", True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.crew_packet_gen_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.uhd_usrp_sink_0_0, 0))    
        self.connect((self.crew_packet_gen_0, 0), (self.blocks_multiply_const_vxx_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "tx_application")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_usrp_rf_freq(self):
        return self.usrp_rf_freq

    def set_usrp_rf_freq(self, usrp_rf_freq):
        self.usrp_rf_freq = usrp_rf_freq
        self.uhd_usrp_sink_0_0.set_center_freq(self.usrp_rf_freq+self.fine_freq, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.usrp_rf_freq+self.fine_freq, self.samp_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.usrp_rf_freq+self.fine_freq, self.samp_rate)

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble

    def get_payload_size(self):
        return self.payload_size

    def set_payload_size(self, payload_size):
        self.payload_size = payload_size
        self.crew_packet_gen_0.set_packet_len(self.payload_size)

    def get_gap(self):
        return self.gap

    def set_gap(self, gap):
        self.gap = gap
        self.crew_packet_gen_0.set_gap(self.gap)

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0_0.set_gain(self.gain, 0)

    def get_fine_freq(self):
        return self.fine_freq

    def set_fine_freq(self, fine_freq):
        self.fine_freq = fine_freq
        self.uhd_usrp_sink_0_0.set_center_freq(self.usrp_rf_freq+self.fine_freq, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.usrp_rf_freq+self.fine_freq, self.samp_rate)

    def get_digital_gain(self):
        return self.digital_gain

    def set_digital_gain(self, digital_gain):
        self.digital_gain = digital_gain
        self.blocks_multiply_const_vxx_0.set_k((self.digital_gain, ))

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
