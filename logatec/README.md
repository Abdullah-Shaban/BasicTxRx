Simple transmit example
=======================


LOG-a-TEC
---------

The `logatec.py` script instructs a single sensor node in the City Center
cluster of the LOG-a-TEC testbed to transmit a 200 kHz wide signal at 2.425 GHz
center frequency and 0 dBm transmission power for 10 seconds.

Requirements:

 * Python 2.x.
 * [vesna-alh-tools](https://github.com/sensorlab/vesna-alh-tools) need to be installed.
 * A valid username and password for the LOG-a-TEC testbed (see vesna-alh-tools
   README on how to set it up).

To run the experiment, use:

    $ python logatec.py

See comments in the script for more details.
