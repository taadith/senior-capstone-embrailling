  <template>
      <div class="braille-translator">
        <div class="input-section">
          <textarea v-model="inputText" placeholder="Enter text or upload a PDF" class="text-input"></textarea>
          <div class="textarea-button-container">
            <label class="textarea-button" for="file-upload">Upload PDF</label>
            <input id="file-upload" type="file" accept=".pdf" style="width: 0; height: 0;" @change="handleFileUpload" />
            <button class="textarea-button" id="#translate-button" @click="translateToBraille">Translate</button>
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
    position: relative;
    margin: 20px;
    width: 45%;
  }

  .text-input,
  .text-output,
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

  textarea {
    width: calc(100% - 40px);
    height: 150px;
    margin: 20px;
    padding: 10px;
    box-sizing: border-box;
  }

  .textarea-button-container {
    position: absolute;
    right: 55px;
    bottom: 20px;
  }

  .textarea-button {
    transition: all .5s ease;
    color: lightgrey;
    border: solid darkgrey;
    border-radius: 4px;
    border-width: 2px;
    font-family:'Montserrat', sans-serif;
    text-transform: uppercase;
    text-align: center;
    line-height: 1;
    font-size: 14px;
    padding: 10px;
    margin: 5px;
    outline: none;
  }

.textarea-button:hover {
    color: #000;
    background-color: darkgrey;
}

#translate-button{
  border-bottom-right-radius: 10px;
}

  input[type="file"] {
    display: none;
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
  