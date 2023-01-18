from flask import Flask, render_template, send_from_directory, redirect, request, jsonify, session, flash, url_for
import subprocess
import templates
import images_captcha
import generated_captcha
import os
import random
import captcha_dictionary
import clicked_captcha

app = Flask(__name__)
app.secret_key = "secret_key"
captcha_images_dictionary = clicked_captcha.word_images
captcha_image = clicked_captcha.word
captcha_clicks = clicked_captcha.clicks
user_clicks = 0

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/captcha")
def captcha():
    images = random.sample(list(captcha_images_dictionary.items()), len(captcha_images_dictionary))
    random.shuffle(images)
    return render_template("clicked_captcha_page.html",images=images)

@app.route('/login')
def login():
    return render_template("index.html",images=images)

@app.route('/refresh')
def refresh():
    return redirect(url_for(login))

@app.route('/check_image/<image_name>')
def check_image(image_name):
    global user_clicks
    captcha_image = clicked_captcha.word
    captcha_clicks = clicked_captcha.clicks
    if image_name == captcha_image:
        user_clicks += 1
        if user_clicks == captcha_clicks:
            return redirect('/login')
        else:
            return jsonify("trafiłeś")
    elif image_name != captcha_image:
        session.clear()
        subprocess.call(['python','clicked_captcha.py'])
        jsonify(message="Wrong image")
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
    session.clear()
    subprocess.call(['python','clicked_captcha.py'])
    return redirect('/captcha')


if __name__ == '__main__':
    
    app.run(debug=True)
    