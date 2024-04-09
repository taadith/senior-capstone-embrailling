import { createApp } from 'vue'
import App from './App.vue'
import './assets/global.css';
import Notifications from '@kyvg/vue3-notification'

import { Amplify } from 'aws-amplify';
import config from './amplifyconfiguration.json';
Amplify.configure(config);

const app = createApp(App);
app.use(Notifications);
app.mount('#app');
