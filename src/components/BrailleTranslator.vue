<template>
    <div class="braille-translator">
      <div class="input-section">
        <textarea v-model="inputText" placeholder="Enter text or upload a PDF" class="text-input"></textarea>
        <input type="file" @change="handleFileUpload" />
        <button @click="translateToBraille">Translate to Braille</button>
        <div class="file-input">
          <FileUpload/>
        </div>
      </div>
        <div class="output-section">
            <textarea v-model="brailleOutput" readonly class="text-output"></textarea>
            <!-- <button @click="translateToBraille" class="download-button">Translate to Braille</button> -->
        </div>
    </div>
  </template>
  
  <script>
  
  // Import any necessary libraries or helpers for PDF extraction and Braille translation
  import axios from 'axios';
  import FileUpload from './FileUpload.vue';

  export default {
    name: 'BrailleTranslator',
    data() {
      return {
        inputText: '',
        brailleOutput: '',
        selectedFile: null
      };
    },

    components: {
      FileUpload
    },

    methods: {
      handleFileUpload(event) {
        this.selectedFile = event.target.files[0];
      },
    
      async translateToBraille() {
        if (!this.selectedFile) {
          alert('Please select a file first.');
          return;
        }

        const formData = new FormData();
        formData.append('file', this.selectedFile);

        try {
          const response = await axios.post('http://127.0.0.1:5000/translate_to_braille', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          console.log('Translation Success:', response.data);
          // Handle the response data as needed, such as displaying the translation
        } catch (error) {
          console.error('Translation Error:', error);
        }
      },
      
      //downloadBraille() {
        
     // }
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
  