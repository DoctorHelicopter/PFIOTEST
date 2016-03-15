from flask import Flask, render_template, request, send_from_directory, url_for, redirect
from scripts.objects import Drink
import RPi.GPIO as GPIO
app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
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
    
if __name__ == '__main__':
    #Define board layout for channels
    GPIO.setmode(GPIO.BCM)
    #Setup using a list of channels for output
    GPIO.setup(self.PUMPS.values(),GPIO.OUT,initial=GPIO.HIGH)
    app.run(host='0.0.0.0',debug=True)
