import { Formatter, formatHelpers } from "style-dictionary";
import { constructDeprecatedDocBlock } from "./helpers";

/**
 * Emits token variables in CommonJS module format.
 *
 * This custom formatter is based on style-dictionary's "javascript/module-flat" format. It additionally
 * handles the `deprecated` and `darkValue` token attributes.  It also adds support for referencing
 * primitive and semantic tokens.
 *
 * Original implementation: https://github.com/amzn/style-dictionary/blob/main/lib/common/formats.js#L249-L253
 */
export const customReactNativeCommonJsModuleFormatter = ({
  dictionary,
  file,
  options,
}: Parameters<Formatter>[0]) => {
  const isDarkMode = options.isDarkMode ?? false;

  return `${formatHelpers.fileHeader({ file })}
module.exports = {
${dictionary.allTokens
  .map((token) => {
    let value =
      isDarkMode && "darkValue" in token ? token.darkValue : token.value;
    const originalValue =
      isDarkMode && "darkValue" in token.original
        ? token.original.darkValue
        : token.original.value;
    if (dictionary.usesReference(originalValue)) {
      const [reference] = dictionary.getReferences(originalValue);
      if (reference.filePath.includes("primitive")) {
        value = `$primitive.${reference.name}`;
      } else if (reference.filePath.includes("semantic")) {
        value = `$semantic.${reference.name}`;
      }
    }
    return `${
      token.deprecated
        ? constructDeprecatedDocBlock(token.deprecated.comment)
            .split("\n")
            .map((line) => "  " + line)
            .join("\n")
        : "  "
    }"${token.name}": ${JSON.stringify(value)},${
      token.comment ? ` // ${token.comment}` : ""
    }`;
  })
  .join("\n")}
};`;
};
