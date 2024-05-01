# TAMU Senior Capstone Project - Embrailling

Web app and associated API to convert english text or pdf to AutoCAD file containing grade-2 braille, for use in TAMU laser cutter to produce physical braille on capsule paper.

## Overview
Vue.js frontend application that makes calls to Python Flask API backend, backend uses pybrl for braille translation and Zamzar for file conversion.

- File Structure
- Local Setup
- User Guide

## File Structure
Code is split up into two main sections, Vue.js front end, and Flask API backend. 

  - Frontend: All the frontend componenets are under the `src` folder. This includes the main `App.vue` file and the main `BrailleTranslator.vue` componenet.
      - [Documentation](https://github.com/taadith/senior-capstone-embrailling/blob/dev/docs/frontend/README.md)
  - Backend: All the backend componenets are under the `backend` folder. This includes the two main files used in the API for translation and conversion, `Flask.py` and `Translate.py`. It also includes the entire [pybrl](https://github.com/ant0nisk/pybrl) library which is used for translation. 
    - [Documentation](https://github.com/taadith/senior-capstone-embrailling/tree/dev/docs/backend)

## Local Setup

### First time setup
```
bash setup.sh
```
This script runs these commands:
```
npm install
sudo pip install -r backend/requirements.txt
sudo apt-get update
sudo apt-get install -y texlive texlive-xetex
```

### Project setup
```
npm install
```

#### Compiles and hot-reloads for development
```
npm run serve
```

#### Compiles and minifies for production
```
npm run build
```

#### Lints and fixes files
```
npm run lint
```

#### Running the project
```
Terminal 1: senior-capstone-embrailling$ npm run serve
Terminal 2: senior-capstone-embrailling/backend$ flask --app Flask.py run
```

#### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

## Users Guide

### Operating Instructions
- Open your preferred web browser.
- Navigate to the local host Terminal 1 is running on.
- Either enter the text to be translated into the text box on the left and click `TRANSLATE TEXT`, or click `TRANSLATE PDF` to select a PDF to be converted into braille.
- Start here if you already have a PDF in braille. On the right, click `CONVERT PDF TO DWG`. This will start the conversion process
- Notifications will be provided once the file has finished translating.
- Once finished, the DWG file will be downloaded locally.

### Tips for Conversion
- Ensure the PDF is clear and legible.
- Review the DWG file to ensure accurate braille translation.

### Troubleshooting
- If more clarification is needed click the help button as more information will be provided.
- If the website fails to load, check your internet connection, and attempt to load another website. If still not working look in `Terminal 1` to see if any errors are present.
- If the translation fails, wait a minute, then try again. If still not working look in `Terminal 2` to see if any errors are present.

