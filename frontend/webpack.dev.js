const merge = require('webpack-merge');
const {appConf, landingConf} = require('./webpack.common.js');

const devConf = {
  mode: "development",
  devtool: "cheap-module-eval-source-map",
  devServer: {
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
  }
}

module.exports = [
  merge(appConf, devConf),
  merge(landingConf, devConf)
];