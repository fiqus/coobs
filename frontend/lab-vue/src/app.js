import Vue from 'vue';
import 'bootstrap/dist/css/bootstrap.min.css'

import app from './app.vue';
import router from './router'

Vue.config.silent = true; // https://vuejs.org/v2/api/#silent

new Vue({
  router,
  render: createElement => createElement(app) // https://github.com/vuejs-templates/webpack-simple/issues/29#issuecomment-312902539
}).$mount("#app")
