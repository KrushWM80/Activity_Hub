import styleDictionary, { Matcher } from "style-dictionary";
import { ValueTransform } from "style-dictionary/types/Transform";

const pxToCGFloat = (value: string) =>
  styleDictionary.transform["size/swift/remToCGFloat"].transformer(
    {
      value,
      name: "",
      path: [],
      original: {
        value,
      },
      filePath: "",
      isSource: false,
    },
    { basePxFontSize: 1 },
  );
/**
 * @param {import("style-dictionary").TransformedToken} token
 */
const timingMatcher: Matcher = (token) => {
  return token.path.includes("timing");
};

export const timing: Record<string, ValueTransform> = {
  "timing/ios": {
    matcher: timingMatcher,

    /**
     * Return a `CAMediaTimingFunction`.
     *
     * @see {@link https://developer.apple.com/documentation/quartzcore/camediatimingfunction}
     * @see {@link https://developer.apple.com/documentation/quartzcore/camediatimingfunctionname}
     *
     * @param {import("style-dictionary").TransformedToken} token
     */
    transformer(token) {
      if (token.value === "linear") {
        return "CAMediaTimingFunctionName.linear";
      }

      const points =
        /cubic-bezier\(([\d.]+), ([\d.]+), ([\d.]+), ([\d.]+)\)/.exec(
          token.value,
        );

      if (!points) {
        throw new Error(`Could not parse timing: "${token.value}"`);
      }

      return `CAMediaTimingFunction(controlPoints: ${pxToCGFloat(
        points[1],
      )}, ${pxToCGFloat(points[2])}, ${pxToCGFloat(points[3])}, ${pxToCGFloat(
        points[4],
      )})`;
    },

    type: "value",
  },
};
