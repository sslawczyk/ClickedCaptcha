import os
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import string
from captcha.image import ImageCaptcha
import captcha_dictionary

word_images = {
    "cock": "static/images_captcha/1.jpg",
    "precel": "static/images_captcha/2.jpg",
    "carrot": "static/images_captcha/3.jpg",
    "flower": "static/images_captcha/4.jpg",
    "shoe": "static/images_captcha/5.jpg",
    "hammer": "static/images_captcha/6.jpg",
    "bulb": "static/images_captcha/7.jpg",
    "car": "static/images_captcha/8.jpg"
}

#ilość kliknięć
global clicks
clicks = random.randint(2,9)
global word
word = random.choice(list(word_images))

#określenie danych obrazów za pomocą frameworka captcha
imageWord = ImageCaptcha(width = 300, height = 100)
imageNumber = ImageCaptcha(width = 50, height = 50)

#usunięcie jednej losowej litery
remove_letter = random.randint(0, len(word) -1)

#zastąpienie losowej litery znakiem "#"
new_word = word[:remove_letter] + "#" + word[remove_letter +1:]
captcha_text = new_word
captcha_true_image = word_images[word]

#przypisanie wartości kliknięć
captcha_number = str(clicks)

#wygenerowanie obrazów
word_data = imageWord.generate(captcha_text)
clicks_data = imageNumber.generate(captcha_number)

#zapis obrazów do folderu
imageWord.write(captcha_text,"generated_captcha/captcha.png")
imageNumber.write(captcha_number,"generated_captcha/captcha_number.png")