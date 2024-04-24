# Backend Documentation
Backend uses a python Flask API that handles braille translation and the Zamzar API that handles file conversion. 

The [pybrl](https://github.com/ant0nisk/pybrl) libarary is within our backend as it is a key componenet in translation. 

## File Structure
- [Flask.py](https://github.com/taadith/senior-capstone-embrailling/blob/dev/backend/Flask.py): Holds endpoints and a majority of functions. Main file used for the backend translation and file conversion.
- [Translate.py](https://github.com/taadith/senior-capstone-embrailling/blob/dev/backend/Translate.py): File that houses function `translate_to_braille` which converts an pdf into grade-2 unicode braille. This file is imported within `Flask.py`.

## Code Documentation
### Flask.py
- [translate_to_braille_endpoint()](https://github.com/taadith/senior-capstone-embrailling/blob/8b15dfffa1c9067955687d1d6e6751a76e7b10a5/backend/Flask.py#L19): Function is used to call the [translate_to_braille](https://github.com/taadith/senior-capstone-embrailling/blob/8b15dfffa1c9067955687d1d6e6751a76e7b10a5/backend/Translate.py#L7C1-L7C5) function. The returned braille unicode is displayed on the front end.

  Returns:
    - Any: Return translated braille unicode, that is displayed on the vue application.
  
- [translate_textbox_to_braille()](https://github.com/taadith/senior-capstone-embrailling/blob/8b15dfffa1c9067955687d1d6e6751a76e7b10a5/backend/Flask.py#L44): Function is used to translate the received text into grade-2 unicode braille. Done by using pybrl translate function to translate the text, and texract xelatex to convert the .tex file to .pdf
    
    Returns:
    - Any: Return translated braille unicode, that is displayed on the vue application.
- [convert_pdf_to_dwg(file_path)](https://github.com/taadith/senior-capstone-embrailling/blob/8b15dfffa1c9067955687d1d6e6751a76e7b10a5/backend/Flask.py#L94):     Function sends request to Zamzar API for file conversion. 
    
    Args:
    - file_path (str): path of uploaded input file.
    
    Returns:
    - Any: Return the job ID for the conversion.

- [convert_to_dwg_endpoint()](https://github.com/taadith/senior-capstone-embrailling/blob/8b15dfffa1c9067955687d1d6e6751a76e7b10a5/backend/Flask.py#L119): Function reflects the uploaded pdf using the [reflect_pdf](https://github.com/taadith/senior-capstone-embrailling/blob/8b15dfffa1c9067955687d1d6e6751a76e7b10a5/backend/Flask.py#L217) function and passes that into the [convert_pdf_to_dwg](https://github.com/taadith/senior-capstone-embrailling/blob/8b15dfffa1c9067955687d1d6e6751a76e7b10a5/backend/Flask.py#L94) function.

        
    Returns:
    - Any: Return the job ID for the conversion.

- [download_dwg()](https://github.com/taadith/senior-capstone-embrailling/blob/8b15dfffa1c9067955687d1d6e6751a76e7b10a5/backend/Flask.py#L147):    Function downloads the converted dwg by querying the Zamzar API with the given job ID. 
    
    Args:
    - job_id (Any): jobId of the Zamzar conversion.
    
    Returns:
    - str: if successful, path of converted dwg file.
    - None: if unsuccessful, nothing is returned.

- [download_dwg_endpoint](https://github.com/taadith/senior-capstone-embrailling/blob/8b15dfffa1c9067955687d1d6e6751a76e7b10a5/backend/Flask.py#L183):     Funtion downloads dwg onto users local machine, given the jobId of Zamzar conversion.
    
    Args:
    - job_id (Any): jobId of the Zamzar conversion.
    
    Returns:
    - File: if file, returns dwg file that is downloaded locally onto users machine.
    - str: if no file, return 404 'File not found' error.

- [download_pdf()](https://github.com/taadith/senior-capstone-embrailling/blob/8b15dfffa1c9067955687d1d6e6751a76e7b10a5/backend/Flask.py#L205):     Function downloads translated grade-2 unicode braille pdf onto users local machine.

    
    Returns:
    - File: returns pdf file that is downloaded locally onto users machine.

- [reflect_pdf()](https://github.com/taadith/senior-capstone-embrailling/blob/8b15dfffa1c9067955687d1d6e6751a76e7b10a5/backend/Flask.py#L217):     Funtion reflects pdf file horizontally to be suitable for laser cutting methods. Uses the scale function from the PyPDF2 library.

    Args:
    - input_path (str): file path of pdf that needs to be reflected.
    - output_path (str): file path of resulting reflected pdf.

### Translate.py
- [translate_to_braille(filename, pdf_password, language)](https://github.com/taadith/senior-capstone-embrailling/blob/8b15dfffa1c9067955687d1d6e6751a76e7b10a5/backend/Translate.py#L7C1-L7C5):     Function used from the pybrl library [samples](https://github.com/ant0nisk/pybrl/blob/master/docs/Samples/pdf_translation/Notebook.ipynb). Function parses a pdf file, translates it to braille, and generates a latex file. Finally using the xelatex subproccess convert to a pdf file.
    
    Args:
    - filename (str): path of uploaded input file.
    - pdf_password (Any): password if pdf is protect, by default 'None' is provided.
    - language (str): language of uploaded pdf and targeted braille, by default 'english' is provided. 

    Returns:
    - Any: Return translated braille unicode, that is displayed on the vue application.

