Simple receive example
======================


LOG-a-TEC
---------

The `logatec.py` script performs a simple spectrum sensing experiment in
the 2.4 GHz band on a sensor node in the City Center cluster of the LOG-a-TEC
testbed.

Requirements:

 * Python 2.x.
 * [vesna-alh-tools](https://github.com/sensorlab/vesna-alh-tools) need to be installed.
 * A valid username and password for the LOG-a-TEC testbed (see vesna-alh-tools
   README on how to set it up).

To run the experiment, use:

    $ python logatec.py

The script saves the recorded spectrogram data into `logatec.csv` file in the
current directory. This is a text-based file that is simple to import into
Matlab or other software.

See comments in the script for more details.
