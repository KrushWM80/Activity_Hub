import styleDictionary, { Matcher } from "style-dictionary";
import { ValueTransform } from "style-dictionary/types/Transform";

/**
 * @param {import("style-dictionary").TransformedToken} token
 */
const textWrapMatcher: Matcher = (token) => {
  return token.path.includes("textWrap");
};

export const text: Record<string, ValueTransform> = {
  "text/align/ios": {
    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    matcher(token) {
      return token.path.includes("textAlign");
    },

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      // https://developer.apple.com/documentation/uikit/nstextalignment
      return `NSTextAlignment.${token.value}`;
    },

    type: "value",
  },

  "text/decoration/ios": {
    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    matcher(token) {
      return token.path.includes("textDecoration");
    },

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      return styleDictionary.transform["content/swift/literal"].transformer(
        token,
      );
    },

    type: "value",
  },

  /**
   * Transform `textWrap` to `android:maxLines` for Android.
   *
   * @see {@link https://developer.android.com/reference/android/widget/TextView#attr_android:maxLines}
   */
  "text/wrap/android": {
    matcher: textWrapMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      const value = token.value;

      if (typeof value !== "boolean") {
        throw new Error(
          `Could not transform token ${token.name}: ${token.value}`,
        );
      }

      return value === false ? 1 : 100;
    },

    type: "value",
  },

  /**
   * Transform `textWrap` to `numberOfLines` for iOS.
   *
   * @see {@link https://developer.apple.com/documentation/uikit/uilabel/1620539-numberoflines}
   */
  "text/wrap/ios": {
    matcher: textWrapMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      const value = token.value;

      if (typeof value !== "boolean") {
        throw new Error(
          `Could not transform token ${token.name}: ${token.value}`,
        );
      }

      return value === false ? "numberOfLines(1)" : "numberOfLines(0)";
    },

    type: "value",
  },

  /**
   * Transform `textWrap` to `white-space` for Web.
   *
   * @see {@link https://developer.mozilla.org/en-US/docs/Web/CSS/white-space}
   */
  "text/wrap/web": {
    matcher: textWrapMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      const value = token.value;

      if (typeof value !== "boolean") {
        throw new Error(
          `Could not transform token ${token.name}: ${token.value}`,
        );
      }

      return value === false ? "nowrap" : "normal";
    },

    type: "value",
  },
};
