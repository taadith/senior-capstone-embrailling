<template>
  <button class="help-button" @click="toggleHelpPopup">Help</button>
    <div v-if="showHelp" class="help-popup blur-transition">
        <button class="close-button" @click="toggleHelpPopup">X</button>
        <h2 class="help-heading">How to Use The Embrailler</h2>
        <p class="help-paragraph">
          <span class="help-item">Translate PDF</span>: Select a PDF file to upload and then translate it to Braille.<br/><br/>
          <span class="help-item">Translate Text</span>: Translate the text in the input box to Braille.<br/><br/>
          <span class="help-item">Convert PDF to DWG</span>: Select a PDF file to upload and then convert it to DWG format.<br/><br/>
          <span class="help-item">Download DWG</span>: Download the converted DWG file.<br/>
        </p>
        <!-- More detailed instructions here -->
    </div>
  <div :class="{'blur': showHelp}" id="app">
    <img id="logo" alt="Embraillers logo" src="./assets/logo_dome.png" aria-hidden="true">
      <div id="app">
        <BrailleTranslator />
      </div>
    <notifications position="top left" width=30% max=4 classes="notif" />
  </div>
</template>

<script>
import BrailleTranslator from './components/BrailleTranslator.vue';

export default {
  name: 'App',
  components: {
    BrailleTranslator,
  },
  data() {
    return {
      showHelp: false,
    };
  },
  methods: {
    toggleHelpPopup() {
      this.showHelp = !this.showHelp;
    }, 
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

#logo {
  display: block; 
  max-width: 200px; 
  margin: 0 auto -200px; /* TODO: Figure out a better way to fix margins than using negative values */
}

#signout {
  position: absolute;
  top: 20px;
  right: 80px;
  cursor: pointer;
}

.blur {
  filter: blur(3px);
}

.blur-transition {
  transition: filter 0.3s ease;
}

.help-button {
  position: fixed;
  z-index: 1000;
  top: 20px;
  right: 20px;
}

.help-heading {
  margin-top: 10px;
}

.help-popup {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #1e1e1e;
  color: lightgrey;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  width: 500px;
  z-index: 1000;
}

.help-paragraph {
  text-align: left;
}

.help-item {
  font-weight: bold;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  border: none;
  background: transparent;
  color: white;
  cursor: pointer;
}
</style>
