import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Plugins from './Plugins'

const app = createApp(App)

app.use(Plugins)

app.use(router)

app.mount('#app')
