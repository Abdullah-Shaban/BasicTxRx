TUD
===

Simple receive source code
--------------------------

This code gives a preview on how a simple receive (Rx) experiment can be run at the TUD Testbed.

Simple transmit source code
---------------------------

This code gives a preview on how a simple transmit (Tx) experiment can be run at the TUD Testbed.

Requirements
============
- Recent version of Matlab
- Access to the Experimental Network through Remote Desktop or direct connection
- TestMan- and HaLo-Library
- Running USRP or PXI system with belonging App (which translates the generic commands for the respective SDR platform)
- Edit halo_defaultConfig file
	- e.g. set right frequency
	- edit path to the mentioned Libraries	

Extension to other languages
============================
- Make sure you can use .NET dlls, e.g. it works with Python
- Load the TestMan.dll
- Use the HaLo-Library as guideline to access TestMan functions
	
Other resources
===============
- internal wiki

Acknowledgements
================
This work was partly funded by the EC under grant agreement n°258301 - Cognitive Radio Experimentation World. 