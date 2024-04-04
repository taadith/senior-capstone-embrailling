from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from Translate import translate_to_braille # Adjust the import statement as needed

import os
import subprocess
import requests
import pybrl as brl
import boto3


app = Flask(__name__)
CORS(app)

s3 = boto3.resource('s3')


@app.route('/translate_to_braille', methods=['POST'])

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

        translated_content = translate_to_braille(filepath)

        return jsonify({'translatedContent': translated_content})


# def upload_file():
#     if 'file' not in request.files:
#         return 'No file part', 400
#     file = request.files['file']
#     if file.filename == '':
#         return 'No selected file', 400
#     if file:
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)
#         return 'File uploaded successfully', 200

# @app.route('/download', methods=['GET'])
# def download_file():
#     # Define the directory where 'output.pdf' is located
#     directory = os.getcwd()  # Assuming 'output.pdf' is in the current working directory
#     filename='output.pdf'
#     print("Serving file from directory:", directory)
#     print("Filename:", filename)
#     try:
#         return send_from_directory(directory, filename=filename, as_attachment=True)
#     except FileNotFoundError:
#         return 'File not found.', 404

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

    print(content)
    
    # Create the new TeX
    output_tex = tex.replace("%%% Content will go here %%%", content)


    with open(output, "w") as f:
        f.write(output_tex)

    subprocess.run(['xelatex', 'output.tex'], check=True)
    # print("PDF generated successfully.")

    with open('output.pdf', 'rb') as data:
        s3.Bucket('filestorageembraillerbucket185717-staging').put_object(Key='output.pdf', Body=data)

    return jsonify({'translatedText': translated_text},{'brailleUnicode': content})

def convert_pdf_to_dwg(file_path):
    zamzar_api_key = "f3f58a14d91cf86b356f18a99bc795ef1124d2af"
    endpoint = "https://api.zamzar.com/v1/jobs"
    source_file = file_path
    target_format = "dwg"

    with open(source_file, 'rb') as file_content:
        response = requests.post(endpoint, data={'target_format': target_format}, files={'source_file': file_content}, auth=(zamzar_api_key, ''))
    data = response.json()

    return data['id']  # Return the job ID for the conversion


@app.route('/convert_to_dwg', methods=['POST'])
def convert_to_dwg_endpoint():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(filename)
        file.save(filepath)

        job_id = convert_pdf_to_dwg(filepath)
        return jsonify({'jobId': job_id})


def download_dwg(job_id):
    zamzar_api_key = "f3f58a14d91cf86b356f18a99bc795ef1124d2af"
    endpoint = f"https://api.zamzar.com/v1/jobs/{job_id}"
    response = requests.get(endpoint, auth=(zamzar_api_key, ''))
    data = response.json()

    # Check if the job is finished
    if data['status'] == 'successful':
        file_id = data['target_files'][0]['id']
        download_url = f"https://api.zamzar.com/v1/files/{file_id}/content"
        local_filename = os.path.join('downloads', f"{file_id}.dwg")

        # Download the DWG file
        response = requests.get(download_url, stream=True, auth=(zamzar_api_key, ''))
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        return local_filename
    else:
        return None

@app.route('/download_dwg/<int:job_id>', methods=['GET'])
def download_dwg_endpoint(job_id):
    dwg_file_path = download_dwg(job_id)
    if dwg_file_path:
        directory = os.path.dirname(dwg_file_path)
        filename = os.path.basename(dwg_file_path)
        return send_from_directory(directory, filename, as_attachment=True)
    else:
        return 'File not found.', 404


if __name__ == '__main__':
    app.run(debug=True)
