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
      const brailleMap = {
        'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 
        'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚', 
        'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 
        'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 
        'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 
        'z': '⠵', 
        ' ': '⠂', // Space
        '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙', '5': '⠼⠑', 
        '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊', '0': '⠼⠚',
        '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', '\'': '⠄', 
        '-': '⠤', '/': '⠌', ':': '⠒', ';': '⠆', '(': '⠷', 
        ')': '⠾', '"': '⠶', '&': '⠯', '@': '⠈', '#': '⠼⠼',
      };

      this.brailleOutput = this.inputText.split('').map(char => {
        const lowerChar = char.toLowerCase();
        return brailleMap[lowerChar] || char; // Keep the character as is if no Braille mapping exists
      }).join('');
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
  