<template>
  <img id="logo" alt="Embraillers logo" src="./assets/logo.png">
  <div id="app">
    <BrailleTranslator />
  </div>
</template>

<script>
import BrailleTranslator from './components/BrailleTranslator.vue';

export default {
  name: 'App',
  components: {
    BrailleTranslator
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

</style>
