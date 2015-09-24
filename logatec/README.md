Simple transmit example
=======================


LOG-a-TEC
---------

The `logatec.py` script instructs a single sensor node in the City Center
cluster of the LOG-a-TEC testbed to transmit a 200 kHz wide signal at 2.425 GHz
center frequency and 0 dBm transmission power for 10 seconds.

Experiments running on LOG-a-TEC testbed are controlled over the Internet from
a Python script running on the user's computer. To run an experiment, you need
the following installed on your system:

 * Python 2.7 (usually already installed on Linux systems) and
 * a valid username and password for the LOG-a-TEC testbed saved in `.alhrc` in
   your home directory (see https://github.com/sensorlab/vesna-alh-tools for
   details).

To install required Python packages, run:

    $ pip install --user -r requirements.txt

To run the experiment:

    $ python logatec.py

See comments in the script for more details.
