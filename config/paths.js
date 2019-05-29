// utility
const path = require('path');
const glob = require('fast-glob');
const { replaceExtension } = require('ds-toolbox-test/tasks/utils');

const CSS_OUTPUT_DIR = './static/build/';
const SVG_LIB_DIR = './node_modules/ds-toolbox-test/assets/icons/base/';
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
    in: [
      `${SVG_LIB_DIR}bug.svg`,
      `${SVG_LIB_DIR}facebook.svg`,
      `${SVG_LIB_DIR}instagram.svg`,
      `${SVG_LIB_DIR}linkedin.svg`,
      `${SVG_LIB_DIR}reddit.svg`,
      `${SVG_LIB_DIR}twitter.svg`,
      `${SVG_LIB_DIR}your-texas.svg`,
      `${SVG_LIB_DIR}youtube.svg`,
      './static/img/check.svg',
      './static/img/star.svg'
    ],
    out: `${SVG_OUTPUT_DIR}/base_icons.html`,
  },
];

const mappedStylesManifest = `${CSS_OUTPUT_DIR}styles.json`;


module.exports = {
  mappedStyles,
  mappedIcons,
  mappedStylesManifest
};
