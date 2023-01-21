import random

from flask import Flask, render_template, send_from_directory, redirect, jsonify, session, url_for, request
from flask import Response

import captcha_dictionary
import clicked_captcha
from flask_session import Session

app = Flask(__name__)
sess = Session()
captcha_images_dictionary = captcha_dictionary.word_images
user_clicks = 0

@app.route("/")
def index():
    checked = session.get('checked')
    return render_template('index.html', checked=checked)

@app.route('/check', methods=['POST'])
def check():
    checked = request.form.get("checked", False)
    session['checked'] = checked
    return redirect("/login", checked=True)

@app.route("/captcha")
def captcha():
    clicked_captcha.prepare_clicks_and_word()
    images = random.sample(list(captcha_images_dictionary.items()), len(captcha_images_dictionary))
    random.shuffle(images)
    session['captcha_clicks'] = clicked_captcha.clicks
    session['captcha_image'] = clicked_captcha.word
    print(int(session['captcha_clicks']))
    print(str(session['captcha_image']))
    return render_template("captcha.html", images=images)

@app.route('/login')
def login():
    return "zalogowano"

@app.route('/refresh', methods=['POST'])
def refresh():
    return redirect('/captcha')

@app.route('/check_image/<image_name>')
def check_image(image_name):
    global user_clicks
    if image_name == clicked_captcha.word:
        user_clicks += 1
        if user_clicks == clicked_captcha.clicks:
            reset_user_clicks()
            return Response(status=200)
        return Response(status=201)
    reset_user_clicks()
    clicked_captcha.prepare_clicks_and_word()
    return Response(status=400)
    
@app.route('/images')
def images():
    return jsonify(prepare_images())


@app.route('/generated_captcha/<path:filename>')
def generated_captcha(filename):
    return send_from_directory('generated_captcha', filename, mimetype='image/png')
    
def prepare_images():
    return random.sample(list(captcha_images_dictionary.items()), len(captcha_images_dictionary))


def reset_user_clicks():
    global user_clicks
    user_clicks = 0


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
    