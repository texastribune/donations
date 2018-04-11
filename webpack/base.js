const path = require('path');

const entryDir = path.join(process.cwd(), 'app', 'static', 'js', 'entry');
const buildDir = path.join(process.cwd(), 'app', 'static', 'js', 'build');

module.exports = { entryDir, buildDir };
