import { ValueTransform } from "style-dictionary/types/Transform";

export const alias: Record<string, ValueTransform> = {
  /**
   * Transform `aliasName` to a string.
   */
  "alias/sass": {
    /**
     * Match alias properties.
     *
     * @param {import("style-dictionary").TransformedToken} token
     * @returns {boolean}
     */
    matcher(token) {
      return token.path.includes("aliasName");
    },

    /**
     * @param {import("style-dictionary").TransformedToken} token
     * @returns {string}
     */
    transformer(token) {
      return `"${token.value}"`;
    },

    type: "value",
  },
};
