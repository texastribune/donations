const webpack = require('webpack');
const Merge = require('webpack-merge');
const SentryWebpackPlugin = require('@sentry/webpack-plugin');

const CommonConfig = require('./config.common.js');
const { buildDir } = require('./paths');

const config = Merge(CommonConfig, {
  mode: 'production',

  devtool: 'source-map',

  plugins: [new webpack.HashedModuleIdsPlugin()],
});

/*
 Releasing requires the following env variables:
 - SENTRY_AUTH_TOKEN
 - SENTRY_ORG
 - SENTRY_PROJECT

 No need to have these variables in your local environment
 because we'll only ever want to do releases during a prod build.

 Given that, it's also important to have ENABLE_SENTRY_RELEASE=False
 set in your local environment.
*/

if (process.env.ENABLE_SENTRY_RELEASE.toLowerCase() === 'true') {
  config.plugins.push(
    new SentryWebpackPlugin({
      release: `${new Date().toString()}-${process.env.SENTRY_ENVIRONMENT}`,
      include: buildDir,
    })
  );
}

module.exports = config;
