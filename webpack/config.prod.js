const webpack = require('webpack');
const Merge = require('webpack-merge');
const SentryWebpackPlugin = require('@sentry/webpack-plugin');

const CommonConfig = require('./config.common.js');

module.exports = Merge(CommonConfig, {
  mode: 'production',

  devtool: 'source-map',

  plugins: [
    new webpack.HashedModuleIdsPlugin(),
    new SentryWebpackPlugin({
      release: 'foobarbaz',
      include: 'static/build/',
    }),
  ],
});
