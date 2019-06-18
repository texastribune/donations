const Merge = require('webpack-merge');

const CommonConfig = require('./config.common.js');

module.exports = Merge(CommonConfig, {
  mode: 'development',

  watch: true,

  cache: false,
});
