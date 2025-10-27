const {merge} = require('webpack-merge');
const {appConf, landingConf, helpConf} = require('./webpack.common.js');

const devConf = {
  mode: "development",
  devtool: "eval-cheap-module-source-map",
  optimization: {
    minimize: false
  }
};

const devServer = {
  contentBase: './dist',
  compress: true,
  port: 8080,
  host: '0.0.0.0',
  hot: true,
  watchOptions: {
    poll: true
  },
  clientLogLevel: "error", // https://webpack.js.org/configuration/dev-server/#devserverclientloglevel
  historyApiFallback: {
    rewrites: [
      { from: /^\/app/, to: '/app/index.html' },
      { from: /^\/landing/, to: '/landing/index.html' },
      { from: /^\/help/, to: '/help/index.html' }
    ]
  },
  proxy: {
    "/api": {
      target: "http://backend:8000",
      ws: true,
      changeOrigin: true,
      timeout: 60000,
      proxyTimeout: 60000
    }
  }
};

module.exports = [
  merge(appConf, devConf, {devServer}),
  merge(landingConf, devConf),
  merge(helpConf, devConf)
];
