import { DesignToken, Formatter, formatHelpers } from "style-dictionary";
import { constructDeprecatedDocBlock } from "./helpers";

/**
 * Custom style-dictionary format to optionally set string literal types in outputted TS
 * type declaration files. In the current version of style-dictionary (v3.7.1), pre-defined
 * TS formats treat string values as type "string", resulting in frequent type assertions
 * in consuming code. (See https://jira.walmart.com/browse/LD-3010)
 *
 * This is meant to be a temporary solution until style-dictionary's TS formats are fixed.
 *
 * TODO: Add GH style-dictionary issue link
 */

// Original implementation: https://github.com/amzn/style-dictionary/blob/main/lib/utils/es6_.js
const unique = (arr: string[]) => {
  return [...new Set(arr)];
};

/**
 * Original implementation: https://github.com/amzn/style-dictionary/blob/main/lib/common/formatHelpers/getTypeScriptType.js
 *
 * @param {object} value An object with uknown type properties
 * @returns {string} A representation of the type model for the passed object
 */
function getObjectType(value: Record<string, unknown>) {
  const entries = Object.entries(value);
  return `{ ${entries
    .map(([key, property], index) => {
      const isLast = entries.length === index + 1;
      return `${key}: ${getTypeScriptType(property)}${!isLast ? ", " : ""}`;
    })
    .join("")} }`;
}

/**
 * Original implementation: https://github.com/amzn/style-dictionary/blob/main/lib/common/formatHelpers/getTypeScriptType.js
 *
 * @param {string[]} value An array to check each property of
 * @returns {string} A valid type for the passed array and it's items
 */
function getArrayType(passedArray: string[]) {
  if (passedArray.length > 0) {
    const firstValueType = getTypeScriptType(passedArray[0]);
    if (passedArray.every((v) => getTypeScriptType(v) === firstValueType)) {
      return firstValueType + "[]";
    } else {
      return `(${unique(
        passedArray.map((item, index) => {
          const isLast = passedArray.length === index + 1;
          return `${getTypeScriptType(item)}${!isLast ? " | " : ""}`;
        }),
      ).join("")})[]`;
    }
  }
  return "any[]";
}

/**
 * Given some value, returns a basic valid TypeScript type for that value.
 * Supports numbers, strings, booleans, arrays and objects of any of those types.
 *
 * NOTE: This function was copied from the style-dictionary codebase and modified to optionally
 * return string literal types for string values.
 *
 * Original implementation: https://github.com/amzn/style-dictionary/blob/main/lib/common/formatHelpers/getTypeScriptType.js
 *
 * @param {*} value A value to check the type of.
 * @param {boolean} outputLiteralTypes Feature flag to assign literal types to tokens with string and number values.
 * @return {string} A valid name for a TypeScript type.
 */
const getTypeScriptType = (
  value: DesignToken["value"],
  outputLiteralTypes?: boolean,
): string | number => {
  if (Array.isArray(value)) {
    return getArrayType(value);
  }
  if (typeof value === "object") {
    return getObjectType(value);
  }

  // The next line was added by LD to add support for string literal types
  if (outputLiteralTypes && typeof value === "string") {
    return `"${value}"`;
  }
  if (outputLiteralTypes && typeof value === "number") {
    return value;
  }

  if (["string", "number", "boolean"].includes(typeof value)) {
    return typeof value;
  }

  return "any";
};

/**
 * Emits TypeScript type declarations for token variables.
 *
 * This custom formatter is based on style-dictionary's "typescript/es6-declarations" format. It
 * additionally handles the `deprecated` token attribute and applies literal types to tokens with
 * string/number values.
 *
 * Original implementation: https://github.com/amzn/style-dictionary/blob/main/lib/common/formats.js#L405-L413
 */
export const customTypescriptFormatter = ({
  dictionary,
  file,
  options,
}: Parameters<Formatter>[0]) => {
  const { outputLiteralTypes } = options;

  return (
    formatHelpers.fileHeader({ file }) +
    dictionary.allProperties
      .map((prop) => {
        return `${
          prop.deprecated
            ? constructDeprecatedDocBlock(prop.deprecated.comment)
            : ""
        }export const ${prop.name} : ${getTypeScriptType(
          prop.value,
          outputLiteralTypes,
        )};${prop.comment ? ` // ${prop.comment}` : ""}`;
      })
      .join("\n")
  );
};

export const customTypescriptIconModuleFormatter = ({
  dictionary,
  file,
  options,
}: Parameters<Formatter>[0]) => {
  const { isMega } = options;

  return `${formatHelpers.fileHeader({ file })}
import {WithIconProps} from ${isMega ? '"@livingdesign/icons/mega"' : '"@livingdesign/icons"'};

${dictionary.allProperties
  .map((prop) => {
    return `export const ${prop.attributes?.item}: (props: WithIconProps) => JSX.Element;`;
  })
  .join("\n")}`;
};
