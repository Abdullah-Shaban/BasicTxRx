# This example shows how to send a signal generation task to a node in the
# LOG-a-TEC testbed.

# You need vesna-alh-tools installed for this example to work. Follow the
# installation instructions at https://github.com/sensorlab/vesna-alh-tools.
from vesna import alh

# vesna-alh-tools uses the standard Python logging module to provide some debug
# information.
import logging

# A standard Python module, required for getting time-of-day.
import time

# Import two classes from vesna-alh-tools we are going to use:
#
# A SignalGenerator object represents a node in the LOG-a-TEC testbed that is
# equipped with a radio that can do signal transmission.
#
# A SignalGeneratorProgram object represents a signal transmission task.
from vesna.alh.signalgenerator import SignalGenerator, SignalGeneratorProgram

# The main function contains all the code for this experiment.
def main():

	# Turn on logging so that we can see requests and responses in the
	# terminal. This is useful to keep track of what is going on during the
	# experiment.
	logging.basicConfig(level=logging.INFO)

	# We must first create an object representing the coordinator node.
	# Each cluster in the LOG-a-TEC has its own coordinator and all
	# communication with the nodes must go through it.
	#
	# The parameters used here correspond to the LOG-a-TEC City Center
	# out-door cluster (see LOG-a-TEC documentation for other valid
	# options).
	#
	# Note that you must have a valid user name and password saved in an
	# "alhrc" file in order for this to work. See vesna-alh-tools README
	# for instructions on how to do that.
	#
	# Also make sure you reserved the cluster in the calendar before
	# running the experiment!
	coor = alh.ALHWeb("https://crn.log-a-tec.eu/communicator", 10002)

	# We will be using node 45 in this example. First we create a generic
	# node object for it.
	node = alh.ALHProxy(coor, 45)

	# We will use our node as a signal generator. Here, we wrap the generic
	# node object with the SignalGenerator class that provides a convenient
	# interface to the signal generation capabilities of the node's radio
	# hardware.
	generator = SignalGenerator(node)

	# Request the list of signal generation configurations that the node
	# supports.
	#
	# Node 45 is equipped with a SNE-ISMTV-2400 radio board that contains a
	# CC2500 reconfigurable transceiver. This tranceiver currently supports
	# one configuration in the 2.4 GHz ISM band.
	gen_config_list = generator.get_config_list()

	# Let's print the list out in a nice format for future reference.
	print
	print "Signal generation devices and configurations available"
	print "======================================================"
	print gen_config_list
	print

	# For a demonstration, we'll transmit a random signal at 2.425 GHz and
	# 0 dBm. We create a TxConfig object that describes the transmission.
	tx_config = gen_config_list.get_tx_config(2425e6, 0)
	if tx_config is None:
		raise Exception("Node can not transmit at the specified frequency and/or power.")

	# Take note of current time.
	now = time.time()

	# SignalGeneratorProgram object allows us to program a node to perform a
	# signal generation task in advance. We'll setup a task for transmission
	# parameters we selected above, starting 5 seconds from now and lasting
	# for 10 seconds.
	gen_program = SignalGeneratorProgram(tx_config, now + 5, 10)

	# Finally, we actually send the programming instructions over the testbed's
	# management network to the node.
	generator.program(gen_program)

main()
