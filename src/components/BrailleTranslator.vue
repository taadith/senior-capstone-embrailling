<template>
    <div class="braille-translator">
      <div class="input-section">
        <textarea v-model="inputText" placeholder="Enter text or upload a PDF" class="text-input"></textarea>
        <input type="file" @change="handleFileUpload" accept="application/pdf" class="file-input">
      </div>
      
        <div class="output-section">
            <textarea v-model="brailleOutput" readonly class="text-output"></textarea>
            <button @click="translateToBraille" class="download-button">Translate to Braille</button>
        </div>
    </div>
  </template>
  
  <script>
  // Import any necessary libraries or helpers for PDF extraction and Braille translation
  import axios from 'axios';

  export default {
    name: 'BrailleTranslator',
    data() {
      return {
        inputText: '',
        brailleOutput: ''
      };
    },
    methods: {
    //   handleFileUpload(event) {
    //     // ...existing code...
    //   },
    translateToBraille() {
      const apiUrl = 'https://api.funtranslations.com/translate/braille.json';
      const params = new URLSearchParams();
      params.append('text', this.inputText);
      
      axios.post(apiUrl, {
            params: {
                text: this.inputText
            },
            headers: {
                // 'X-Funtranslations-Api-Secret': '<Your_API_Key>'
            }
        })
        .then(response => {
            if (response.data.contents.translated.length > 0) {
                // Join the array elements into a single string
                this.brailleOutput = response.data.contents.translated.join("");
            } else {
                // Handle the case where the translated array is empty
                this.brailleOutput = 'No translation available.';
            }
        }) 
        .catch(error => {
          console.error('Error translating to Braille:', error);
          this.brailleOutput = 'Error translating to Braille. Please try again.';
        });
    },
    //   downloadBraille() {
    //     // ...existing code...
    //   }
    }
  };
  </script>
  
  <style scoped>
  .braille-translator {
    display: flex;
    align-items: center;
    justify-content: space-around;
    height: 100vh;
    padding-top: 50px;
    background-color: #121212;
    color: #ffffff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  }
  
  .input-section, .output-section {
    width: 45%;
  }

  .text-input,
  .text-output,
  .file-input,
  .download-button {
    width: 100%;
    max-width: 600px;
    margin: 10px;
    padding: 15px;
    border: none;
    border-radius: 5px;
  }
  
  .text-input,
  .text-output {
    width: 100%;
    height: 300px;
    margin-bottom: 15px; /* Space between text area and button */
    background-color: #1e1e1e;
    color: #ffffff;
    font-size: 16px;
    resize: none; /* Disables resize handle */
  }
  
  .file-input {
    background-color: #2a2a2a;
    color: #ffffff;
  }
  
  .download-button {
    background-color: #2979ff;
    color: #ffffff;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .download-button:hover {
    background-color: #5393ff;
  }
  </style>
  