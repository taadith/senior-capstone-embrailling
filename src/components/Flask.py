from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from Translate import translate_to_braille  # Adjust the import statement as needed
import os
import subprocess

UPLOAD_FOLDER = 'src/components/uploads'

app = Flask(__name__)

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
