// utility
const watch = require('glob-watcher');
const iconsRunner = require('ds-toolbox-test/tasks/icons');
const stylesRunner = require('ds-toolbox-test/tasks/styles');
const { logMessage } = require('ds-toolbox-test/tasks/utils');

// internal
const { mappedStyles, mappedIcons, mappedStylesManifest } = require('../paths.js');


module.exports = async () => {
  const compileStyles = async showMsg => {
    const showMsgToggle = typeof showMsg !== 'undefined' ? showMsg : true;

    if (showMsgToggle) {
      logMessage('Change detected...', 'purple');
    }
    try {
      const mappedStylesArr = await mappedStyles();
      await stylesRunner(mappedStylesArr, mappedStylesManifest);
    } catch (err) {
      logMessage('Error compiling CSS.', 'red');
      logMessage(err);
    }
  };

  const buildIcons = async () => {
    try {
      await iconsRunner(mappedIcons);
    } catch (err) {
      logMessage(err);
    }
  };

  // initial compile of styles
  await compileStyles(false);

  // build icons
  await buildIcons();

  // styles watching
  logMessage('Success! Watching styles...', 'green');
  watch(['./**/*.scss'], compileStyles);
};
