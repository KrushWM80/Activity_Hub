/* eslint-env node */

/**
 * Generate PNGs at varying sizes (eg. 16, 24, 32, etc.) at scales for
 * react-native applications (1x, 2x, 3x) from SVG icon files.
 *
 * Note: This requires the following programs to be installed and available from the command line: `inkscape`, `rsvg-convert` (from librsvg), `convert` (from imagemagick)
 */
const glob = require('glob');
const mkdirp = require('mkdirp');
const path = require('path');
const {promisify} = require('util');
const fs = require('fs');

const exec = promisify(require('child_process').exec);
const globAsync = promisify(glob);
const mkdirpAsync = promisify(mkdirp);

const OUTPUT_DIR = path.resolve(__dirname, '../.tmp/new_pngs');
const SRC_DIR = path.resolve(__dirname, '../images/icons');

const sizes = {
  Check: [12],
  Close: [12],
  Star: [12],
  StarFill: [12],
  StarHalf: [12],
  ExclamationCircle: [48, 64],
  CheckCircle: [48, 64],
  Warning: [48, 64],
};

// /**
//  * Removes all whitespace from a given SVG file.
//  *
//  * @param {string} inputFile - The path to the input SVG file.
//  * @param {string} outputFile - The path to the output SVG file.
//  */
// const trimSVG = async (inputFile, outputFile) => {
//   await exec(`inkscape --export-plain-svg --export-filename="${outputFile}" --export-area-drawing "${inputFile}"`)
// }

/**
 * @typedef SVGFileInformation
 * @property {string} svg - The path to the SVG file.
 * @property {number[]} sizes - The sizes needed for this SVG file.
 */

/**
 * Generate PNGs of appropriate size from a given SVG image file.
 * @param {SVGFileInformation} inputFileInfo
 * @returns {string[]} Array of written file information.
 */
const generatePNGs = async (inputFileInfo) => {
  const {name} = path.parse(inputFileInfo.svg);
  const outputFiles = [];
  for await (const size of inputFileInfo.sizes) {
    for await (const mult of [1, 2, 3]) {
      const postfix = mult > 1 ? `@${mult}x` : '';
      const outputFileRsvg = path.join(
        OUTPUT_DIR,
        `${name}-${size}${postfix}-rsvg.png`,
      );
      const outputFile = path.join(OUTPUT_DIR, `${name}-${size}${postfix}.png`);
      // Convert SVG to PNG and resize, maintaining aspect ratio.
      await exec(
        `rsvg-convert -a -w ${size * mult} -h ${size * mult} ${
          inputFileInfo.svg
        } > ${outputFileRsvg}`,
      );

      // Fill PNG with black, and pad image to appropriate size.
      await exec(
        `convert -background none -fill "black" -colorize 100 -resize ${
          size * mult
        }x${size * mult} -gravity center -extent ${size * mult}x${
          size * mult
        } ${outputFileRsvg} ${outputFile}`,
      );
      fs.unlinkSync(outputFileRsvg);

      outputFiles.push(outputFile);
    }
  }
  return outputFiles;
};

const pBar = (current, max, caption, length = 20) => {
  const percent = current / max;
  const complete = Math.floor(percent * length);
  return `[${new Array(complete + 1).join('.')}${new Array(
    length - complete + 1,
  ).join(' ')}]${Math.floor(percent * 100)}% - ${caption} ${current} of ${max}`;
};

(async () => {
  const [inputFiles] = await Promise.all([
    globAsync(path.join(SRC_DIR, '/*.svg')),
    mkdirpAsync(OUTPUT_DIR),
  ]);
  const trimmedFiles = [];
  const generatedFiles = [];

  trimmedFiles.push(...inputFiles);

  const fileInfo = trimmedFiles.reduce((memo, svg) => {
    const {name} = path.parse(svg);
    return memo.concat({
      sizes: [...new Set([16, 24, 32].concat(...(sizes[name] || [])))].sort(
        (a, b) => a - b,
      ),
      svg,
    });
  }, []);

  // NOTE(luc): caller script will display this instead
  // process.stdout.write(`Generating PNG files\n`);
  process.stdout.write(
    '--------------------------------------------------------------\n',
  );

  for await (const file of fileInfo) {
    const progress = pBar(
      generatedFiles.length + 1,
      inputFiles.length,
      'Generating PNG files',
    );
    process.stdout.write(`\r${progress}`);
    const generated = await generatePNGs(file);
    generatedFiles.push(generated);
  }
  process.stdout.write('\n\n');
})();
