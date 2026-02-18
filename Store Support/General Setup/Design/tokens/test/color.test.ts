import styleDictionary, {
  Core,
  DesignTokens,
  DesignToken,
} from "style-dictionary";

import configuration from "../configuration";

interface PartiallyTransformedToken extends DesignToken {
  name: string;
  path: string[];
}

const isDesignToken = (item: unknown): item is DesignToken => {
  return !!item && typeof item === "object" && "value" in item;
};

/**
 * @note style-dictionary does not appear to provide `TransformedToken`s to
 * anything besides formatters. This utility flattens and filters semantic color
 * tokens.
 */
const getSemanticColorTokens = (core: Core): PartiallyTransformedToken[] => {
  const tokens: PartiallyTransformedToken[] = [];

  const items: {
    path: string[];
    property: DesignToken | DesignTokens;
  }[] = [
    {
      path: ["color"],
      property: core.properties.semantic.color,
    },
  ];

  while (items.length) {
    const { path, property } = items.shift()!;

    if (isDesignToken(property)) {
      if (!property.filePath.includes("src/semantic/")) {
        continue;
      }

      tokens.push({
        ...property,
        name: path.join("."),
        path,
      });
    } else if (!!property && typeof property === "object") {
      for (const [key, value] of Object.entries(property)) {
        items.push({
          path: [...path, key],
          property: value,
        });
      }
    }
  }

  return tokens;
};

describe("Color", () => {
  const core = styleDictionary.extend(configuration);

  const semanticColorTokens = getSemanticColorTokens(core);

  test.each(semanticColorTokens)(
    "Should have a .darkValue property for token: $name.",
    (token) => {
      expect(token).toHaveProperty("darkValue");
    },
  );
});
