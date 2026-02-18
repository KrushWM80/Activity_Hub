import { Formatter, formatHelpers } from "style-dictionary";
import { constructDeprecatedDocBlock } from "./helpers";

/**
 * Emits token variables in ES6 module format.
 *
 * This custom formatter is based on style-dictionary's "javascript/es6" format. It additionally
 * handles the `deprecated` token attribute.
 *
 * Original implementation: https://github.com/amzn/style-dictionary/blob/main/lib/common/formats.js#L363-L371
 */
export const customEs6ModuleFormatter = ({
  dictionary,
  file,
}: Parameters<Formatter>[0]) => {
  return (
    formatHelpers.fileHeader({ file }) +
    dictionary.allTokens
      .map((token) => {
        return `${
          token.deprecated
            ? constructDeprecatedDocBlock(token.deprecated.comment)
            : ""
        }export const ${token.name} = ${JSON.stringify(token.value)};${
          token.comment ? ` // ${token.comment}` : ""
        }`;
      })
      .join("\n")
  );
};

/**
 * Emits token variables in CommonJS module format.
 *
 * This custom formatter is based on style-dictionary's "javascript/module-flat" format. It additionally
 * handles the `deprecated` token attribute.
 *
 * Original implementation: https://github.com/amzn/style-dictionary/blob/main/lib/common/formats.js#L249-L253
 */
export const customCommonJsModuleFormatter = ({
  dictionary,
  file,
}: Parameters<Formatter>[0]) => {
  return `${formatHelpers.fileHeader({ file })}
module.exports = {
${dictionary.allTokens
  .map((token) => {
    return `${
      token.deprecated
        ? constructDeprecatedDocBlock(token.deprecated.comment)
            .split("\n")
            .map((line) => "  " + line)
            .join("\n")
        : "  "
    }"${token.name}": ${JSON.stringify(token.value)},${
      token.comment ? ` // ${token.comment}` : ""
    }`;
  })
  .join("\n")}
};`;
};

export const customEs6IconModuleFormatter = ({
  dictionary,
  file,
  options,
}: Parameters<Formatter>[0]) => {
  const { isMega } = options;

  return `${formatHelpers.fileHeader({ file })}
import * as Icon from ${isMega ? '"@livingdesign/icons/mega"' : '"@livingdesign/icons"'};

${dictionary.allTokens
  .map((token) => {
    return `export const ${token.attributes?.item} = Icon.${token.value};`;
  })
  .join("\n")}`;
};

export const customCommonJsIconModuleFormatter = ({
  dictionary,
  file,
  options,
}: Parameters<Formatter>[0]) => {
  const { isMega } = options;

  return `${formatHelpers.fileHeader({ file })}
const Icon = require(${isMega ? '"@livingdesign/icons/mega"' : '"@livingdesign/icons"'});

module.exports = {
${dictionary.allTokens
  .map((token) => {
    return `  "${token.attributes?.item}": Icon.${token.value},`;
  })
  .join("\n")}
};`;
};
