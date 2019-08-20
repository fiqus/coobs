import Vue from 'vue';
import Vuelidate from 'vuelidate';
import 'bootstrap/dist/css/bootstrap.min.css'

import app from './app.vue';
import router from './router'

import { library } from '@fortawesome/fontawesome-svg-core'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(far, fas)

Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.config.silent = true; // https://vuejs.org/v2/api/#silent

Vue.use(Vuelidate);

new Vue({
  router,
  render: createElement => createElement(app) // https://github.com/vuejs-templates/webpack-simple/issues/29#issuecomment-312902539
}).$mount("#app")
