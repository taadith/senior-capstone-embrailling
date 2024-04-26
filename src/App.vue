<template>
    <img id="logo" alt="Embraillers logo" src="./assets/logo_dome.png" aria-hidden="true">
      <div id="app">
        <BrailleTranslator />
      </div>
  <notifications position="top left" width=30% max=4 classes="notif" />
</template>

<script>
import BrailleTranslator from './components/BrailleTranslator.vue';

export default {
  name: 'App',
  components: {
    BrailleTranslator,
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

</style>
