import { createApp } from 'vue'
import App from './App.vue'
import './assets/global.css';
import ToastPlugin from 'vue-toast-notification';
import 'vue-toast-notification/dist/theme-bootstrap.css';

import { Amplify } from 'aws-amplify';
import config from './amplifyconfiguration.json';
Amplify.configure(config);

const app = createApp(App);
app.use(ToastPlugin, {
    // One of the options
    position: 'top'
});
app.mount('#app');
