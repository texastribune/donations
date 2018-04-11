const path = require('path');

const entryDir = path.join(process.cwd(), 'static', 'js', 'entry');
const buildDir = path.join(process.cwd(), 'static', 'js', 'build');

consolel.log(path.resolve(__dirname, './dist'));
console.log(entryDir, buildDir);

module.exports = { entryDir, buildDir };
