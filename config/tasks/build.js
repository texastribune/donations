// utility
const stylesRunner = require('@texastribune/ds-toolbox-tasks/styles');
const iconsRunner = require('@texastribune/ds-toolbox-tasks/icons');
const { logMessage } = require('@texastribune/ds-toolbox-tasks/utils');

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
