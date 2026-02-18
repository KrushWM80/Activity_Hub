import * as _ from "lodash";
import { Matcher } from "style-dictionary";
import { ValueTransform } from "style-dictionary/types/Transform";

/**
 * @param {import("style-dictionary").TransformedToken} token
 */
const fontFamilyMatcher: Matcher = (token) => {
  return token.path.includes("font") && token.path.includes("family");
};

/**
 * Custom transforms for the font tokens.
 */
export const font: Record<string, ValueTransform> = {
  /**
   * Transform font family for  web resource.
   *
   */
  "font/family/web": {
    matcher: fontFamilyMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      const fontStack = token.$extensions?.["livingdesign.fontStack"];
      return fontStack
        ? token.value +
            ", " +
            fontStack.map((font: string) => `'${font}'`).join(", ")
        : token.value;
    },

    type: "value",
  },

  /**
   * Transform font family to Android resource.
   *
   * @see {@link https://developer.android.com/guide/topics/resources/font-resource}
   */
  "font/family/android": {
    matcher: fontFamilyMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      const value = token.value.split(",")[0];

      if (!value) {
        throw new Error(
          `Could not transform token ${token.name}: ${token.value}`,
        );
      }

      return `@font/${_.snakeCase(value)}`;
    },

    type: "value",
  },

  /**
   * Transform `fontFamily` to a string for Swift.
   */
  "font/family/ios": {
    matcher: fontFamilyMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      const value = token.value.split(",")[0];

      if (!value) {
        throw new Error(
          `Could not transform token ${token.name}: ${token.value}`,
        );
      }

      return `"${_.camelCase(value)}"`;
    },

    type: "value",
  },
};
