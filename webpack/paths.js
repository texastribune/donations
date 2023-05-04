const path = require('path');

const entryDir = path.join(process.cwd(), 'server', 'static', 'js', 'src', 'entry');
const buildDir = path.join(process.cwd(), 'server', 'static', 'build');

module.exports = { entryDir, buildDir };
