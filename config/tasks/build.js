// utility
const stylesRunner = require('ds-toolbox-test/tasks/styles');
const iconsRunner = require('ds-toolbox-test/tasks/icons');
const { logMessage } = require('ds-toolbox-test/tasks/utils');

// internal
const { mappedStyles, mappedIcons, mappedStylesManifest } = require('../paths.js');

async function build() {
  // compile styles
  const mappedStylesArr = await mappedStyles();
  await stylesRunner(mappedStylesArr, mappedStylesManifest);

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
