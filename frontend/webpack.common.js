const webpack = require("webpack");
const { VueLoaderPlugin } = require("vue-loader");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const path = require("path");
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const baseConf = {
  module: {
    rules: [
      {
        test: /\.vue$/,
        use: "vue-loader"
      },
      {
        test: /\.(scss|css)$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
            options: {}
          },
          "css-loader"
        ]
      },
      {
        test: /\.(jpe?g|png|gif|woff|woff2|eot|ttf|svg)(\?[a-z0-9=.]+)?$/,
        use: [
          "file-loader"
        ]
      }
    ]
  },
  resolve: {
    alias: {
      "jquery": path.join(__dirname, "./assets/js/jquery.min.js")
    }
  },
  externals: {
    "jQuery": "jquery"
  }
}

const appConf = Object.assign({}, baseConf, {
  name: "app",
  entry: "./src/app.js",
  output: {
    path: path.join(__dirname, "./dist/app"),
    filename: "app.bundle.js"
  },
  plugins: [
    new webpack.DefinePlugin({process: {env: {'NODE_ENV': JSON.stringify(process.env.NODE_ENV)}}}), // Ugly fix for `"production" !== production`
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[id].css',
      ignoreOrder: false,
    }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    }),
    new VueLoaderPlugin(),
    new CopyWebpackPlugin({patterns: [{
      context: path.resolve(__dirname, 'static'),
      from: "**/*",
      to: "./"
    }]}),
    new HtmlWebpackPlugin({
      template: "index.html",
      path: path.join(__dirname, "./dist/app"),
      filename: "index.html",
      inject: true
    })
  ]
});

const landingConf = Object.assign({}, baseConf, {
  name: "landing",
  entry: "./landing/app.js",
  output: {
    path: path.join(__dirname, "./dist/landing"),
    filename: "landing.bundle.js"
  },
  plugins: [
    new webpack.DefinePlugin({process: {env: {'NODE_ENV': JSON.stringify(process.env.NODE_ENV)}}}), // Ugly fix for `"production" !== production`
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[id].css',
      ignoreOrder: false,
    }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    }),
    new CopyWebpackPlugin({patterns: [{
      from: "**/*",
      context: path.resolve(__dirname, 'static'),
      to: "./"
    }]}),
    new HtmlWebpackPlugin({
      template: "landing/index.html",
      path: path.join(__dirname, "./dist/landing"),
      filename: "index.html",
      inject: true
    })
  ]
});

const helpConf = Object.assign({}, baseConf, {
  name: "help",
  entry: "./help/app.js",
  output: {
    path: path.join(__dirname, "./dist/help"),
    filename: "help.bundle.js"
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].css',
      chunkFilename: '[id].css',
      ignoreOrder: false
    }),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery"
    }),
    new CopyWebpackPlugin({patterns: [{
      context: path.resolve(__dirname, 'help', 'images'),
      from: "**/*",
      to: "./images/screens"
    }]}),
    new CopyWebpackPlugin({patterns: [{
      context: path.resolve(__dirname, 'static', 'images'),
      from: "**/*",
      to: "./images"
    }]}),
    new HtmlWebpackPlugin({
      template: "help/index.html",
      path: path.join(__dirname, "./dist/help"),
      filename: "index.html",
      inject: true
    }),
    new HtmlWebpackPlugin({
      template: "help/es.html",
      path: path.join(__dirname, "./dist/help"),
      filename: "es.html",
      inject: false
    }),
    new HtmlWebpackPlugin({
      template: "help/en.html",
      path: path.join(__dirname, "./dist/help"),
      filename: "en.html",
      inject: false
    })
  ]
});

module.exports = {
  appConf, landingConf , helpConf
};
