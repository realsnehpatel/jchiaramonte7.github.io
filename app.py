
from flask import Flask, render_template, request, flash
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError
from flask_mail import Mail, Message
import os

mail = Mail()

app = Flask(__name__)

app.secret_key = 'development key'

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'jeremychiaramonte@gmail.com',
    "MAIL_PASSWORD": '' # put in your password for your email in here  
    
}

app.config.update(mail_settings)
mail.init_app(app)



class ContactForm(Form):
    name = TextField("Name",  [validators.DataRequired()])
    email = TextField("Email",  [validators.DataRequired(), validators.Email()])
    subject = TextField("Subject",  [validators.DataRequired()])
    message = TextAreaField("Message",  [validators.DataRequired()])
    submit = SubmitField("Send")

@app.route('/', methods=['GET', 'POST'])

def contact():
  form = ContactForm()
 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('index.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=[app.config['MAIL_USERNAME']])
      msg.body = """From: %s &lt;%s&gt; %s""" % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template('index.html', success=True)
 
  elif request.method == 'GET':
    return render_template('index.html', form=form)

def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)