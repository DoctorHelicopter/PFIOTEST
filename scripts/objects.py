from time import sleep
import json
import os
try:
    if os.uname()[1] == 'raspberrypi':
        from neopixel import *
        import anims
except AttributeError:
    pass
    
    
class Show:
    def __init__(self):
        self.steps = []
        #1 second per step 
        #to be used as delay time after each step
        self.STEP_DELAY = 1 
        self.STRIPS = {"ring" : {
                                    "LED_COUNT"   : 24,      # Number of LED pixels.
                                    "LED_PIN"     : 18,      # GPIO pin connected to the pixels (must support PWM!).
                                    "LED_FREQ_HZ" : 800000,  # LED signal frequency in hertz (usually 800khz)
                                    "LED_DMA"     : 5,       # DMA channel to use for generating signal (try 5)
                                    "LED_INVERT"  : False,   # True to invert the signal (when using NPN transistor level shift)
                                }
                      }
        self.ANIMATIONS = [
            (anims.default, Color(0,255,255))
            (anims.default, Color(255,255,0))
        ]
        print self.ANIMATONS
        print self.STEIPS
        #self.startup()
        
    def startup(self):
        print "Setting up GPIO pins..."
        
    def start_show(self, show, strips=self.STRIPS.keys()):
        status = True
        strip_list = []
        for strip in strips:
            s = self.setup_strip(self.STRIPS[strip])
            strip_list.append(s)
        print "Show started."
        print "Press Ctrl+C to stop."
        while status:
            for s in strip_list:
                print s
                #try:
                #anim(light).run()
                for anim in self.ANIMATIONS:
                    anim[0](s, anim[1])
                #except Exception as ex:
                #    print ex
                #    status = False  
        return status
                
    def setup_strip(self, strip):
        s = Adafruit_Neopixel(strip['LED_COUNT'], strip['LED_PIN'], strip['LED_FREQ_HZ'], strip['LED_DMA'], strip['LED_INVERT'])
        s.begin()
        return s
                      
        
        
    def add_step(self,liquor,time):
        #used in the manual creation of recipes
        self.steps.append((liquor,time))
        
    def get_steps(self,show):
        self.steps = self.SHOW_LIST[show]["steps"]
        
    def pour(self):
        #at some point i want to make it overlap pours
        #turn them all on
        #then turn them off one at a time
        try:
            if os.uname() == 'raspberrypi':
                gpio = pigpio.pi()
                flag = 1
        except AttributeError:
            flag = 0
        for step in self.steps:
            go_time = self.SHOT_TIME*step[1]
            print "Pump %s ON" % step[0]
            if flag:
	            gpio.write(self.PUMPS[step[0]],0)
            print "Wait %s" % go_time
            sleep(go_time)
            print "Pump %s OFF" % self.PUMPS[step[0]]
            if flag:
	            gpio.write(self.PUMPS[step[0]],1)
            
    def save(self,name):
       lowername = name.replace(' ','').lower()
       if name not in self.DRINK_LIST.keys():
           self.DRINK_LIST[lowername] = {"name" : name,
                                         "ingredients" : self.steps}
           self.write()
           return 1
       return 0
           
    def update(self,name):
        lowername = name.replace(' ','').lower()
        self.DRINK_LIST[lowername] = {"name" : name,
                                      "ingredients" : self.steps}
        self.write() 
           
    def delete(self,name):
       lowername = name.replace(' ','').lower()
       del self.DRINK_LIST[lowername]
       self.write()
            
    def write(self):
       with open(os.path.join(os.getcwd(),'static/drinklist.json'),'w') as f:
           f.write(json.dumps(self.DRINK_LIST))
