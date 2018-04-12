const path = require('path');

let buildDir;
const entryDir = path.join(process.cwd(), 'static', 'js', 'src', 'entry');
const env = process.env.NODE_ENV;

if (env === 'production') {
  buildDir = path.join(process.cwd(), 'static', 'js', 'prod');
} else {
  buildDir = path.join(process.cwd(), 'static', 'js', 'build');
}

module.exports = { entryDir, buildDir };
