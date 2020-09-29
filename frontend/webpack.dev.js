const merge = require('webpack-merge');
const {appConf, landingConf, helpConf} = require('./webpack.common.js');

const devConf = {
  mode: "development",
  devtool: "cheap-module-eval-source-map",
  devServer: {
    contentBase: './dist',
    hot: true,
    historyApiFallback: {
      rewrites: [
        { from: /^\/landing\/help/, to: '/landing/help.html' }
      ]
    },
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
  merge(landingConf, devConf),
  merge(helpConf, devConf)
];
