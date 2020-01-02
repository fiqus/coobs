import Vue from 'vue';
import Vuelidate from 'vuelidate';
import vuexI18n from 'vuex-i18n';
import browserLocale from 'browser-locale';
import VueJWT from 'vuejs-jwt'

import app from './app.vue';
import router from './router'
import {loadLocalMessage} from './i18n';
import store from './store';

import NavbarLayout from './layouts/navbar-layout.vue';
import EmptyLayout from './layouts/empty-layout.vue';
import LoginLayout from './layouts/login-layout.vue';

Vue.config.silent = true; // https://vuejs.org/v2/api/#silent

Vue.component('navbar-layout', NavbarLayout);
Vue.component('empty-layout', EmptyLayout);
Vue.component('login-layout', LoginLayout);

Vue.use(Vuelidate);
Vue.use(VueJWT);

Vue.use(vuexI18n.plugin, store);
Vue.i18n.add('en', loadLocalMessage("en"));
Vue.i18n.add('es', loadLocalMessage("es"));
const vuexStorage = localStorage.getItem("vuex");
const storage = vuexStorage ? JSON.parse(vuexStorage) : null;
const locale = storage ? storage.lang : browserLocale().split("-")[0];
Vue.i18n.set(locale || 'en');

new Vue({
  router,
  store,
  render: createElement => createElement(app) // https://github.com/vuejs-templates/webpack-simple/issues/29#issuecomment-312902539
}).$mount("#app")
