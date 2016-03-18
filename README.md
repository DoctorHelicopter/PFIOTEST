PYDRINKBOT V0.2
===============

Introduction
------------
<p>This project started as a keypad hooked up to an Arduino controlling some pumps, and I was like "yeah, that's lame."

So I got a Raspberry Pi and hooked that up to the pumps instead. I'm using eight of the GPIO pins on the board, plus the 5v and a ground, hooked up to a solid state relay board with 8 relays. The relays are wired up with 12v power, and each one controls a peristaltic pump. This project is for the Flask server that controls all of that.</p> 
    
Dependencies
------------
1. A Raspberry Pi
~*It needs to connect to your home network. You can get an adapter, or use a Pi 3.
2. Python 2.7.6+, and the following modules:
~1. Flask (and dependencies)
~2. RPi.GPIO (note: this only works on the Pi, can't be tested on another machine)
3. Apache 2

```
Just run the following on your Pi:

# apt-get update
# apt-get upgrade
# apt-get install apache2 libapache2-mod-wsgi python-pip
# pip install Flask RPi.GPIO
```