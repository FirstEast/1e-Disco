# 1e-Disco

This repository contains all the code for running and controlling the First East Disco Lighting System.

## Installing Required Libraries
Before you get started installing the libraries, make sure to do these first steps:
* Install Python 2.6 or 2.7 on your computer
* Install Python setup tools on your computer (gives you `easy_install` or `pip`)
* For Windows users: try using Anaconda for your Python distribution, since it comes with all that stuff available in the rather pathetic Windows command line

Next, you will need to install various Python modules that our source needs to run properly.  Typically `easy_install` or `pip` can install the modules we need.  If at any time, either gets upset and throws errors, they'll typically inform you as to what to do next.

For running the server code from source, install the following modules:
* Tornado (networking library)
* Twisted (networking library)
* Autobahn (websocket library)
* Numpy
* Pillow or PIL

To run the beat code from source, you will also need to install the following:
* PyAudio (Google for it and you'll find installers for Windows/Mac/Linux)

The Raspberry Pi code requires only Twisted, but you will need to use a SPI library that's provided on the Adafruit Raspberry Pi OS called "Occidentalis".  We (Erin and I) have saved an image of a working disco Raspi that can be copied onto an 8gb SD card and used.

**NOTE: the beat code currently only runs properly on Mac.  On other operating systems, you must pass a 16bit 44100Hz wav file as a command line argument.**

## Make it Run
To get everything started, here's what you'll need to do:
* Get a computer with a static IP and run the DiscoServer on it.
* Get the DJ's computer (or a computer that will playback the same music into headphones) and run the BeatServer on it, using the proper command line args to point at the DiscoServer host (port should be fine).  Choose the proper input device to receive the sound input.
* Edit the `config.txt` files on the Raspi USB sticks to point at the DiscoServer host.  Port and number of lights should be fine.
* Turn on the Raspi's and wait about 30-45 seconds.
* Turn on the PixelPusher and potentially wait 20-30 seconds.

Once all of this is done, you should have a DJ connected to the central server and all the devices connected as well.  Head to the Web UI to check that everything is working and enjoy.

## Using the Server Utilities
Each server is either the main server or some peripheral that will attempt to connect to the main server.
* Main server (run from server directory): `python DiscoServer.py`
* Beat server: `python beat/BeatServer.py`

The DiscoServer network configurations are in the Python file (Goodale port, Bemis port, etc).  Run the BeatServer with the runtime argument `-h` to see a list of the arguments you can use with the BeatServer.

To view the state of the Disco System and control it, open a browser head to port 90 on the DiscoServer machine.  The port number may change back to 80 at some point.

**NOTE: the BeatServer MUST be run after the DiscoServer is up.**

## Running Code on the PixelPusher
**NOTE: I don't actually know how this works.**

The PixelPusher that controls the dancefloor is configured to find the DiscoServer if they are both connected via Ethernet to the network.  Alternatively, you can run the server on your computer and directly connect the controller to your computer.  The server will print a message when it has found the PixelPusher.

## Running Code on the Raspberry Pi
Both Bemis and Goodale currently use Raspberry Pi controllers to control the light patterns.  The Raspi's can handle the network load and output frames quick enough over SPI.

The Raspi code is located in the directory `raspberry-pi`.  Running `PiLights.py` will connect the controller to the central server.  The server, port, and light configurations are kept in a USB stick in a top-level file called `config.txt`.  The first line of the config is the server host, followed by the port, followed by the number of lights.  These configurations are broken out onto a USB stick because modifying that is significantly easier than running the code again on the Raspi's.

Our current saved Raspi image will run the code on boot and look for a USB stick connected to it, so in theory it should just work when you plug it in.  However, if the Raspi doesn't work for some reason, make sure the Ethernet is in the right wall plug, the device is registered with the MIT network garbage, and the config file is formatted properly.  You may also have to unplug and plug it back in a couple times, though that is rare.

If you change the network config, you must unplug the Raspi, edit the config file, and plug it back in.  Future work may want to provide smarter code that will just look at the USB stick periodically for the proper network config and switch accordingly.

**NOTE: do not edit the config file on Windows.  It will add carriage returns that mess up the extremely dumb text parsing.**

## Modifying the Python Networking
If you are interested in modifying the client files (namely `PiLights.py`) or the server files, please make sure to read the code over and get some general understanding of how Twisted works.

The main idea is to create a factory object that will provide a protocol for a given connection when a connection is made.  So when the DiscoServer opens a port to receive the Goodale connection, it also creates a device socket factory.  When the connection is made, that factory creates a receiver which handles sending and receiving messages from the device.

Most of the networking code operates by having some model object stored with the receiver/protocol object, which is then used to read out the next frame of data to pass to the recipient.  Aside from sockets to the various devices, a special connection we don't really understand is used to talk with the PixelPusher, and websockets are used to communicate with the web UI.

## Modifying the Python Patterns
Before you modify the pattern classes, you should first ask yourself the question: can I make my desired pattern out of the existing patterns without going 10 layers deep?  If the answer is yes, you probably shouldn't write a new pattern.

However, if you're intent on it, take a look at the existing pattern classes to get an idea of how it works.  You make an object that extends the Pattern class, has a set of default parameters, and defines how to render itself.  Try to put your new pattern in a sane location in the package hierarchy, and don't go deeper into file hierarchy levels.  I'm fairly certain there's a bit of code that finds all these classes, and I don't think it looks deeper than the depth we go now.

Unfortunately, if your pattern throws an error, it's really really hard to detect.  Be careful, check your Python, and try printing things.  Exceptions aren't very clear when they're jumbled through a layer of Autobahn websocketing.

## Modifying the Web Interface
The web UI is built using Coffeescript, Backbone, SASS, and Handlebars.  All of these are pretty easy to get a handle on.  The code is built using Grunt, which you should also read up on before diving in.  Finally, the Grunt commands rely on some node modules, so before you begin, go into the `contrl_interface` directory and type `npm install`.  If you don't have node, install it.  You may also need the `grunt-cli` package globally installed from npm (`npm install -g grunt-cli`).

Before you begin working, the `grunt watch` command will make Grunt recompile your stuff as it changes, which is very useful even though it occasionally fails with Coffeescript.
