import { createApp } from 'vue'
import App from './App.vue'
import './assets/global.css';

import { Amplify } from 'aws-amplify';
import config from './amplifyconfiguration.json';
Amplify.configure(config);

createApp(App).mount('#app')
