const SCSS_DIR = './server/static/sass';
const CSS_OUTPUT_DIR = './server/static/build/';
const SVG_LOCAL_DIR = './server/static/svg';
const SVG_LIB_DIR = './node_modules/@texastribune/queso-ui/assets/icons/base/';
const SVG_OUTPUT_SPRITE = './server/templates/includes/base_icons.html';

const SCSS_FILES = ['account', 'blast', 'business', 'charge', 'circle', 'donate', 'old', 'waco'];

const SVG_LIB_FILES = [
  'bars',
  'bug',
  'caret-down',
  'camera',
  'facebook',
  'instagram',
  'linkedin',
  'reddit',
  'twitter',
  'your-texas',
  'youtube',
  'long-arrow-right'
];

const SVG_LOCAL_FILES = ['bell', 'check', 'close', 'download', 'pencil-fill', 'star'];

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
