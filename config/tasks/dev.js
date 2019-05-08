// internal
const { series, logMessage } = require('ds-toolbox-test/tasks/utils');
const watch = require('./watch');

async function develop() {
  const runner = series([watch]);
  await runner();
}

// eslint-disable-next-line no-console
develop().catch(e => logMessage(e));