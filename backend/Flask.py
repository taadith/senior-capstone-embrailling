from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from Translate import translate_to_braille # Adjust the import statement as needed

import os
import subprocess
import pybrl as brl
import boto3

UPLOAD_FOLDER = 'src/components/uploads'

app = Flask(__name__)
CORS(app)

s3 = boto3.resource('s3')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/translate_to_braille', methods=['POST'])
@app.route('/upload', methods=['POST'])

def translate_to_braille_endpoint():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(filename)
        file.save(filepath)

        # Assuming translate_to_braille function can handle the file path
        translated_content = translate_to_braille(filepath)

        return jsonify({'translatedContent': translated_content})

from werkzeug.utils import secure_filename

@app.route('/translate_textbox_to_braille', methods=['POST'])
def translate_textbox_to_braille():
    print("Inside translate_textboxtobraille")
    
    form_data = request.form
    text = form_data.get('text')

    print(text)

    
    translated_text = brl.translate(text, main_language='english')

    for x in range(len(translated_text)):
        print(translated_text[x])


    tex = ""                         # Template contents and what will be edited.
    output = "output.tex"            # Output path to the tex file
    TEMPLATE_PATH = "template.tex"   # Path to the Template tex file

    with open(TEMPLATE_PATH, 'r', encoding='ISO-8859-1') as f:
        tex = f.read()

    
    # Concatenate all the text. 
    content = ""


    unicode_braille = brl.toUnicodeSymbols(translated_text, flatten=True)
    content = unicode_braille
    
    # Create the new TeX
    output_tex = tex.replace("%%% Content will go here %%%", content)


    with open(output, "w") as f:
        f.write(output_tex)

    subprocess.run(['xelatex', 'output.tex'], check=True)
    # print("PDF generated successfully.")

    with open('output.pdf', 'rb') as data:
        s3.Bucket('filestorageembraillerbucket185717-staging').put_object(Key='output.pdf', Body=data)

    return jsonify({'translatedText': translated_text})

def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return 'File uploaded successfully', 200


if __name__ == '__main__':
    app.run(debug=True)
