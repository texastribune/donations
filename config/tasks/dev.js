// lib
const { series, logMessage } = require('ds-toolbox-test/tasks/utils');

// internal
const watch = require('./watch');

async function develop() {
  const runner = series([watch]);
  await runner();
}

develop().catch(e => logMessage(e));
