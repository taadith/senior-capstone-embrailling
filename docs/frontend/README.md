# senior-capstone-embrailling

Website to convert text or pdf to AutoCAD file, for use in TAMU laser cutter.

## First time setup
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

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Running the project
```
Terminal 1: senior-capstone-embrailling$ npm run serve
Terminal 2: senior-capstone-embrailling/backend$ flask --app Flask.py run
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
