const path = require('path');

const entryDir = path.join(process.cwd(), 'static', 'js', 'entry');
const buildDir = path.join(process.cwd(), 'static', 'js', 'build');

module.exports = { entryDir, buildDir };
