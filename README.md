1e-Disco
========

1E synchronized disco light code.

Installing Required Libraries
=============================
Before you get started installing the libraries, make sure to do these first steps:
* Install Python 2.6 or 2.7 on your computer
* Install Python setup tools on your computer (gives you `easy_install` or `pip`)
* For Windows users: try using Anaconda for your Python distribution, since it comes with all that stuff available in the rather pathetic Windows command line

Next, you will need to install various Python modules that our source needs to run properly.  Typically `easy_install` or `pip` can install the modules we need.  If at any time, either gets upset and throws errors, they'll typically inform you as to what to do next.

For running the server code from source, install the following modules:
* Twisted (networking library)
* Autobahn (websocket library)
* Numpy

To run the beat code from source, you will also need to install the following:
* PyAudio (Google for it and you'll find installers for Windows/Mac/Debian/Ubuntu)
* Python wave module (may already be default? Not sure...)

**NOTE: the beat code currently only runs properly on Mac.  On other operating systems, you must pass a 16bit 44100Hz wav file as a command line argument.**

Finally, to write and compile code for the web UI, you will need a means of compiled Coffeescript and LESS.  There are various tooling utilities you can install to compile these languages down to JS/CSS, and also have them watch your files for any changes and do it automatically.

Using the Various Computer Utilities
======================================
Each utility is either the main server or some peripheral that will attempt to connect to the main server.
* Main server (run from server directory): `python DiscoServer.py`
* Beat server: `python beat/BeatServer.py`

Currently all the network configurations (where to find the disco server, which port, etc) are all in those respective files as globals.  This should be abstracted to runtime args at a later point in time.

To view the simulations, head to `localhost` to see the Web UI.

Running Code on the Controllers
======================================
This section will be completed later.
