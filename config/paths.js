const { utils } = require('@texastribune/queso-tools');
const {
  SCSS_DIR,
  CSS_OUTPUT_DIR,
  SVG_LOCAL_DIR,
  SVG_LIB_DIR,
  SVG_OUTPUT_SPRITE,
  SCSS_FILES,
  SVG_LIB_FILES,
  SVG_LOCAL_FILES,
} = require('./constants');

const cssMap = () =>
  SCSS_FILES.map(file => ({
    in: utils.resolveApp(`${SCSS_DIR}/${file}.scss`),
    out: utils.resolveApp(`${CSS_OUTPUT_DIR}/${file}.css`),
  }));

const svgMap = () => {
  const libSet = SVG_LIB_FILES.map(file =>
    utils.resolveApp(`${SVG_LIB_DIR}/${file}.svg`)
  );
  const localSet = SVG_LOCAL_FILES.map(file =>
    utils.resolveApp(`${SVG_LOCAL_DIR}/${file}.svg`)
  );
  return [
    {
      in: [...libSet, ...localSet],
      out: utils.resolveApp(SVG_OUTPUT_SPRITE),
    },
  ];
};

const manifest = utils.resolveApp(`${CSS_OUTPUT_DIR}styles.json`);

module.exports = {
  css: cssMap(),
  svg: svgMap(),
  manifest,
};
