const { scheme, hostname } =
  process.env.NODE_ENV === 'production'
  ? { scheme: 'https'
    , hostname: window.location.hostname }
  : { scheme: 'http'
    , hostname: 'localhost:8080' };

const apiURL = `${scheme}://${hostname}/api`;

const axios = require("axios").create({baseURL: apiURL, timeout: 0, headers: {}});

function _buildHeaders() {
  // const token = store ? store.getters.getToken : null;

  // if (token) {
  //   return Object.assign({}, defaultHeaders, {
  //     "Authorization": `Bearer ${token}`
  //   });
  // }

  // return defaultHeaders;
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

export function httpDelete(url) {
  return axios.delete(url, {headers: _buildHeaders()});
}

/* END HTTP METHODS */
