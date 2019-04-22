const { entryDir } = require('./paths');

const entriesNames = ['donate', 'charge', 'circle', 'business', 'old'];
const polyfillPaths = ['es6-promise/auto', 'nodent-runtime'];

const entries = entriesNames.reduce((acc, curr) => {
  acc[curr] = [...polyfillPaths, `${entryDir}/${curr}`];
  return acc;
}, {});

module.exports = entries;
