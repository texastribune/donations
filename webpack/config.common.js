const WebpackAssetsManifest = require('webpack-assets-manifest');

const { entryDir, buildDir } = require('./base');

module.exports = {
  context: process.cwd(),

  entry: {
    donate: `${entryDir}/donate`,
  },

  output: {
    filename: '[name].[chunkhash].js',
    chunkFilename: '[name].chunk.[chunkhash].js',
    library: 'jsBundle',
    libraryTarget: 'umd',
    path: buildDir,
  },

  plugins: [
    new WebpackAssetsManifest({
      output: 'assets.json',
      entrypoints: true,
    }),
  ],

  optimization: {
    splitChunks: {
      chunks: 'all',
      name: false,
    },

    runtimeChunk: 'single',
  },

  stats: {
    warnings: false,
    cached: false,
  },

  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
      },

      {
        test: /\.vue$/,
        exclude: /node_modules/,
        loader: 'vue-loader',
      },
    ],
  },

  resolve: {
    extensions: ['.js', '.json', '.jsx', '.vue'],
  },
};
