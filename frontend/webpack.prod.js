const {merge} = require('webpack-merge');
const {appConf, landingConf, helpConf} = require('./webpack.common.js');

const prodConf = {
  mode: "production",
  devtool: "source-map",
  optimization: {
    minimize: true
  }
}

module.exports = [
  merge(appConf, prodConf),
  merge(landingConf, prodConf),
  merge(helpConf, prodConf)
];
