const SCSS_DIR = './static/sass';
const CSS_OUTPUT_DIR = './static/build/';
const SVG_LOCAL_DIR = './static/svg';
const SVG_LIB_DIR = './node_modules/@texastribune/queso-ui/assets/icons/base/';
const SVG_OUTPUT_SPRITE = './templates/includes/base_icons.html';

const SCSS_FILES = ['account', 'business', 'charge', 'circle', 'donate', 'old'];

const SVG_LIB_FILES = [
  'bars',
  'bug',
  'camera',
  'facebook',
  'instagram',
  'linkedin',
  'reddit',
  'twitter',
  'your-texas',
  'youtube',
];

const SVG_LOCAL_FILES = ['bell', 'check', 'close', 'download', 'star'];

module.exports = {
  SCSS_DIR,
  CSS_OUTPUT_DIR,
  SVG_LOCAL_DIR,
  SVG_LIB_DIR,
  SVG_OUTPUT_SPRITE,
  SCSS_FILES,
  SVG_LIB_FILES,
  SVG_LOCAL_FILES,
};
