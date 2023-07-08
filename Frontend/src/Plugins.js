// ToastPlugin.js

import { createApp } from 'vue';
import { useCookies } from 'vue3-cookies'
import Toast from './components/ToastMessage.Vue';

const Plugins = {
  install(app) {
    const toastContainer = document.createElement('div');
    toastContainer.style.position = "absolute"
    toastContainer.style.width = "100%"
    toastContainer.style.height = "100%"
    toastContainer.style.top = "0"
    toastContainer.style.zIndex = "-3"
    document.body.appendChild(toastContainer);

    const appInstance = createApp(Toast);
    const toastInstance = appInstance.mount(toastContainer);

    app.config.globalProperties.$toast = {
      show(status, message) {
        toastInstance.status = status;
        toastInstance.message = message;
        toastInstance.show();
      },
    };

    app.config.globalProperties.$login = {
      verify() {
        const {cookies} = useCookies()
        if(cookies.get("jwt")){
          return true
        }
        else{
          return false
        }
      }
    }
  },
};

export default Plugins;
