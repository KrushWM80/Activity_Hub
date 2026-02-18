import styleDictionary, { Matcher, TransformedToken } from "style-dictionary";
import { ValueTransform } from "style-dictionary/types/Transform";

const pxToRem = (token: TransformedToken) =>
  styleDictionary.transform["size/pxToRem"].transformer(token);

/**
 * @param {import("style-dictionary").TransformedToken} token
 */
const pxSizeMatcher: Matcher = (token) => {
  return typeof token.value === "string" && token.value.indexOf("px") !== -1;
};

/**
 * Custom transformers for size tokens.
 *
 * @see {@link https://github.com/amzn/style-dictionary/issues/461#issuecomment-760664949}
 * @see {@link https://github.com/amzn/style-dictionary/tree/3.0/examples/advanced/transitive-transforms}
 */
export const pxSize: Record<string, ValueTransform> = {
  /**
   * Custom `sp` and `dp` unit transformer for Android.
   *
   * @note Use `sp` for font sizes, `dp` for everything else.
   *
   * @see {@link https://developer.android.com/training/multiscreen/screendensities#TaskUseDP}
   */
  "pxSize/android": {
    matcher: pxSizeMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      const floatValue = parseFloat(token.value);

      if (Number.isNaN(floatValue)) {
        throw new Error(`Invalid size: ${token.name}: ${token.value}`);
      }

      const unit =
        token.attributes?.category === "font" || token.name.includes("font")
          ? "sp"
          : "dp";

      return `${
        floatValue % 1 > 0 ? floatValue.toFixed(2) : floatValue
      }${unit}`;
    },

    transitive: true,

    type: "value",
  },

  "pxSize/reactnative": {
    matcher: pxSizeMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      const value = styleDictionary.transform["size/px"].transformer(token);

      return parseFloat(value.replace("px", ""));
    },

    transitive: true,

    type: "value",
  },

  "pxSize/ios": {
    matcher: pxSizeMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer: (token) => {
      const value = pxToRem(token);

      const transformedValue = styleDictionary.transform[
        "size/swift/remToCGFloat"
      ].transformer(Object.assign({}, token, { value }));

      return transformedValue;
    },

    transitive: true,

    type: "value",
  },

  "pxSize/web": {
    matcher: pxSizeMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} prop
     */
    transformer(token) {
      return pxToRem(token);
    },

    transitive: true,

    type: "value",
  },
};
