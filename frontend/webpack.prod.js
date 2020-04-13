const merge = require('webpack-merge');
const {appConf, landingConf} = require('./webpack.common.js');

const prodConf = {
  mode: "production",
  devtool: "source-map"
}

module.exports = [
  merge(appConf, prodConf),
  merge(landingConf, prodConf)
];
