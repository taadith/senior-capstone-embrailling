# Frontend Documentation
Application uses Vue.js for the frontend. The front end handles the calls and receives the responses from the backend Flask API.

All the frontend componenets are contained within the `src` folder. 

## File Structure
- [App.vue](https://github.com/taadith/senior-capstone-embrailling/blob/dev/src/App.vue): Application that houses the main componentent, also holds the help menu. 
- [components/BrailleTranslator.vue](https://github.com/taadith/senior-capstone-embrailling/blob/dev/src/components/BrailleTranslator.vue): This is the main application component. Each button present makes calls to the Flask API that we have implemented

## Code Documentation
### App.vue
- [toggleHelpPopup()](https://github.com/taadith/senior-capstone-embrailling/blob/611ebc0c0c4d8f1519335a57e6f8dfabda8673bc/src/App.vue#L45): Changes the showHelp var to display or hide the help pop up.

### BrailleTranslator.vue
- [handleFileUpload(event)](https://github.com/taadith/senior-capstone-embrailling/blob/611ebc0c0c4d8f1519335a57e6f8dfabda8673bc/src/components/BrailleTranslator.vue#L63): Sets selected file to one user has uploaded
    
    Args:
    - {any}: event
 
- [translateToBraille()](https://github.com/taadith/senior-capstone-embrailling/blob/611ebc0c0c4d8f1519335a57e6f8dfabda8673bc/src/components/BrailleTranslator.vue#L73): Takes the selected pdf file from the user and calls the translate_to_braille endpoint. The file is passed to the Flask API as the form data. The braille unicode response is then displayed inside of the braille output textfield.

- [downloadPDF()](https://github.com/taadith/senior-capstone-embrailling/blob/611ebc0c0c4d8f1519335a57e6f8dfabda8673bc/src/components/BrailleTranslator.vue#L99): Calls the Flask API endpoint to intiate the local download of the translated pdf file. The API responds back with the translated file. After the response the file is downloaded locally under the name 'download-success.pdf' to the users downloads directory.

- [translateTexboxToBraille](https://github.com/taadith/senior-capstone-embrailling/blob/611ebc0c0c4d8f1519335a57e6f8dfabda8673bc/src/components/BrailleTranslator.vue#L127): Takes the text inputted from the user and calls the translate_textbox_to_braille endpoint. The text is passed to the Flask API as the form data. The braille unicode response is then displayed inside of the braille output textfield.

- [convertPdfToDwg()](https://github.com/taadith/senior-capstone-embrailling/blob/611ebc0c0c4d8f1519335a57e6f8dfabda8673bc/src/components/BrailleTranslator.vue#L165): User uploads a pdf file that is then converted to dwg. This method calls the convert_to_dwg endpoint in the Flask API. The uploaded pdf is sent as the form data.

- [handleFileChange(event)](https://github.com/taadith/senior-capstone-embrailling/blob/611ebc0c0c4d8f1519335a57e6f8dfabda8673bc/src/components/BrailleTranslator.vue#L209): After user uploades a pdf file, the convertPdfToDwg method is called to initiate the file conversion.
   
    Args:
    - {any}: event

 - [downloadDwg](https://github.com/taadith/senior-capstone-embrailling/blob/611ebc0c0c4d8f1519335a57e6f8dfabda8673bc/src/components/BrailleTranslator.vue#L226): Using the jobId for the Zamzar conversion calls the download_dwg endpoint on the FlaskAPI. Constantly fetches and sees if the conversion has finished and displays appropriate notifications.

    Args:
    - {any} jobId - jobId for Zamzar file conversion
  
