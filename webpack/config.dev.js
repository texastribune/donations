const Merge = require('webpack-merge');
const CleanWebpackPlugin = require('clean-webpack-plugin');

const CommonConfig = require('./config.common.js');
const { buildDir } = require('./base');

module.exports = Merge(CommonConfig, {
  mode: 'development',

  output: {
    publicPath: '/static/build/',
  },

  watch: true,

  cache: false,

  plugins: [
    new CleanWebpackPlugin([buildDir], {
      root: process.cwd(),
      verbose: false,
    }),
  ],
});
