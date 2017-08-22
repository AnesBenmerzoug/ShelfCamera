# ShelfCamera

A program used to monitor and track people's interaction with a certain shelf in a supermarket

### Prerequisites

In order to run the program som dependencies have to be installed.

#### Linux

First of all, if the program is ran on a Raspberry Pi then you need to update it

    $ sudo apt-get update
    $ sudo apt-get upgrade
    $ sudo rpi-update

Then you have to install the python wrapper for openCV as well as imutils, which is a series of OpenCV convenience functions

    $ sudo apt-get install python-opencv
    $ sudo pip install imutils
    
#### Windows

All you have to do is install pip by following the instructions in this link 
https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip 
and then using it to install numpy and openCV and imutils, which is a series of OpenCV convenience functions

    $ pip install numpy opencv-python imutils
    
