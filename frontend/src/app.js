import Vue from 'vue';
import Vuelidate from 'vuelidate';

import app from './app.vue';
import router from './router'
import {i18n} from './i18n';

import NavbarLayout from './layouts/navbar-layout.vue';
import EmptyLayout from './layouts/empty-layout.vue';
import LoginLayout from './layouts/login-layout.vue';

Vue.config.silent = true; // https://vuejs.org/v2/api/#silent

Vue.component('navbar-layout', NavbarLayout);
Vue.component('empty-layout', EmptyLayout);
Vue.component('login-layout', LoginLayout);

Vue.use(Vuelidate);

new Vue({
  router,
  i18n,
  render: createElement => createElement(app) // https://github.com/vuejs-templates/webpack-simple/issues/29#issuecomment-312902539
}).$mount("#app")
