import router from "./router";
import store from './store';
import Vue from 'vue';
import browserLocale from 'browser-locale';

const { scheme, hostname } =
  process.env.NODE_ENV === "production"
    ? { scheme: "https"
      , hostname: window.location.hostname }
    : { scheme: "http"
      , hostname: "localhost:"+window.location.port };

const apiURL = `${scheme}://${hostname}/api`;

const axios = require("axios").create({baseURL: apiURL, timeout: 0, headers: {}});

axios.interceptors.response.use((response) => response,
  (err) =>{
    const originalRequest = err.config;
    if (err.response.status === 401 && originalRequest.url.indexOf("/api/token/refresh/") !== -1) {
      router.push("/login");
      return Promise.reject(err);
    }
    if (err.response.status === 401 && err.response.data.code === "token_not_valid" && !originalRequest._retry) {
      originalRequest._retry = true;
      return axios.post("/token/refresh/", {refresh: store.state.user.refresh})
        .then((res) => {
          const {access} = res.data;
          const tokenData = Vue.$jwt.decode(access);
          store.commit("setUser", {...tokenData.user, access});
          // update auth header for original request
          originalRequest.headers["Authorization"] = `Bearer ${access}`;
          return axios(originalRequest);
        })
        .catch((errRefresh) => {
          router.push("/login");
          return Promise.reject(errRefresh);
        });
    }
    if (err.response.status >= 405) {
      const newErr = { response: { data: { detail: "backendServicesError" } } };
      return Promise.reject(newErr);
    }
    return Promise.reject(err);
  }
);

function _buildHeaders(defaultHeaders = {}) {
  const user = store && store.state ? store.state.user : null;
  const storeLocale = store && store.state && store.state.i18n ? store.state.i18n.locale : '';
  const currentLocale = browserLocale().split("-")[0];
  const locale = storeLocale || currentLocale;

  Object.assign(defaultHeaders, {"Accept-Language": locale || 'en'})

  if (user && user.access) {
    return Object.assign({}, defaultHeaders, {
      "Authorization": `Bearer ${user.access}`
    });
  }

  return defaultHeaders;
}

/* HTTP METHODS */

export function httpGet(url, params = {}) {
  return axios.get(url, {headers: _buildHeaders(), params});
}

export function httpPost(url, data) {
  return axios.post(url, data, {headers: _buildHeaders()});
}

export function httpPut(url, data) {
  return axios.put(url, data, {headers: _buildHeaders()});
}

export function httpPatch(url, data) {
  return axios.patch(url, data, {headers: _buildHeaders()});
}

export function httpDelete(url) {
  return axios.delete(url, {headers: _buildHeaders()});
}

/* END HTTP METHODS */
