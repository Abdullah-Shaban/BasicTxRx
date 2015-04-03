Simple receive example
===================

TCD
-----

The 'ofdm_rx_usrp_to_file.xml' file implements a simple OFDM receiver in Iris.

Requirements:

  * [Basic Iris install](https://github.com/softwareradiosystems)
  OR
  * [Access to the Iris Testbed via SSH](http://www.crew-project.eu/portal/iris/apply-for-an-account)

To run the receiver:

    $ iris ofdm_rx_usrp_to_file.xml

This .xml file consists of three components:
  * usrprx1
    * Tells the USRP frontend to receive transmissions at a centre frequency of 5.01 GHz and bandwidth of 500 kHz.
  * ofdmdemod1
    * Performs the OFDM demodulation of the received signal
  * filerawwriter1
    * Writes the output to the file "out.txt"
