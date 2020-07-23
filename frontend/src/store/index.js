import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

import {state} from "./state";
import {mutations} from "./mutations";
import {actions} from "./actions";
import {getters} from "./getters";
import CKEditor from '@ckeditor/ckeditor5-vue';

Vue.use(Vuex);
Vue.use(CKEditor);

const debug = process.env.NODE_ENV !== "production";

export default new Vuex.Store({
  state,
  actions,
  mutations,
  getters,
  strict: debug,
  plugins: [createPersistedState()]
});