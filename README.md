NitroRestClient
===============

This package is used for automation of Citrix Netscaler devices. A class module is provided which implements
the main functionality in a "client" approach. Instantiating the NitroRestClient into an object will create a "client."
This module has been tested on the following Netscaler OS: NS10.1 Build 118.7nc, NS10.5 55.8nc

Two examples of the class in use can be found in the root. These examples disable and enable a server object in the Netscaler. The Client itself is found in bin/

The request modules is packaged with the client for simplicity. 