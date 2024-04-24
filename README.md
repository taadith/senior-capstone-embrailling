# TAMU Senior Capstone Project - Embrailling

Website to convert text or pdf to AutoCAD file, for use in TAMU laser cutter.

## Overview
Vue.js frontend application that makes calls to Python Flask API backend, backend uses pybrl for braille translation and Zamzar for file conversion

- [File Structure](https://github.com/taadith/senior-capstone-embrailling/edit/dev/README.md#file-structure)
- How to use
  - [Online](https://github.com/taadith/senior-capstone-embrailling/edit/dev/README.md#online)
  - [Local Setup](https://github.com/taadith/senior-capstone-embrailling/edit/dev/README.md#local-setup)

## File Structure
Code is split up into two main sections, Vue.js front end, and Flask API backend. 

  - Frontend: All the frontend componenets are under the `src` folder. This includes the main `App.vue` file and the main `BrailleTranslator.vue` componenet.
      - [Documentation](https://github.com/taadith/senior-capstone-embrailling/blob/dev/docs/frontend/README.md)
  - Backend: All the backend componenets are under the `backend` folder. This includes the two main files used in the API for translation and conversion, `Flask.py` and `Translate.py`. It also includes the entire [pybrl](https://github.com/ant0nisk/pybrl) library which is used for translation. 
    - [Documentation](https://github.com/taadith/senior-capstone-embrailling/tree/dev/docs/backend)

## How to use

### Online

### Local Setup

#### First time setup
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

#### Project setup
```
npm install
```

##### Compiles and hot-reloads for development
```
npm run serve
```

##### Compiles and minifies for production
```
npm run build
```

##### Lints and fixes files
```
npm run lint
```

##### Running the project
```
Terminal 1: senior-capstone-embrailling$ npm run serve
Terminal 2: senior-capstone-embrailling/backend$ flask --app Flask.py run
```

##### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).
