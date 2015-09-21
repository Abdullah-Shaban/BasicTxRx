TCD
===

Requirements:

  * [Basic Iris install](https://github.com/softwareradiosystems)
  OR
  * [Access to the Iris Testbed via SSH](http://www.crew-project.eu/portal/iris/apply-for-an-account)


Simple receive example
----------------------

The 'ofdm_rx_usrp_to_file.xml' file implements a simple OFDM receiver in Iris.

To run the receiver:

    $ iris ofdm_rx_usrp_to_file.xml

This .xml file consists of three components:
  * usrprx1
    * Tells the USRP frontend to receive transmissions at a centre frequency of 5.01 GHz and bandwidth of 500 kHz.
  * ofdmdemod1
    * Performs the OFDM demodulation of the received signal
  * filerawwriter1
    * Writes the output to the file "out.txt"

Simple transmit example
===================

The 'ofdm_tx_file_to_usrp.xml' file implements a simple OFDM transmitter in Iris.

To run the transmitter:

    $ iris ofdm_tx_file_to_usrp.xml

This .xml file consists of three components:
  * filerawreader1
    * Reads the input data from the file "testdata.txt".
  * ofdmmod1
    * Performs the OFDM modulation of the signal to be transmitted
    * Note: This OFDM modulation technique requires a transmission rate that is double the receive rate.
  * signalscaler1
    * Scales the output signal for transmission by a gain of 0.9
  * usrptx1
    * Tells the USRP frontend to transmit at a centre frequency of 5.01 GHz and transmission rate of 1 Msample/s (1MHz)