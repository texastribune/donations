const Merge = require('webpack-merge');
const CleanWebpackPlugin = require('clean-webpack-plugin');

const CommonConfig = require('./config.common.js');

module.exports = Merge(CommonConfig, {
  mode: 'development',

  watch: true,

  cache: false,

  plugins: [
    new CleanWebpackPlugin({
      root: process.cwd(),
      verbose: false,
      cleanOnceBeforeBuildPatterns: ['**/*', '!.gitkeep'],
    }),
  ],
});
