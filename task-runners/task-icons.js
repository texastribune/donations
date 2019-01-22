const dirTree = require('directory-tree');
const fs = require('fs');
const SVGSpriter = require('svg-sprite');
const pathTool = require('path');
const mkdirp = require('mkdirp');

// Folders to parse
const groups = ['base', 'circle'];

// Loop through each icon in each folder and build SVG sprite
(buildIcons => {
  groups.forEach(group => {
    const iconTree = dirTree(`./static/icons/${group}`);
    const allArr = iconTree.children;
    const newArr = [];
    // Create spriter instance (see https://github.com/jkphl/svg-sprite#general-configuration-options for `config` examples)
    const spriter = new SVGSpriter({
      dest: './templates/icons',
      mode: {
        symbol: {
          mode: 'symbol',
          sprite: `${group}-sprite`,
          inline: true,
          dest: '',
          example: false
        }
      },
      svg: {
        xmlDeclaration: false,
        doctypeDeclaration: false
      }
    });
    if (Array.isArray(allArr)) {
      allArr.forEach(element => {
        // Build new clean array
        newArr.push(element.name.replace(/(\/|\.|svg)/g, ''));
        // Add spriter icon
        let svgPath = `./${element.path}`;
        spriter.add(
          pathTool.resolve(svgPath),
          element.name,
          fs.readFileSync(svgPath, { encoding: 'utf-8' })
        );
      });
    }
    // Compile the sprite
    spriter.compile(function (error, result) {
      /* Write `result` files to disk */
      for (var mode in result) {
        for (var resource in result[mode]) {
          mkdirp.sync(pathTool.dirname(result[mode][resource].path));
          // Add display: none prop for accessibility and perf
          // @link: https://www.24a11y.com/2018/accessible-svg-icons-with-inline-sprites/
          let fileContents = (result[mode][resource].contents).toString('utf8');
          fileContents = fileContents.replace(/position:absolute/, 'display:none;')
          fs.writeFileSync(
            result[mode][resource].path,
            fileContents
          );
        }
      }
    });
    console.log(`✓ Create icon sprite in ./templates/icons/${group}-sprite.svg`);
  });
})();
