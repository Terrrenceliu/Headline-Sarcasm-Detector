# Run by typing python3 main.py

## **IMPORTANT:** only collaborators on the project where you run
## this can access this web server!

"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page? 
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building? 
    3. What other features you'd like to develop to help AI write better with a user? 
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model? 
"""

# import basics
import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow import keras
from prep_sentence import prep_sentence
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import send_from_directory
from flask import jsonify
from utils import get_base_url, allowed_file, and_syntax

'''
Coding center code - comment out the following 4 lines of code when ready for production
'''
# load up the model into memory
# you will need to have all your trained model in the app/ directory.
df = pd.read_csv('input_data.csv')
text_result = df.values.flatten().tolist()
MAX_NUM_WORDS = 1000
MAX_SEQUENCE_LENGTH = 100
tokenizer = Tokenizer(num_words=MAX_NUM_WORDS)
tokenizer.fit_on_texts(text_result)
model = keras.models.load_model('./keras model')

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
# port = 12345
# base_url = get_base_url(port)
# app = Flask(__name__, static_url_path=base_url+'static')

'''
Deployment code - uncomment the following line of code when ready for production
'''
app = Flask(__name__)

@app.route('/')
# @app.route(base_url)
def home():
    return render_template('Home.html', generated=None)

@app.route('/', methods=['POST'])
# @app.route(base_url, methods=['POST'])
def home_post():
    return redirect(url_for('results'))

@app.route('/results')
# @app.route(base_url + '/results')
def results():
    return render_template('Home.html', generated=None)

@app.route('/generate_text', methods=["POST"])
# @app.route(base_url + '/generate_text', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text. 
    """

    prompt = request.form['prompt']
    if prompt is not None:
        seq = tokenizer.texts_to_sequences([prep_sentence(prompt)])
        padded = pad_sequences(seq, maxlen=MAX_SEQUENCE_LENGTH)
        pred = model.predict(padded)
        threshold = 0.0001
        diff = abs(pred[0,0] - pred[0,1])
        if np.argmax(pred) == 0 and diff > threshold:
            is_sarcastic = "This news headline is not sarcastic!"
        elif np.argmax(pred) == 1 and diff > threshold:
            is_sarcastic = "This news headline is sarcastic!"
        else:
            is_sarcastic = "Too close to tell! Try another!"

        print(is_sarcastic)

    data = {'generated_ls': is_sarcastic}

    return jsonify(data)

if __name__ == "__main__":
    '''
    coding center code
    '''
    # IMPORTANT: change the cocalcx.ai-camp.org to the site where you are editing this file.
    website_url = 'cocalc3.ai-camp.org'
    print(f"Try to open\n\n    https://{website_url}" + base_url + '\n\n')

    app.run(host = '0.0.0.0', port=port, debug=True)
    import sys; sys.exit(0)

    '''
    scaffold code
    '''
    # Only for debugging while developing
    # app.run(port=80, debug=True)
