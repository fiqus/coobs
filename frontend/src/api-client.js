import router from './router'

const { scheme, hostname } =
  process.env.NODE_ENV === 'production'
  ? { scheme: 'https'
    , hostname: window.location.hostname }
  : { scheme: 'http'
    , hostname: 'localhost:8080' };

const apiURL = `${scheme}://${hostname}/api`;

const axios = require("axios").create({baseURL: apiURL, timeout: 0, headers: {}});

axios.interceptors.response.use((response) => response,
  (err) =>{
    const originalRequest = err.config;
    if (err.response.status === 401 && originalRequest.url.indexOf("/api/refresh/") !== -1) {
      router.push('/login');
      return Promise.reject(err);
    }
    if (err.response.status === 401 && err.response.data.code === "token_not_valid" && !originalRequest._retry) {
      originalRequest._retry = true;
      return axios.post("/refresh/", {refresh: localStorage.getItem("user-token-refresh")})
        .then((res) => {
          localStorage.setItem("user-token", res.data.access);
          // update auth header for original request
          originalRequest.headers['Authorization'] = 'Bearer ' + localStorage.getItem("user-token");
          return axios(originalRequest);
        })
        .catch((errRefresh) => {
          return Promise.reject(errRefresh);
        })
    }
    return Promise.reject(err);
  }
);

function _buildHeaders(defaultHeaders = {}) {
  const token = localStorage.getItem("user-token");

  if (token) {
    return Object.assign({}, defaultHeaders, {
      "Authorization": `Bearer ${token}`
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

export function httpDelete(url) {
  return axios.delete(url, {headers: _buildHeaders()});
}

/* END HTTP METHODS */
