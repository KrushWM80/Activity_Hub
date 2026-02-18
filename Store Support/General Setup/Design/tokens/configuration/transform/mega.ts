import { Matcher } from "style-dictionary";
import { ValueTransform } from "style-dictionary/types/Transform";
/**
 * Get a scaled value from a token's original value.
 *
 * @param {number | string} value The original token's value
 * @param {number} factor The multiplication factor for the value
 * @returns {number | string} The scaled value
 */
const getScaledValue = (
  value: number | string,
  factor: number,
): number | string => {
  if (typeof value === "number") {
    return value * factor;
  }

  const parsedValue = parseFloat(value);

  if (Number.isNaN(parsedValue)) {
    throw new Error(`Could not scale value: "${value}"`);
  }

  return `${parsedValue * factor}px`;
};

/**
 * @todo Remove when cleaning up deprecated px-scale font sizes.
 *
 * @param {import("style-dictionary").TransformedToken} token
 */
const isDeprecatedFontSize: Matcher = (token) => {
  const { deprecated, path } = token;

  return path[0] === "font" && path[1] === "size" && !!deprecated;
};

export const mega: Record<string, ValueTransform> = {
  mega: {
    /**
     * Match tokens that should be scaled for mega:
     *
     * - Anything that is a size i.e. ends with "px", except breakpoints
     * - Elevation
     *
     * @param {import("style-dictionary").TransformedToken} token
     */
    matcher(token) {
      const { path, value } = token;

      return (
        (typeof value === "string" &&
          value.endsWith("px") &&
          !path.includes("breakpoint") &&
          !isDeprecatedFontSize(token)) ||
        path.includes("elevation")
      );
    },

    /**
     * Scale matched tokens for mega:
     *
     * - Border and separator widths: 2x
     * - Everything else: 1.5x
     *
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      const { path, value } = token;

      if (
        path.some(
          (piece, index, array) =>
            piece.startsWith("borderWidth") ||
            (piece.toLowerCase().includes("separator") &&
              array[index + 1] === "width"),
        )
      ) {
        return getScaledValue(value, 2);
      } else if (path.includes("elevation")) {
        return value.map(
          (item: {
            blur: string;
            color: string;
            offsetX: string;
            offsetY: string;
            spread: string;
          }) => {
            const { blur, color, offsetX, offsetY, spread } = item;

            return {
              blur: getScaledValue(blur, 1.5),
              color,
              offsetX: getScaledValue(offsetX, 1.5),
              offsetY: getScaledValue(offsetY, 1.5),
              spread: getScaledValue(spread, 1.5),
            };
          },
        );
      }

      return getScaledValue(value, 1.5);
    },

    transitive: false,

    type: "value",
  },
};
