import styleDictionary, { Matcher } from "style-dictionary";
import { ValueTransform } from "style-dictionary/types/Transform";

const pxToCGFloat = (value: string | number) =>
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

const toRem = (value: string | number) =>
  styleDictionary.transform["size/pxToRem"].transformer({
    value,
    name: "",
    path: [],
    original: {
      value,
    },
    filePath: "",
    isSource: false,
  });

/**
 * @param {import("style-dictionary").TransformedToken} token
 */
const elevationMatcher: Matcher = (token) => token.path.includes("elevation");

/**
 * Custom transformers for elevation tokens.
 *
 * @see {@link https://github.com/amzn/style-dictionary/issues/461#issuecomment-760664949}
 * @see {@link https://github.com/amzn/style-dictionary/issues/456#issuecomment-730606261}
 */
export const elevation: Record<string, ValueTransform> = {
  /**
   * Transform elevation tokens to emit the relative distance between two surfaces in `dp`.
   */
  "elevation/android": {
    matcher: elevationMatcher,

    transformer(token) {
      // TODO: figure out what to do with custom elevations
      if (token.attributes?.type) {
        if (isNaN(parseInt(token.attributes.type, 10))) {
          return "";
        }
        return { 100: "2dp", 200: "6dp", 300: "8dp" }[token.attributes.type];
      }
      return undefined;
    },

    type: "value",
  },

  /**
   * Transform elevation tokens to emit instances of the custom struct
   * defined in `LivingDesignElevation.swift`.
   */
  "elevation/ios": {
    matcher: elevationMatcher,

    transformer(token) {
      const values = Array.isArray(token.original.value)
        ? token.original.value
        : [token.original.value];

      return values
        .map(
          (elevation: {
            color: string;
            offsetX: string | number;
            offsetY: string | number;
            spread: string | number;
          }) => {
            const { color, offsetX, offsetY, spread } = elevation;

            return `LivingDesignElevation(
      color: ${styleDictionary.transform["color/UIColorSwift"].transformer({
        value: color,
        name: "",
        path: [],
        original: {
          value: color,
        },
        filePath: "",
        isSource: false,
      })},
      offset: CGSize(width: ${pxToCGFloat(offsetX)}, height: ${pxToCGFloat(
        offsetY,
      )}),
      radius: ${pxToCGFloat(spread)}
    )`;
          },
        )
        .join(", ");
    },

    type: "value",
  },

  "elevation/web": {
    matcher: elevationMatcher,

    transformer(token) {
      const values = Array.isArray(token.original.value)
        ? token.original.value
        : [token.original.value];

      return values
        .map(
          (elevation: {
            blur: string | number;
            color: string;
            offsetX: string | number;
            offsetY: string | number;
            spread: string | number;
          }) => {
            const { blur, color, offsetX, offsetY, spread } = elevation;

            return `${toRem(offsetX)} ${toRem(offsetY)} ${toRem(blur)} ${toRem(
              spread,
            )} ${color}`;
          },
        )
        .join(", ");
    },

    type: "value",
  },
};
