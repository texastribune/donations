const path = require('path');

const entryDir = path.join(process.cwd(), 'static', 'js', 'src', 'entry');
const buildDir = path.join(process.cwd(), 'static', 'build');

module.exports = { entryDir, buildDir };
