from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from Translate import translate_to_braille # Adjust the import statement as needed

import os
import subprocess
import requests
import pybrl as brl
import PyPDF2


app = Flask(__name__)
CORS(app)


@app.route('/translate_to_braille', methods=['POST'])

def translate_to_braille_endpoint():
    """
    Function is used to call the translate_to_braille function. The returned braille unicode is displayed on the front end.

    
    Returns:
    Any: Return translated braille unicode, that is displayed on the vue application. 
    """
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

@app.route('/translate_textbox_to_braille', methods=['POST'])
def translate_textbox_to_braille():
    """
    Function is used to translate the received text into grade-2 unicode braille. Done by using pybrl translate function to translate the text, and texract xelatex to convert the .tex file to .pdf
    
    Returns:
    Any: Return translated braille unicode, that is displayed on the vue application.
    """
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

    return jsonify({'translatedText': translated_text},{'brailleUnicode': content})

def convert_pdf_to_dwg(file_path):
    """
    Function sends request to Zamzar API for file conversion. 
    
    Args:
    file_path (str): path of uploaded input file.
    
    Returns:
    Any: Return the job ID for the conversion.
    """


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
    """
    Function is reflects the uploaded pdf using the reflect_pdf function and passes that into the convert_pdf_to_dwg function.

        
    Returns:
    Any: Return the job ID for the conversion.
    """

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(filename)
        file.save(filepath)

        #Need to reflect PDF before sending to conversion
        relfect_pdf(filepath, 'reflected-input.pdf')

        job_id = convert_pdf_to_dwg('reflected-input.pdf')
        return jsonify({'jobId': job_id})


def download_dwg(job_id):
    """
    Function downloads the converted dwg by querying the Zamzar API with the given job ID. 
    
    Args:
    job_id (Any): jobId of the Zamzar conversion.
    
    Returns:
    str: if successful, path of converted dwg file.
    None: if unsuccessful, nothing is returned.
    """


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
    """
    Funtion downloads dwg onto users local machine, given the jobId of Zamzar conversion.
    
    Args:
    job_id (Any): jobId of the Zamzar conversion.
    
    Returns:
    File: if file, returns dwg file that is downloaded locally onto users machine.
    str: if no file, return 404 'File not found' error.
    """

    dwg_file_path = download_dwg(job_id)
    if dwg_file_path:
        directory = os.path.dirname(dwg_file_path)
        filename = os.path.basename(dwg_file_path)
        return send_from_directory(directory, filename, as_attachment=True)
    else:
        return 'File not found.', 404


@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    """
    Function downloads translated grade-2 unicode braille pdf onto users local machine.

    
    Returns:
    File: returns pdf file that is downloaded locally onto users machine.
    """
    pdf_path = 'output.pdf'  # Update with the path to your PDF file
    return send_file(pdf_path, as_attachment=True)


def relfect_pdf(input_path, output_path):
    """
    Funtion reflects pdf file horizontally to be suitable for laser cutting methods. Uses the scale function from the PyPDF2 library.

    Parameters:
    input_path (str): file path of pdf that needs to be reflected.
    output_path (str): file path of resulting reflected pdf.
    """
    with open(input_path, 'rb') as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            # Reflect horizontally
            page.scale(-1, 1)
            # Add the reflected page to the new PDF
            pdf_writer.add_page(page)

        with open(output_path, 'wb') as output_file:
            pdf_writer.write(output_file)

if __name__ == '__main__':
    app.run(debug=True)
