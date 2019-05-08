// lib
const stylesRunner = require('ds-toolbox-test/tasks/styles');
const iconsRunner = require('ds-toolbox-test/tasks/icons');
const { logMessage } = require('ds-toolbox-test/tasks/utils');

const { mappedStyles, mappedIcons } = require('../paths.js');

async function build() {
  // compile styles
  const mappedStylesArr = await mappedStyles();
  await stylesRunner(mappedStylesArr);

  // compile icons
  await iconsRunner(mappedIcons);
}

build()
  .then(() => {
    logMessage('Success!', 'green');
  })
  .catch(err => {
    logMessage('Something went wrong in the build...', 'red');
    logMessage(err);
    process.exit(1);
  });
