const watch = require('glob-watcher');
const { styles, icons, utils } = require('@texastribune/queso-tools');
const { css, svg, manifest } = require('../paths');

async function dev() {
  const compileStyles = async showMsg => {
    const showMsgToggle = typeof showMsg !== 'undefined' ? showMsg : true;

    if (showMsgToggle) {
      utils.logMessage('Change detected...', 'purple');
    }
    try {
      await styles(css, manifest);
      if (showMsgToggle) {
        utils.logMessage('Change updated.', 'green');
      }
    } catch (err) {
      utils.logMessage('Error compiling CSS', 'red');
      utils.logMessage(err);
    }
  };

  const buildIcons = async () => {
    try {
      await icons(svg);
    } catch (err) {
      utils.logMessage(err);
    }
  };

  // initial compile of styles
  await compileStyles(false);

  // build icons
  await buildIcons();

  // styles watching
  utils.logMessage('Success! Watching styles...', 'green');
  watch(['./**/*.scss'], compileStyles);
}

dev().catch(e => utils.logMessage(e));
