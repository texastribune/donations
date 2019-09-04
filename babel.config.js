module.exports = {
  presets: [
    [
      '@babel/env',
      {
        modules: false,
        exclude: ['transform-regenerator', 'transform-async-to-generator'],
      },
    ],
  ],

  plugins: [
    ['module:fast-async', { useRuntimeModule: true }],
    '@babel/syntax-dynamic-import',
    ['@babel/transform-runtime', { regenerator: false, useESModules: true }],
  ],
};
