#!/usr/bin/python2

from flask import Flask, request, session, \
                  redirect, url_for, render_template, flash
from contextlib import closing

from control import *

init_board()

# configuration
DEBUG = True
SECRET_KEY = b'-\x0e[\xda\xd7@\xbf\xdf\xef\xc2\xdcD#3E-u\xba\xbc\xac\xca\xf4\xd9\n'
USERNAME = 'pi'
PASSWORD = 'raspberry'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home():
  if not session.get('logged_in'):
    return redirect(url_for('login'))
  else:
    return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
  error = None
  if request.method == 'POST':
    if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
      session['logged_in'] = True     
      session['username'] = request.form['username']
      flash('You were logged in')
      return redirect(url_for('home'))
    else:
      error = 'Wrong username or password'
  return render_template('login.html', error=error)

@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  session.pop('username', None)
  flash('You were logged out')
  return redirect(url_for('login'))

@app.route('/lights', methods=['POST'])
def lights():
  if request.form['red'] == 'on':   GPIO.output(RED, 1)
  else:                             GPIO.output(RED, 0)
  if request.form['blue'] == 'on':  GPIO.output(BLUE, 1)
  else:                             GPIO.output(BLUE, 0)
  if request.form['green'] == 'on': GPIO.output(GREEN, 1)
  else:                             GPIO.output(GREEN, 0)
  return redirect(url_for('home'))

@app.route('/message', methods=['POST'])
def message():
  if request.form['msg']:
    lcd.message(request.form['msg'])
  return redirect(url_for('home'))

if __name__ == "__main__":
  app.run('0.0.0.0',8800)
