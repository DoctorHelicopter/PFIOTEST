from time import sleep
import json
import os
if os.uname()[1] == 'raspberrypi':
    import pigpio
    
    
class Drink:
    def __init__(self):
        self.steps = []
        #4 seconds per shot (?) 
        #to multiply by the number of shots in the recipe
        self.SHOT_TIME = 4 
        #drinklist.json should be prefilled with your favorite liquids
        with open(os.path.join(os.getcwd(),'static/drinklist.json'),'r') as f:
            self.DRINK_LIST = json.loads(f.read())
        #pumps.json maps drink names (used in the recipe, for readability)
        #to the GPIO pins on the RPi
        #channels are defined using the BCM standard
        with open(os.path.join(os.getcwd(),'static/pumps.json'),'r') as f:
            self.PUMPS = json.loads(f.read())
        #self.startup()
        
    def startup(self):
        print "Setting up GPIO pins..."
        print self.PUMPS.values()
        
    def add_step(self,liquor,time):
        #used in the manual creation of recipes
        self.steps.append((liquor,time))
        
    def get_steps(self,drink):
        self.steps = self.DRINK_LIST[drink]["ingredients"]
        
    def pour(self):
        #at some point i want to make it overlap pours
        #turn them all on
        #then turn them off one at a time
        if os.uname() == 'raspberrypi':
	        gpio = pigpio.pi()
        for step in self.steps:
            go_time = self.SHOT_TIME*step[1]
            print "Pump %s ON" % step[0]
            if os.uname() == 'raspberrypi':
	            gpio.write(self.PUMPS[step[0]],0)
            print "Wait %s" % go_time
            sleep(go_time)
            print "Pump %s OFF" % self.PUMPS[step[0]]
            if os.uname() == 'raspberrypi':
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
