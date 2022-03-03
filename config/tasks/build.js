const { styles, icons } = require('@texastribune/queso-tools');
const { css, svg, manifest } = require('../paths');

async function build() {
  await styles(css, manifest);
  await icons(svg);
}

build().catch(err => {
  // eslint-disable-next-line no-console
  console.error(err.message);
  process.exit(1);
});
