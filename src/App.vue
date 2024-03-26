<template>
    <Authenticator :social-providers="['google']">
     <template v-slot="{ signOut }">
        <img id="logo" alt="Embraillers logo" src="./assets/logo_dome.png">
        <button @click="signOut" id="signout">Sign Out</button>
          <div id="app">
            <BrailleTranslator />
          </div>
     </template>
    </Authenticator>
</template>
<script>
import BrailleTranslator from './components/BrailleTranslator.vue';

import { Authenticator } from "@aws-amplify/ui-vue";
import "@aws-amplify/ui-vue/styles.css";

import { Amplify } from 'aws-amplify';
import config from './amplifyconfiguration.json';
Amplify.configure(config);

export default {
  name: 'App',
  components: {
    BrailleTranslator,
    Authenticator
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
  margin: 0 auto -200px; /* TODO: Figure out a better way to fix margins than using negative */
}


</style>
