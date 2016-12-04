from neopixel import *
import time
import sys

def main(args):
    strips = args[1].split(',')
    shows = args[2].split(',')        
    
    strip_list = [setup_strip(STRIPS[name]) for name in strips]
    show_list = [SHOWS[name] for name in shows]
    print "Starting..."
    print "Press Ctrl+C to stop."
    while True:
        for show in show_list:
            for strip in strip_list:
                show(strip)
        
 
def setup_strip(strip):
    s = Adafruit_NeoPixel(strip['LED_COUNT'], strip['LED_PIN'], strip['LED_FREQ_HZ'], strip['LED_DMA'], strip['LED_INVERT'])
    s.begin()
    return s
        
        
def ColorWipe(strip):
    for color in [Color(255,0,0), Color(0,255,0), Color(0,0,255)]:
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(.001)
        
STRIPS = {"Ring" : {
                    "LED_COUNT"   : 24,      # Number of LED pixels.
                    "LED_PIN"     : 18,      # GPIO pin connected to the pixels (must support PWM!).
                    "LED_FREQ_HZ" : 800000,  # LED signal frequency in hertz (usually 800khz)
                    "LED_DMA"     : 5,       # DMA channel to use for generating signal (try 5)
                    "LED_INVERT"  : False,   # True to invert the signal (when using NPN transistor level shift)
                }
        }
SHOWS = {
    "ColorWipe" : ColorWipe
    }  

if __name__=="__main__":
    main(sys.argv)