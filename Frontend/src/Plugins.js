// ToastPlugin.js

import { createApp } from 'vue';
import { useCookies } from 'vue3-cookies'
import Toast from './components/ToastMessage.Vue';

const Plugins = {
  install(app) {
    const toastContainer = document.createElement('div');
    toastContainer.style.position = "relative";
    toastContainer.style.width = "100%"
    toastContainer.style.height = "100%"
    toastContainer.style.top = "0"
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
          return cookies.get("jwt")
        }
        else{
          return false
        }
      },
      async getUserData(){
        const {cookies} = useCookies()
        if(cookies.get("jwt")){
          const response = await fetch(`${import.meta.env.VITE_APP_BACKEND_URL}/users/verify?jwt=${cookies.get('jwt')}`)
          const data = await response.json()
          if(data.status == 200)
          {
            return data.user
          }
          else{
            return null
          }
        }
        else{
          return null
        }
      }
    }
  },
};

export default Plugins;
