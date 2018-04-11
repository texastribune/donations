const path = require('path');

const entryDir = path.join(__dirname, '..', 'static', 'js', 'entry');
const buildDir = path.join(__dirname, '..', 'static', 'js', 'build');

module.exports = { entryDir, buildDir };
