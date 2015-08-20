#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Rx Application
# Generated: Thu Aug 20 17:18:09 2015
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
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import crew
import sip
import sys
import time

from distutils.version import StrictVersion
class rx_application(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Rx Application")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Rx Application")
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

        self.settings = Qt.QSettings("GNU Radio", "rx_application")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.nfilts = nfilts = 32
        self.eb = eb = 0.35
        self.usrp_rf_freq = usrp_rf_freq = 2495e6
        self.samp_rate = samp_rate = 200000
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), eb, 5*sps*nfilts)
        self.preamble = preamble = [1,-1,1,-1,1,1,-1,-1,1,1,-1,1,1,1,-1,1,1,-1,1,-1,-1,1,-1,-1,1,1,1,-1,-1,-1,1,-1,1,1,1,1,-1,-1,1,-1,1,-1,-1,-1,1,1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,1,1,1,1,1,1,-1,-1]
        self.matched_filter = matched_filter = firdes.root_raised_cosine(nfilts, nfilts, 1, eb, int(11*sps*nfilts))
        self.gain = gain = 30
        self.digital_gain = digital_gain = 30
        self.constel = constel = digital.constellation_calcdist(([1,- 1]), ([0,1]), 2, 1).base()
        self.addr = addr = "addr=192.168.20.2"

        ##################################################
        # Blocks
        ##################################################
        self._usrp_rf_freq_range = Range(2400e6, 2500e6, 100e3, 2495e6, 200)
        self._usrp_rf_freq_win = RangeWidget(self._usrp_rf_freq_range, self.set_usrp_rf_freq, "Rx Frequency", "counter_slider")
        self.top_grid_layout.addWidget(self._usrp_rf_freq_win, 3,0,1,2)
        self._gain_range = Range(0, 40, 0.5, 30, 200)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "Rx Gain", "counter_slider")
        self.top_grid_layout.addWidget(self._gain_win, 2,0,1,1)
        self._digital_gain_range = Range(0, 60, 1, 30, 200)
        self._digital_gain_win = RangeWidget(self._digital_gain_range, self.set_digital_gain, "Digital Gain", "counter_slider")
        self.top_grid_layout.addWidget(self._digital_gain_win, 2,1,1,1)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join((addr, "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(usrp_rf_freq, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.uhd_usrp_source_0.set_antenna("J1", 0)
        self.qtgui_time_sink_x_1_0 = qtgui.time_sink_f(
        	50, #size
        	samp_rate, #samp_rate
        	"Packet Error Rate", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_1_0.set_update_time(0.10)
        self.qtgui_time_sink_x_1_0.set_y_axis(0, 100)
        
        self.qtgui_time_sink_x_1_0.set_y_label("PER", "%")
        
        self.qtgui_time_sink_x_1_0.enable_tags(-1, False)
        self.qtgui_time_sink_x_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.5, 0, 0, "")
        self.qtgui_time_sink_x_1_0.enable_autoscale(False)
        self.qtgui_time_sink_x_1_0.enable_grid(True)
        self.qtgui_time_sink_x_1_0.enable_control_panel(True)
        
        if not True:
          self.qtgui_time_sink_x_1_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [0, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_0_win, 1,0,1,2)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
        	40000, #size
        	samp_rate, #samp_rate
        	"", #name
        	3 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-200, 400)
        
        self.qtgui_time_sink_x_1.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 200, 0.010, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_1.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_1_win, 0,0,1,1)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
        	20000, #size
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(False)
        
        if not True:
          self.qtgui_const_sink_x_0_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_win, 0,1,1,1)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, 2*3.14/100.0, (rrc_taps), nfilts, 0, 0.5, 1)
        self.digital_fll_band_edge_cc_0 = digital.fll_band_edge_cc(sps, eb, 45, 2*3.14/100.0)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(1*3.14/50.0, 2, False)
        self.digital_correlate_and_sync_cc_0 = digital.correlate_and_sync_cc((preamble), (matched_filter), sps)
        self.crew_packet_decoder_cb_0 = crew.packet_decoder_cb((preamble))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((digital_gain, ))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, "/users/lwei/file_received.txt", False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_time_sink_x_1, 1))    
        self.connect((self.blocks_complex_to_float_0, 1), (self.qtgui_time_sink_x_1, 2))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_time_sink_x_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.digital_fll_band_edge_cc_0, 0))    
        self.connect((self.crew_packet_decoder_cb_0, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.crew_packet_decoder_cb_0, 1), (self.qtgui_time_sink_x_1_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.crew_packet_decoder_cb_0, 0))    
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_0_0, 0))    
        self.connect((self.digital_fll_band_edge_cc_0, 0), (self.digital_correlate_and_sync_cc_0, 0))    
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_costas_loop_cc_0, 0))    
        self.connect((self.digital_correlate_and_sync_cc_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))    
        self.connect((self.digital_correlate_and_sync_cc_0, 1), (self.blocks_complex_to_float_0, 0))    
        self.connect((self.digital_correlate_and_sync_cc_0, 1), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_const_vxx_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rx_application")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_matched_filter(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1, self.eb, int(11*self.sps*self.nfilts)))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.eb, 5*self.sps*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_matched_filter(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1, self.eb, int(11*self.sps*self.nfilts)))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.eb, 5*self.sps*self.nfilts))

    def get_eb(self):
        return self.eb

    def set_eb(self, eb):
        self.eb = eb
        self.set_matched_filter(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1, self.eb, int(11*self.sps*self.nfilts)))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), self.eb, 5*self.sps*self.nfilts))

    def get_usrp_rf_freq(self):
        return self.usrp_rf_freq

    def set_usrp_rf_freq(self, usrp_rf_freq):
        self.usrp_rf_freq = usrp_rf_freq
        self.uhd_usrp_source_0.set_center_freq(self.usrp_rf_freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1_0.set_samp_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.set_taps((self.rrc_taps))

    def get_preamble(self):
        return self.preamble

    def set_preamble(self, preamble):
        self.preamble = preamble

    def get_matched_filter(self):
        return self.matched_filter

    def set_matched_filter(self, matched_filter):
        self.matched_filter = matched_filter

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_source_0.set_gain(self.gain, 0)

    def get_digital_gain(self):
        return self.digital_gain

    def set_digital_gain(self, digital_gain):
        self.digital_gain = digital_gain
        self.blocks_multiply_const_vxx_0.set_k((self.digital_gain, ))

    def get_constel(self):
        return self.constel

    def set_constel(self, constel):
        self.constel = constel

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
    tb = rx_application()
    tb.start()
    tb.show()
    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None #to clean up Qt widgets
