const webpack = require('webpack');
const Merge = require('webpack-merge');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');

const CommonConfig = require('./config.common.js');

module.exports = Merge(CommonConfig, {
  mode: 'production',

  plugins: [
    new webpack.HashedModuleIdsPlugin(),
    new OptimizeCSSAssetsPlugin({}),
  ],
});
