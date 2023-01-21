import random

from captcha.image import ImageCaptcha

word_images = {
    "rooster": "static/images_captcha/1.jpg",
    "pretzel": "static/images_captcha/2.jpg",
    "carrot": "static/images_captcha/3.jpg",
    "flower": "static/images_captcha/4.jpg",
    "shoe": "static/images_captcha/5.jpg",
    "hammer": "static/images_captcha/6.jpg",
    "bulb": "static/images_captcha/7.jpg",
    "car": "static/images_captcha/8.jpg",
    "bottle": "static/images_captcha/9.jpg"
}

global clicks
global word
clicks = random.randint(2, 9)
word = random.choice(list(word_images))

def prepare_clicks_and_word():
    global clicks
    global word
    clicks = random.randint(2, 9)
    word = random.choice(list(word_images))
    captcha_number = str(clicks)
    remove_letter = random.randint(0, len(word) - 1)
    new_word = word[:remove_letter] + "#" + word[remove_letter +1:]
    imageWord = ImageCaptcha(width=300, height=100)
    imageNumber = ImageCaptcha(width=50, height=50)
    imageWord.write(new_word, "generated_captcha/captcha.png")
    imageNumber.write(captcha_number, "generated_captcha/captcha_number.png")