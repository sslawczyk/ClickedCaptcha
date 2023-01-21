import random

from captcha.image import ImageCaptcha
import captcha_dictionary

word_images = captcha_dictionary.word_images

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