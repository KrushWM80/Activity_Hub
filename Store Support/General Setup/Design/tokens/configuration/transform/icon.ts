import * as _ from "lodash";
import { ValueTransform } from "style-dictionary/types/Transform";

export const icon: Record<string, ValueTransform> = {
  /**
   * Transform `iconName` to the correct Android format.
   */
  "iconName/android": {
    /**
     * Match iconName properties.
     *
     * @param {import("style-dictionary").TransformedToken} token
     * @returns {boolean}
     */
    matcher(token) {
      return token.path.includes("iconName");
    },

    /**
     * @param {import("style-dictionary").TransformedToken} token
     * @returns {string}
     */
    transformer(token) {
      // Should match the prefix on https://gecgithub01.walmart.com/LivingDesign/icons/blob/main/icons/build.gradle#L55
      const prefix = "ld_ic_";

      return `@drawable/${prefix + _.snakeCase(token.value)}`;
    },

    type: "value",
  },

  /**
   * Map `iconSize` to the correct icon dimensions.
   */
  "iconSize/android": {
    /**
     * Match iconSize properties.
     *
     * @param {import("style-dictionary").TransformedToken} token
     * @returns {boolean}
     */
    matcher(token) {
      return token.path.includes("iconSize");
    },

    /**
     * @param {import("style-dictionary").TransformedToken} token
     * @returns {string}
     */
    transformer(token) {
      return `@dimen/ld_size_icon_${token.value}`;
    },

    type: "value",
  },
};
