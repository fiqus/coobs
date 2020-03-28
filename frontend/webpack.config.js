'use strict'

const webpack = require('webpack');
const { VueLoaderPlugin } = require('vue-loader');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const path = require("path");

module.exports = {
  mode: 'development',
  entry: {
    app: './src/app.js',
    landing: './landing/app.js'
  },
  output: {
    filename: "[name].bundle.js",
    path: path.join(__dirname, "./dist"),
  },
  // cheap-module-eval-source-map is faster for development
  devtool: "#cheap-module-eval-source-map",
  //devtool: "inline-source-map",
  // watch: true,
  devServer: {
    hot: true,
    watchOptions: {
      poll: true
    },
    clientLogLevel: 'error', // https://webpack.js.org/configuration/dev-server/#devserverclientloglevel
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        ws: true,
        changeOrigin: true
      }
    }
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        use: 'vue-loader'
      },
      {
        test: /\.(scss|css)$/,
        use: [
          'vue-style-loader',
          'css-loader',
        ]
      },
      {
        test: /\.(jpe?g|png|gif|woff|woff2|eot|ttf|svg)(\?[a-z0-9=.]+)?$/,
        use: [
          'file-loader'
        ]
      }
    ]
  },
  resolve: {
    alias: {
      'jquery': path.join(__dirname, './assets/js/jquery.min.js')
    }
  },
  externals: {
    'jQuery': 'jquery'
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    }), 
    new webpack.HotModuleReplacementPlugin(),
    new VueLoaderPlugin(),
    new CopyWebpackPlugin([{ from: 'static/', to: './' }]),
    new HtmlWebpackPlugin({
      template: 'index.html',
      chunks: ["app"],
      path: path.join(__dirname, "./dist/app"),
      filename: 'index.html',
      inject: true
    }),
    new HtmlWebpackPlugin({
      template: 'landing/index.html',
      chunks: ["landing"],
      path: path.join(__dirname, "./dist/landing"),
      filename: 'index.html',
      inject: true
    })
  ]
}
