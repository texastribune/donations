// utility
const path = require('path');
const glob = require('fast-glob');
const { replaceExtension } = require('ds-toolbox-test/tasks/utils');

const CSS_OUTPUT_DIR = './static/build/';
const SVG_OUTPUT_DIR = './templates/includes';

const mappedStyles = async () => {
  // note: ignore '_' prefixed files
  const sassDirs = await glob(['./static/sass/[^_]*.scss']);
  const styleDirs = sassDirs.map(file => ({
    in: file,
    out: path.join(
      CSS_OUTPUT_DIR,
      replaceExtension(path.basename(file), '.css')
    ),
  }));
  return styleDirs;
};

const mappedIcons = [
  {
    in: './node_modules/ds-toolbox-test/assets/icons/base/',
    out: `${SVG_OUTPUT_DIR}/base_icons.html`,
  },
];

module.exports = {
  mappedStyles,
  mappedIcons,
};
