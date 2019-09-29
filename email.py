from flask import *
from flask_mail import *
from random import randint

app = Flask(__name__)

#Flask mail configuration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME'] = 'abc@gmail.com'
app.config['MAIL_PASSWORD'] = '*********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#instantiate the Mail class
mail = Mail(app)
otp = randint(000000,999999)

@app.route('/verify', methods = ['POST'])
def sendmail():
    email = request.json.get('email')
    msg = Message ('OTP', sender = 'abc7@gmail.com', recipients = email.split())
    msg.body = str(otp)
    mail.send(msg)

    response ={
    'alert' : 'Email Sent !'
    }
    return jsonify(response),200

@app.route('/validate', methods = ['POST'])
def validate():
    user_otp = request.json.get('OTP')
    if otp == int(user_otp):
        response ={
            'alert' : 'Verified'
        }
    else:
        response = {
            'alert' : "Wrong OTP"
        }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug = True)
