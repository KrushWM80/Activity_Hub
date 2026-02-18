/*
  TRANSFORM NAME - updateJestConfig
  This transform is meant to be run only on consumer app:
  It needs to be run by devs manually using npx runCodemods updateJestConfig.
  It performs the following:
    - This transform will run on jest.config.js / package.json to update the jest transformIgnorePatterns.
  Example:
    BEFORE - >  transformIgnorePatterns: [
    '<rootDir>/node_modules/(?!(react-native)']

    AFTER - >   transformIgnorePatterns: [
    '<rootDir>/node_modules/(?!(react-native|@walmart/gtp-shared-components|@walmart/gtp-shared-icons)'];
*/

import {API, FileInfo, Options} from 'jscodeshift';

export default function transformer(
  file: FileInfo,
  api: API,
  options: Options,
) {
  /* jscodeshift api to parse and update the identifiers*/
  const j = api.jscodeshift;

  /* File Output Print Options */
  const printOptions = options.printOptions || {
    quote: 'single',
    trailingComma: true,
    flowObjectCommas: true,
    arrowParensAlways: true,
    arrayBracketSpacing: false,
    objectCurlySpacing: false,
  };

  /* File root to parse AST. */
  var root;

  const filePath = require('path');
  const fs = require('fs');

  const filePrefix1 = 'jest.config';
  const filePrefix2 = 'package.json';
  const fileName = filePath.basename(file.path);

  const componentsString = '@walmart/gtp-shared-components';
  const iconsString = '@walmart/gtp-shared-icons';

  const replaceOrAppendString = (str: string) => {
    if (str.includes(componentsString) && !str.includes(iconsString)) {
      return str.replace(
        componentsString,
        `${componentsString}|${iconsString}`,
      );
    } else if (!str.includes(componentsString) && str.includes(iconsString)) {
      return str.replace(iconsString, `${componentsString}|${iconsString}`);
    } else if (!str.includes(componentsString) && !str.includes(iconsString)) {
      const lastIndexPosition = str.lastIndexOf(')');
      const updatedString = `${str.substring(
        0,
        lastIndexPosition,
      )}|${componentsString}|${iconsString})`;
      return updatedString;
    }
    return str;
  };

  if (fileName.startsWith(filePrefix1)) {
    const tsxParser = j.withParser('tsx');
    root = tsxParser(file.source);
  } else if (fileName.startsWith(filePrefix2)) {
    const parsedJson = JSON.parse(
      JSON.parse(JSON.stringify(file.source, null, 2)),
    );
    if (parsedJson.jest.transformIgnorePatterns) {
      const transformIgnorePatterns = parsedJson.jest.transformIgnorePatterns;

      parsedJson.jest.transformIgnorePatterns = transformIgnorePatterns.map(
        (element: any) => {
          return replaceOrAppendString(element);
        },
      );
    }
    fs.writeFileSync(file.path, JSON.stringify(parsedJson, null, 2) + '\n');
    return;
  } else {
    return;
  }

  const validateKeys = (path: any) => {
    const {value, parentPath} = path || {};
    const {key} = value || {};
    const {name} = key || {};
    if (name && name === 'transformIgnorePatterns') {
      return 'IdentifierFound';
    } else {
      return parentPath;
    }
  };

  const checkIdentifier = (literalPath: any) => {
    let isKeyFind = 'IdentifierNotFound';
    let path = literalPath;
    for (var _i = 0; isKeyFind === 'IdentifierNotFound'; _i++) {
      const verifiedPath = validateKeys(path);
      if (verifiedPath && verifiedPath === 'IdentifierFound') {
        isKeyFind = 'IdentifierFound';
        return 'IdentifierFound';
      } else if (verifiedPath) {
        path = verifiedPath;
      } else {
        isKeyFind = 'ParentPathEmpty';
        return 'ParentPathEmpty';
      }
    }
    return isKeyFind;
  };

  root.find(j.Literal).filter((path: any) => {
    const str = '' + path.node.value;
    const isKeyTransformIgnorePatternsFind = checkIdentifier(path);
    if (isKeyTransformIgnorePatternsFind === 'IdentifierFound') {
      j(path).replaceWith(j.literal(replaceOrAppendString(str)));
    } else {
      return;
    }
  });

  return root.toSource(printOptions);
}
