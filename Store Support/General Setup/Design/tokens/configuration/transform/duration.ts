import { Matcher } from "style-dictionary";
import { ValueTransform } from "style-dictionary/types/Transform";

/**
 * @param {import("style-dictionary").TransformedToken} token
 */
const durationMatcher: Matcher = (token) => {
  return token.path.includes("duration");
};

/**
 * Custom transforms for duration.
 */
export const duration: Record<string, ValueTransform> = {
  /**
   * Transform duration to milliseconds.
   *
   * @see {@link https://developer.android.com/reference/android/transition/Transition#attr_android:duration}
   */
  "duration/android": {
    matcher: durationMatcher,

    /**
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      const value = parseFloat(token.value) * 1000;

      if (Number.isNaN(value)) {
        throw new Error(
          `Could not transform token ${token.name}: ${token.value}`,
        );
      }

      return value;
    },

    transitive: true,

    type: "value",
  },

  "duration/ios": {
    matcher: durationMatcher,

    transformer(token) {
      const value = parseFloat(token.value);

      if (Number.isNaN(value)) {
        throw new Error(`Unable to parse duration: "${token.value}"`);
      }

      return value;
    },

    transitive: true,

    type: "value",
  },

  "duration/web": {
    matcher: durationMatcher,

    transformer(token) {
      const value = parseFloat(token.value) * 1000;

      if (Number.isNaN(value)) {
        throw new Error(`Unable to parse duration: "${token.value}"`);
      }

      return value;
    },

    transitive: true,

    type: "value",
  },
};
