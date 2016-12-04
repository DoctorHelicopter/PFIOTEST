from flask import Flask, render_template, request, send_from_directory, url_for, redirect
from scripts.objects import Drink
import os
import sys
import json
try:
    if os.uname()[1] == 'raspberrypi':
        import bibiopixel as bp
        s = Show()
        s.start_show('default', 'all')
        #import pigpio
        #gpio = pigpio.pi()
except AttributeError:
    pass
app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    #with open(os.path.join(os.getcwd(),'static/pumps.json'),'r') as f:
    #    PUMPS = json.loads(f.read())
    try:
        if os.uname()[1] == 'raspberrypi':
            message = "Please choose a show"
            #import pigpio
            #for p in PUMPS.values():
            #    gpio.write(p,1)
    except AttributeError as ex:
        message = ex
    #if request.method == 'POST':
    #    drink = request.form.get('availabledrinks')
    #    print drink
    #    d = Drink()
    #    if drink == 'Custom':
    #        return redirect(url_for('newcustom'))
    #    else:
    #        d.get_steps(drink)
    #        
    #    print d.steps
    #    try:
    #        print "Pouring..."
    #        d.pour()
    #        message = "Your drink is ready!"
    #    except Exception as ex:
    #        print "Error!"
    #        print ex
    #        message = "There was an error:", ex
    return render_template('index.html',message=message)
    
    
#@app.route('/pour_drink/<drink>', methods=['POST'])
#def pour_drink(drink):
#    print drink
#    d = Drink()
#    d.get_steps(drink)
#    print d.steps
#    try:
#        print "Pouring..."
#        d.pour()
#        message = "Your drink is ready!"
#        code = 200
#    except Exception as ex:
#        print "Error!"
#        print ex
#        message = "There was an error:", ex
#        code = 500
#    return message, code

@app.route('/start_show/<show>', methods=['POST']):
def start_show(show):
    print show
    s = Show()
    try:
        print "Starting %s..." % show
        #If all is successful, this won't ever return.
        #The template should have already moved on and refreshed
        s.start_show(show, 'all')
        message = "Started"
        code = 200
    except Exception as ex:
        print "Error!"
        print ex
        message = "There was an error:", ex
        code = 500
    print message, code
    return message, code
        
        
@app.route('/edit_drink/<drink>', methods=['GET','POST'])
def edit_drink(drink):
    print drink
    if request.method == 'GET':
        #get the current drink
        d = Drink()
        return render_template('editdrink.html',drink=json.dumps(d.DRINK_LIST[drink]), drink_dict=d.DRINK_LIST[drink])
    elif request.method == 'POST':
        steps = []
        name = request.form.get('name')
        liquors = request.form.getlist('liquor') #get by name
        shots = request.form.getlist('shot')
        if len(liquors) != len(shots):
            message = "Invalid entry"
            return render_template('editdrink.html',message=message,drink=json.dumps(d.DRINK_LIST[drink]), drink_dict=d.DRINK_LIST[drink])
        d = Drink()
        for i in range(len(liquors)):
            d.add_step(liquors[i],int(shots[i]))
        result = d.update(name)
        return redirect('/')
    
    
@app.route('/delete_drink/<drink>', methods=['POST'])
def delete_drink(drink):
    print drink
    if drink != 'Custom':
        d = Drink()
        d.delete(drink)
        message = "Drink deleted!"
    return message

        
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
        result = d.save(name)
        if result:
            message = "Drink created!"
        else:
            message = "Drink already exists - not created."
    else:
        message = ""
    return render_template('newcustom.html',message=message)
    
    
if __name__ == '__main__':
    with open(os.path.join(os.getcwd(),'static/shows.json'),'r') as f:
        SHOWS = json.loads(f.read())
    try:
        if os.uname()[1] == 'raspberrypi':
            pass
            #import pigpio
            #gpio = pigpio.pi()
            #for p in PUMPS.values():
            #    gpio.write(p,1)
    except AttributeError:
        pass
        
    app.run(host='0.0.0.0',debug=True)
    