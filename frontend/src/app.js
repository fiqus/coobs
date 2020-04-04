import Vue from "vue";
import Vuelidate from "vuelidate";
import vuexI18n from "vuex-i18n";
import browserLocale from "browser-locale";
import VueJWT from "vuejs-jwt";

import app from "./app.vue";
import router from "./router";
import {loadLocalMessage} from "./i18n";
import store from "./store";

import NavbarLayout from "./layouts/navbar-layout.vue";
import EmptyLayout from "./layouts/empty-layout.vue";
import LoginLayout from "./layouts/login-layout.vue";

import {formatToUIDate} from './utils';

import "../node_modules/@fortawesome/fontawesome-free/css/all.css"
import "../assets/css/fonts.css"
import "../assets/css/custom.css"
import "../assets/css/sb-admin-2.min.css"
import "jquery"
import "../assets/js/bootstrap.bundle.min.js"
import "../assets/js/jquery.easing.min.js"
import "../assets/js/sb-admin-2.min.js"

Vue.config.silent = true; // https://vuejs.org/v2/api/#silent

Vue.filter("formatToUIDate", formatToUIDate);

Vue.component("navbar-layout", NavbarLayout);
Vue.component("empty-layout", EmptyLayout);
Vue.component("login-layout", LoginLayout);

Vue.use(Vuelidate);
Vue.use(VueJWT);

Vue.use(vuexI18n.plugin, store);
Vue.i18n.add("en", loadLocalMessage("en"));
Vue.i18n.add("es", loadLocalMessage("es"));
const vuexStorage = localStorage.getItem("vuex");
const storage = vuexStorage ? JSON.parse(vuexStorage) : null;
const locale = storage && storage.i18n && storage.i18n.locale ? storage.i18n.locale : browserLocale().split("-")[0];
Vue.i18n.set(locale || "en");

new Vue({
  router,
  store,
  render: createElement => createElement(app) // https://github.com/vuejs-templates/webpack-simple/issues/29#issuecomment-312902539
}).$mount("#app");
