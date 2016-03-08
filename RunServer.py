from flask import Flask, render_template, request, send_from_directory
from scripts.objects import Drink
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        drink = request.form.get('availabledrinks')
        print drink
        d = Drink()
        if drink == 'CUSTOM':
            pass #support this later
        else:
            d.get_steps(drink)
            
        print d.steps
        try:
            print "Pouring..."
            d.pour()
            message = "Your drink is ready!"
        except Exception as ex:
            print "Error!"
            print ex
            message = "There was an error:", ex
    else:
        message = "Please choose a drink"
    return render_template('index.html',message=message)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)