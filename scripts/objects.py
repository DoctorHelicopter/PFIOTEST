#import pifacedigitalio as pfio
from time import sleep
import json
import os
class Drink:
    def __init__(self):
        self.steps = []
        with open(os.path.join(os.getcwd(),'static\\drinklist.json'),'r') as f:
            self.DRINK_LIST = json.loads(f.read())
        with open(os.path.join(os.getcwd(),'static\\pumps.json'),'r') as f:
            self.PUMPS = json.loads(f.read())
        
    def add_step(self,liquor,time):
        self.steps.append((liquor,time))
        
    def get_steps(self,drink):
        self.steps = self.DRINK_LIST[drink]["ingredients"]
        
    def pour(self):
        #pfio.init()
        for step in self.steps:
            print "Pump %s ON" % step[0]
            #pfio.digital_write(self.PUMPS[step[0]],1)
            print "Wait %s" % step[1]
            sleep(step[1])
            print "Pump %s OFF" % step[0]
            #pfio.digital_write(self.PUMPS[step[0]],0)
            sleep(1)