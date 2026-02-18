import { customScssFormatter } from "./scss";

describe("customScssFormatter", () => {
  const mockDictionaryProperties = {
    allProperties: [],
    properties: {},
    tokens: {},
  };

  const mockTransformedTokenProperties = {
    filePath: "",
    isSource: true,
    path: [],
  };

  test("should return reference value for themeable token", () => {
    const mockTokenName = "component-bottom-sheet-container-background-color";

    const dictionary = {
      allTokens: [
        {
          name: mockTokenName,
          original: {
            value: "{core.color.white}",
          },
          value: "#FFFFFF",
          ...mockTransformedTokenProperties,
        },
      ],
      usesReference: () => true,
      getReferences: () => [
        {
          ...mockTransformedTokenProperties,
          name: "color-surface-overlay",
          original: { value: "" },
          path: ["semantic", "color", "surface", "overlay"],
          themeable: true,
          value: "FFFFFF",
        },
      ],
      ...mockDictionaryProperties,
    };
    const file = { destination: "" };

    const result = customScssFormatter({
      dictionary,
      file,
      options: {},
      platform: {},
    });

    expect(result).toEqual(
      expect.stringContaining(
        `$${mockTokenName}: var(--ld-semantic-color-surface-overlay, FFFFFF)`,
      ),
    );
  });

  test("should not return reference value for non-themeable token", () => {
    const mockTokenName =
      "component-bottom-sheet-container-state-exit-active-transition-duration";
    const mockTokenValue = "0.5s";

    const dictionary = {
      allTokens: [
        {
          name: mockTokenName,
          original: {
            value: "{core.duration.500}",
          },
          value: mockTokenValue,
          ...mockTransformedTokenProperties,
        },
      ],
      usesReference: () => true,
      getReferences: () => [
        {
          name: "{core.duration.500}",
          original: { value: "" },
          value: mockTokenValue,
          ...mockTransformedTokenProperties,
        },
      ],
      ...mockDictionaryProperties,
    };
    const file = { destination: "" };

    const result = customScssFormatter({
      dictionary,
      file,
      options: {},
      platform: {},
    });

    expect(result).toEqual(
      expect.stringContaining(`$${mockTokenName}: ${mockTokenValue}`),
    );
  });
});
