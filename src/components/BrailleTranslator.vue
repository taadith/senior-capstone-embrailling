<template>
  <div class="braille-translator">
    <div class="input-section">
      <textarea v-model="inputText" placeholder="Enter text or upload a PDF" class="text-input"></textarea>
      <div class="textarea-button-container">
        <label class="textarea-button" for="file-upload">Translate PDF</label>
        <input id="file-upload" type="file" accept=".pdf" style="width: 0; height: 0;" @change="handleFileUpload" />
        <button class="textarea-button" id="#translate-text" @click="translateTextboxToBraille">Translate Text</button>
      </div>
    </div>
      <div class="output-section">
        <textarea id="braille-output" v-model="brailleOutput" readonly class="text-output" aria-label="Braille Output"></textarea>
        <!-- <input type="file" @change="handleFileChange" accept=".pdf" /> -->
        <div class="textarea-button-container">
          <label class="textarea-button" for="file-dwg">Convert PDF to DWG</label>
          <input id="file-dwg" type="file" accept=".pdf" style="width: 0; height: 0;" @change="handleFileChange" />
          <button class="textarea-button" @click="downloadDwg(jobId)">Download DWG</button>
        </div>
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
      this.translateToBraille();
    },
  
    async translateToBraille() {
      if (!this.selectedFile) {
        this.$notify({type: "error", text: "Please select a file first!"});
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
        this.$notify({type: "success", text: "Translation complete!"});
        // Handle the response data as needed, such as displaying the translation
        this.brailleOutput = response.data['translatedContent'];
        this.downloadPDF();
      } catch (error) {
        console.error('Translation Error:', error);
        this.$notify({type: "error", text: "Translation error."});
      }
    },
    
    downloadPDF() {
      const url = 'http://127.0.0.1:5000/download_pdf'; // Update with your Flask server URL
      axios.get(url, {
        responseType: 'blob', // Set the response type to blob to handle binary data
      })
      .then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'download-success.pdf'); // Specify the file name
        document.body.appendChild(link);
        link.click();
      })
      .catch(error => {
        console.error('Error downloading PDF:', error);
        this.$notify({type: "error", text: "Error downloading PDF."});
      });
    },

    async translateTextboxToBraille(){
      if(!(this.inputText.trim().length > 0)){
        this.$notify({type: "error", text: "Please enter text first!"});
        return;
      }

      this.$notify({type: "alert", text: "Translating text to braille..."});

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
        this.$notify({type: "success", text: "Translation complete!"});
        // Handle the response data as needed, such as displaying the translation
        console.log(response.data[1]['brailleUnicode']);
        this.brailleOutput = response.data[1]['brailleUnicode'];
        this.downloadPDF();
      } catch (error) {
        console.error('Translation Error:', error);
        this.$notify({type: "error", text: "Translation error."});
      }

    },

    convertPdfToDwg() {
      console.log("Starting conversion process...");

      if (!this.selectedPdfFile) {
        this.$notify({type: "error", text: "Please select a PDF first!"});
        return;
      }

      this.$notify({type: "alert", text: "Starting conversion..."});

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
          this.downloadDwg(this.jobId);
        } else {
          console.error('Failed to start conversion:', data);
          this.$notify({type: "error", text: "Conversion failed."});
        }
      })
      .catch(error => {
        console.error('Error:', error);
        this.$notify({type: "error", text: "Conversion error."});
      });
    },

    handleFileChange(event) {
      const files = event.target.files;
      if (files.length > 0) {
        this.selectedPdfFile = files[0];
        console.log("File selected:", this.selectedPdfFile.name);
        this.convertPdfToDwg();
      } else {
        this.selectedPdfFile = null;
      }
    },

    downloadDwg(jobId) {
      console.log("Attempting to download DWG file for Job ID:", jobId);
      if (!jobId) {
        this.$notify({type: "error", text: "Create a DWG first!"});
        return;
      }

      const url = `http://127.0.0.1:5000/download_dwg/${jobId}`;

      this.polling = setInterval(() => {
        fetch(url)
          .then(response => {
            if (!response.ok) {
              this.$notify({type: "warn", text: "DWG isn't finished converting!"});
              return;
            }
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
            this.$notify({type: "success", text: "DWG downloaded!"});
            clearInterval(this.polling);
          })
          .catch(error => {
            console.error('Download failed:', error);
            clearInterval(this.polling);
          });
        }, 3000)
    },

    pollAPI() {
      return;
    },

    beforeDestroy() {
      clearInterval(this.polling);
    },
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
.text-output {
  height: 80%;
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
  margin-top: auto;
}


#translate-button{
border-bottom-right-radius: 10px;
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