import { Matcher } from "style-dictionary";
import { ValueTransform } from "style-dictionary/types/Transform";

/**
 * Match alignment properties.
 *
 * @param {import("style-dictionary").TransformedToken} token
 * @returns {boolean}
 */
const alignmentMatcher: Matcher = (token) =>
  new RegExp(/^align(Horizontal|Vertical)/).test(
    token.path[token.path.length - 1],
  );

const webAlignmentMap = {
  end: "flex-end",
  start: "flex-start",
};

/**
 * Custom transformers for alignment tokens.
 */
export const alignment: Record<string, ValueTransform> = {
  "alignment/web": {
    matcher: alignmentMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      const { value } = token.original;

      if (typeof value === "string" && (value === "end" || value === "start")) {
        return webAlignmentMap[value];
      }
      return value;
    },

    transitive: true,

    type: "value",
  },
};
