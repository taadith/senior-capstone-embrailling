<template>
  <div class="braille-translator">
    <div class="input-section">
      <textarea v-model="inputText" placeholder="Enter text or upload a PDF" class="text-input"></textarea>
      <div class="textarea-button-container">
        <label class="textarea-button" for="file-upload">Upload PDF</label>
        <input id="file-upload" type="file" accept=".pdf" style="width: 0; height: 0;" @change="handleFileUpload" />
        <button class="textarea-button" id="#translate-button" @click="translateToBraille">Translate PDF</button>
        <button class="textarea-button" id="#translate-text" @click="translateTextboxToBraille">Translate Text</button>
      </div>
    </div>
      <div class="output-section">
        <textarea v-model="brailleOutput" readonly class="text-output"></textarea>
<!-- <button @click="downloadPDF">Download PDF</button> -->
        <input type="file" @change="handleFileChange" accept=".pdf" />
        <button @click="convertPdfToDwg">Convert PDF to DWG</button>
        <button @click="downloadDwg(jobId)">Download DWG File</button>
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
      selectedFile: null,
      selectedPdfFile: null,
      jobId: null,
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
        this.brailleOutput = response.data['translatedContent'];
      } catch (error) {
        console.error('Translation Error:', error);
      }
    },
    
    //downloadPDF() {
    // Fetch the file from the Flask endpoint
    //  window.location.href = '/api/download'; // Adjust this if your Flask app's URL structure is different
    //},


    async translateTextboxToBraille(){
      if(!(this.inputText.trim().length > 0)){
        alert('Please enter text first.')
        return;
      }

      const formData = new FormData();
      formData.append('text', this.inputText);
      console.log(this.inputText);

      this.inputText = '';

      try {
        const response = await axios.post('http://127.0.0.1:5000/translate_textbox_to_braille', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        console.log('Translation Success:', response.data);
        // Handle the response data as needed, such as displaying the translation
        console.log(response.data[1]['brailleUnicode']);
        this.brailleOutput = response.data[1]['brailleUnicode'];
      } catch (error) {
        console.error('Translation Error:', error);
      }

    },

    convertPdfToDwg() {
      console.log("Starting conversion process...");

      if (!this.selectedPdfFile) {
        alert("Please select a PDF file first.");
        return;
      }

      const formData = new FormData();
      formData.append('file', this.selectedPdfFile);

      
      console.log("Sending request to Flask...");
      fetch('http://127.0.0.1:5000/convert_to_dwg', { // Adjust this URL to match your Flask endpoint
        method: 'POST',
        body: formData,
      })
      .then(response => {
        console.log("Received response from Flask:", response); // Log response
        return response.json();
      })
      .then(data => {
        if (data.jobId) {
          console.log('Conversion started, job ID:', data.jobId);
          this.jobId = data.jobId;
        } else {
          console.error('Failed to start conversion:', data);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
    },

    handleFileChange(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.selectedPdfFile = files[0];
        console.log("File selected:", this.selectedPdfFile.name);
      } else {
        this.selectedPdfFile = null;
      }
    },

    // async startConversion() {
    //   try {
    //     const response = await fetch('http://127.0.0.1:5000/convert_to_dwg', { method: 'POST' });
    //     const data = await response.json();
    //     this.jobId = data.jobId; // Update jobId with the value received from the server
    //   } catch (error) {
    //     console.error('Error starting conversion:', error);
    //   }
    // },

    //setJobId(id) {
      //this.jobId = id;
      //console.log("Job ID set:", this.jobId);
    //},

    downloadDwg(jobId) {
      console.log("Attempting to download DWG file for Job ID:", jobId);
      if (!jobId) {
        alert("Job ID is required for downloading the DWG file.");
        return;
      }

      const url = `http://127.0.0.1:5000/download_dwg/${jobId}`;

      // Fetch the DWG file from the server
      fetch(url)
        .then(response => {
          if (!response.ok) {
            throw new Error(`Server returned ${response.status} when trying to download DWG file.`);
          }
          return response.blob();
        })
        .then(blob => {
          // Create a new link element and trigger the download
          const downloadUrl = window.URL.createObjectURL(blob);
          const link = document.createElement('a');
          link.href = downloadUrl;
          link.setAttribute('download', 'output.dwg');
          document.body.appendChild(link);
          link.click();
          link.parentNode.removeChild(link);
          window.URL.revokeObjectURL(downloadUrl);
        })
        .catch(error => {
          console.error('Download failed:', error);
        });
    }
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
  width: 45%;
}

.text-input,
.text-output,
.download-button {
  width: 100%;
  max-width: 600px;
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
  margin: 10px;
  padding: 10px;
  box-sizing: border-box;
}

.textarea-button-container {
  position: absolute;
  right: 55px;
  bottom: 20px;
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