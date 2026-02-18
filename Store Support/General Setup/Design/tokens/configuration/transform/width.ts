import { Matcher } from "style-dictionary";
import { ValueTransform } from "style-dictionary/types/Transform";

/**
 * @param {import("style-dictionary").TransformedToken} token
 */
const widthMatcher: Matcher = (token) => {
  return token.path.includes("width");
};

/**
 * Custom transforms for width.
 */
export const width: Record<string, ValueTransform> = {
  /**
   * Transform width to "X%".
   */
  "width/toPercent": {
    matcher: widthMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      return token.original.value.match(
        /^(fill-screen|fill-parent|hug-contents)$/,
      )
        ? "100%"
        : token.value;
    },

    transitive: true,

    type: "value",
  },
};
