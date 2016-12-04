from time import sleep
import json
import os
try:
    if os.uname()[1] == 'raspberrypi':
        import bibiopixel as bp
        import anims
except AttributeError:
    pass
    
    
class Show:
    def __init__(self):
        self.steps = []
        #1 second per step 
        #to be used as delay time after each step
        self.STEP_DELAY = 4 
        #showlist.json should be prefilled with your show configurations
        with open(os.path.join(os.getcwd(),'static/showlist.json'),'r') as f:
            self.SHOW_LIST = json.loads(f.read())
        #lights.json maps light strips (by name)
        #to GPIO pins
        with open(os.path.join(os.getcwd(),'static/lights.json'),'r') as f:
            for name, light in json.loads(f.read()):
                self.LIGHTS[name] = bp.LEDStrip(bp.drivers.LPD8806.DriverLPD8806(light['size'], dev = light['path']), threadedUpdate = True, masterBrightness = 126, pixelWidth = 1)
        #self.startup()
        
    def startup(self):
        print "Setting up GPIO pins..."
        
    def start_show(self, show, light_name):
        status = True
        if light_name = 'all':
            lights = self.LIGHTS.keys()
        else:
            lights = [light_name]
            
        for light in lights:
            anim = get_anim(show)(light)
            try:
                anim.run()
                print "Show started."
            except Exception as ex:
                print ex
                status = False  
        return status
                
    def get_anim(self, show):
        print "Getting animation: %s" % show
        return self.SHOW_LIST[show]
                      
        
        
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
