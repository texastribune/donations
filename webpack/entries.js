const { entryDir } = require('./paths');

const entriesNames = [
  'donate',
  'charge',
  'circle',
  'business',
  'blast',
  'waco',
  'old',
  'account',
];
const polyfillPaths = ['es6-promise/auto', 'nodent-runtime'];

const entries = entriesNames.reduce((acc, curr) => {
  acc[curr] = [...polyfillPaths, `${entryDir}/${curr}`];
  return acc;
}, {});

module.exports = entries;
