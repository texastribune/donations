const WebpackAssetsManifest = require('webpack-assets-manifest');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const Autoprefixer = require('autoprefixer');

const { entryDir, buildDir } = require('./base');

module.exports = {
  context: process.cwd(),

  entry: {
    donate: `${entryDir}/donate/index`,
    charge: `${entryDir}/charge/index`,
    circle: `${entryDir}/circle/index`,
    business: `${entryDir}/business/index`,
    old: `${entryDir}/old/index`,
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
    new MiniCssExtractPlugin({
      filename: 'styles.[chunkhash].css',
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
        test: /\.(scss|sass)$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader', {
            loader: 'postcss-loader',
            options: {
              plugins: [
                Autoprefixer({
                  browsers: [
                    '> 0.5%',
                    'last 2 versions',
                    'Firefox ESR',
                    'iOS >= 10',
                    'Safari >= 11',
                    'not dead',
                  ],
                }),
              ],
            },
          },
          'sass-loader',
        ],
      },

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

      {
        test: /\.(png|jpg|gif|svg)$/,
        loader: 'file-loader',
      },
    ],
  },

  resolve: {
    extensions: ['.js', '.json', '.jsx', '.vue'],
  },
};
