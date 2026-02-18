import { Formatter, formatHelpers } from "style-dictionary";

export const customCssFormatter: Formatter = (args) => {
  const { dictionary, file, options } = args;

  const isDarkMode = options.isDarkMode ?? false;
  const prefix = options.prefix ?? "ld-";
  const selector = options.selector ?? ":root";

  return [
    formatHelpers.fileHeader({ file }),

    `${selector} {`,

    ...dictionary.allTokens.map((token) => {
      const value =
        isDarkMode && "darkValue" in token ? token.darkValue : token.value;
      const originalValue =
        isDarkMode && "darkValue" in token.original
          ? token.original.darkValue
          : token.original.value;

      const line = (val = value) => {
        return `  --${prefix}${token.name}: ${val};${
          token.comment ? ` /* ${token.comment} */` : ""
        }`;
      };

      if (!dictionary.usesReference(originalValue)) {
        return line();
      }

      const [reference] = dictionary.getReferences(originalValue);

      // Include fallback value only for primitive and semantic tokens, not component tokens
      const isComponentToken = token.path[0] === "component";

      return line(
        isComponentToken
          ? `var(--${prefix}${reference.name})`
          : `var(--${prefix}${reference.name}, ${reference.value})`,
      );
    }),

    "}",
  ].join("\n");
};
