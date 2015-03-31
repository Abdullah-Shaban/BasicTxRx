Simple transmit example
===================

TCD
-----

The 'ofdm_tx_file_to_usrp.xml' file implements a simple OFDM transmitter in Iris.

Requirements:

  * [Basic Iris install](https://github.com/softwareradiosystems)
  OR
  * [Access to the Iris Testbed via SSH](http://www.crew-project.eu/portal/iris/apply-for-an-account)

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
