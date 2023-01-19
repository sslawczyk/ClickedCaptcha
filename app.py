from flask import Flask, render_template, send_from_directory, redirect, request, jsonify, session, flash, url_for, sessions
import subprocess
import templates
import images_captcha
import generated_captcha
import os
import random
import captcha_dictionary
import clicked_captcha
from flask_session import Session
import secrets
from flask import current_app

app = Flask(__name__)
sess = Session()
captcha_images_dictionary = captcha_dictionary.word_images
user_clicks = 0


@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/captcha")
def captcha():
    images = random.sample(list(captcha_images_dictionary.items()), len(captcha_images_dictionary))
    random.shuffle(images)
    session['captcha_clicks'] = clicked_captcha.clicks
    session['captcha_image'] = clicked_captcha.word
    return render_template("index.html",images=images)

@app.route('/login')
def login():
    return "zalogowano"

@app.route('/refresh')
def refresh():
    return redirect(url_for(login))

@app.route('/check_image/<image_name>')
def check_image(image_name):
    global user_clicks
    captcha_image = session.get('captcha_image')
    captcha_clicks = session.get('captcha_clicks')
    print(str(captcha_image))
    print(str(clicked_captcha.word))
    print(int(captcha_clicks))
    print(int(clicked_captcha.clicks))
    if image_name == captcha_image:
        user_clicks += 1
        if user_clicks == captcha_clicks:
            session.pop('captcha_clicks', None)
            session.pop('captcha_image', None)
            return redirect('/login')
            
    elif image_name != captcha_image:
        session.pop('captcha_clicks', None)
        session.pop('captcha_image', None)
        jsonify(message="Wrong image")
        subprocess.call(['python3','clicked_captcha.py'])
        return redirect('/captcha')
    
@app.route('/images')
def images():
    images = random.sample(list(captcha_images_dictionary.items()), len(captcha_images_dictionary))
    return jsonify(images)
@app.route('/generated_captcha/<path:filename>')
def generated_captcha(filename):
    return send_from_directory('generated_captcha', filename, mimetype='image/png')

@app.route('/run_script', methods=['GET','POST'])
def run_script():
    subprocess.call(['python3','clicked_captcha.py'])
    session['captcha_clicks'] = clicked_captcha.clicks
    session['captcha_image'] = clicked_captcha.word
    print(str(session['captcha_image']))
    print(str(clicked_captcha.word))
    print(int(session['captcha_clicks']))
    print(int(clicked_captcha.clicks))
    return redirect('/captcha')
    
if __name__ == '__main__':
    app.config.update (
    TESTING=True,
    DEBUG= True,
    FLASK_ENV='development',
    SECRET_KEY='GDtfDCFYjD',
    SESSION_TYPE = 'filesystem'
)
    sess = Session()
    sess.init_app(app)
    
    app.run(debug=True)
    