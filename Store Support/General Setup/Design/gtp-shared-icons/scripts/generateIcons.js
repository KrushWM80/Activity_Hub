/* eslint-env node */
/* eslint-disable no-unused-vars */
const flatten = require('lodash/flatten');
const fs = require('fs');
const glob = require('glob');
// const kebabCase = require('lodash/kebabCase');
const map = require('lodash/map');
const mkdirp = require('mkdirp');
const path = require('path');
const {promisify} = require('util');

const {
  iconMarkdownTemplate,
  iconTemplate,
  iconTestTemplate,
  iconIndexTemplate,
  pascalCase,
} = require('./utils.js');

const ICONS_DIR = path.resolve(__dirname, '../assets/images/icons');
const JS_DIR = path.resolve(__dirname, '../src/icons');
const globAsync = promisify(glob);
const pattern = /^(.*)-(\d+)$/;
const mkdirpAsync = promisify(mkdirp);
const writeFile = promisify(fs.writeFile);

const TESTS_DIR = path.join(JS_DIR, '__tests__');

/**
 * @param {string[]} files Collection of icons' source PNGs
 * @param {string} componentsDir Full path to icons' component directory
 * @returns {Object} Images meta
 */
const getImagesMeta = (files, componentsDir) =>
  files.reduce((memo, image) => {
    if (!image.includes('@')) {
      const match = pattern.exec(path.parse(image).name);

      if (!match) {
        throw new Error(`Cannot parse image name: ${image}`);
      }

      const [, name, size] = match;

      const meta = new Map([
        ['name', name],
        ['importPath', path.relative(componentsDir, image)],
        ['size', size],
      ]);

      if (!(name in memo)) {
        memo[name] = [meta];
      } else {
        memo[name].push(meta);
      }
    }

    return memo;
  }, {});

/**
 * Write the files.
 *
 * @param {string} componentsDir
 * @param {string} testsDir
 * @param {string} [prefix='']
 * @returns {Function} Mapper fn that resolves with `Promise<Array,Error>`
 */
const getFileWriter =
  (componentDir, testDir, prefix = '') =>
  (images, name) => {
    const className = pascalCase(`${prefix}${name}Icon`);
    const componentPath = path.join(
      componentDir,
      `${pascalCase(`${prefix}${name}Icon`)}.tsx`,
    );
    const markdownPath = path.join(
      componentDir,
      `${pascalCase(`${prefix}${name}Icon`)}.md`,
    );

    return Promise.all([
      writeFile(
        componentPath,
        iconTemplate(
          className,
          images,
          path
            .relative(path.resolve(__dirname, '..'), componentPath)
            .replace(/\.tsx$/, ''),
        ),
      ),
      writeFile(markdownPath, iconMarkdownTemplate(className, images)),
    ]).then(() => [componentPath, markdownPath]);
  };

const writeIndex = (componentDir, icons, prefix = '') => {
  const fileInfo = map(Object.keys(icons), (key) => ({
    fileName: `./${pascalCase(`${prefix}${key}Icon`)}`,
    componentName: pascalCase(`${prefix}${key}Icon`),
  }));
  return writeFile(
    path.join(componentDir, 'index.tsx'),
    iconIndexTemplate(fileInfo),
  );
};

Promise.all([globAsync(path.join(ICONS_DIR, '*.png')), mkdirpAsync(JS_DIR)])
  .then(([files]) => {
    const imagesMeta = getImagesMeta(files, JS_DIR);

    return Promise.all(
      map(imagesMeta, getFileWriter(JS_DIR)).concat(
        writeIndex(JS_DIR, imagesMeta),
      ),
    );
  })
  .then((results) => {
    console.log('Components generation complete');
    // console.log(`Created templates: ${flatten(results).join('\n')} `);
  })
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
