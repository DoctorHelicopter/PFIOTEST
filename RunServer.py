from flask import Flask, render_template, request, send_from_directory, url_for, redirect
from scripts.objects import Drink
import os
import sys
import json
#import RPi.GPIO as GPIO
import pigpio
app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    #if not GPIO.getmode():
    #GPIO.setmode(GPIO.BCM)
    with open(os.path.join(os.getcwd(),'static/pumps.json'),'r') as f:
        PUMPS = json.loads(f.read())
    #GPIO.setup(PUMPS.values(),GPIO.OUT)
    #GPIO.output(PUMPS.values(),GPIO.HIGH)
    gpio = pigpio.pi()
    for p in PUMPS.values():
        gpio.write(p,1)
    if request.method == 'POST':
        drink = request.form.get('availabledrinks')
        print drink
        d = Drink()
        if drink == 'Custom':
            return redirect(url_for('newcustom'))
        else:
            d.get_steps(drink)
            
        print d.steps
        try:
            print "Pouring..."
            d.pour()
            #d.close()
            message = "Your drink is ready!"
        except Exception as ex:
            print "Error!"
            print ex
            #d.close()
            message = "There was an error:", ex
    else:
        message = "Please choose a drink"
    return render_template('index.html',message=message)
    
    
@app.route('/newcustom', methods=['POST','GET'])
def newcustom():
    if request.method == 'POST':
        steps = []
        name = request.form.get('name')
        liquors = request.form.getlist('liquor') #get by name
        shots = request.form.getlist('shot')
        if len(liquors) != len(shots):
            message = "Invalid entry"
            return render_template('newcustom.html',message=message)
        d = Drink()
        for i in range(len(liquors)):
            d.add_step(liquors[i],int(shots[i]))
        d.save(name)
        message = "Drink created!"
    else:
        message = ""
    return render_template('newcustom.html',message=message)
    
    
@app.route('/deletedrink', methods=['POST'])
def delete_drink():
    drink = request.form.get('availabledrinks')
    print drink
    if drink != 'Custom':
        d = Drink()
        d.delete(drink)
        message = "Drink deleted!"
    return redirect('/')
    
#if __name__ == '__main__':
    #with open(os.path.join(os.getcwd(),'static/pumps.json'),'r') as f:
    #    PUMPS = json.loads(f.read())
    #Define board layout for channels
    #GPIO.setmode(GPIO.BCM)
    #Setup using a list of channels for output
    #GPIO.setup(PUMPS.values(),GPIO.OUT)#,initial=GPIO.HIGH)
    #GPIO.output(PUMPS.values(),GPIO.HIGH)
    #try:
    #    app.run(host='0.0.0.0',debug=True)
    #except KeyboardInterrupt:
    #    GPIO.cleanup()
    #    sys.exit()
