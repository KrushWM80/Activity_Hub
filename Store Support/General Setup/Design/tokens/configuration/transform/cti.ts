import styleDictionary from "style-dictionary";
import { AttributeTransform } from "style-dictionary/types/Transform";

const propertiesToCTI: Record<string, unknown> = {};

const propertiesKeys = new Set(Object.keys(propertiesToCTI));

/**
 * {@link https://github.com/amzn/style-dictionary/blob/c34cfa5313ee69f02783a2fb51d5f78720163d53/examples/advanced/component-cti/config.js}
 */
export const cti: Record<string, AttributeTransform> = {
  "attribute/cti": {
    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      // Only do this custom functionality in the 'component' top-level namespace.
      if (token.path[0] === "component") {
        const match = token.path.find((p) => propertiesKeys.has(p));

        if (match) {
          console.log(propertiesToCTI[match]);
          return propertiesToCTI[match];
        }
      }

      // Fallback to the original 'attribute/cti' transformer
      return styleDictionary.transform["attribute/cti"].transformer(token);
    },
    type: "attribute",
  },
};
