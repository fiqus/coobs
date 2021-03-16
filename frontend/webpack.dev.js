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
  hot: true,
  watchOptions: {
    poll: true
  },
  clientLogLevel: "error", // https://webpack.js.org/configuration/dev-server/#devserverclientloglevel
  proxy: {
    "/api": {
      target: "http://localhost:8000",
      ws: true,
      changeOrigin: true
    }
  }
};

module.exports = [
  merge(appConf, devConf, {devServer}),
  merge(landingConf, devConf),
  merge(helpConf, devConf)
];
