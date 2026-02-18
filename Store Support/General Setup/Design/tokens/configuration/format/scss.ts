import { Formatter, formatHelpers } from "style-dictionary";

/**
 * Emits SCSS token variables.
 *
 * This custom formatter is based on style-dictionary's "scss/variables" format. It additionally
 * handles the `deprecated` token attribute.
 *
 * Original implementation: https://github.com/amzn/style-dictionary/blob/main/lib/common/formats.js#L140-L144
 */
export const customScssFormatter: Formatter = (args) => {
  const { dictionary, file } = args;

  const prefix = "ld";

  return [
    formatHelpers.fileHeader({ file, commentStyle: "short" }),

    ...dictionary.allTokens.map((token) => {
      const line = (value = token.value) => {
        const output = `$${token.name}: ${value}${
          token.themeable ? " !default" : ""
        };${token.comment ? ` // ${token.comment}` : ""}`;

        if (token.deprecated) {
          return `/// @deprecated ${token.deprecated.comment};
            ${output}`;
        }

        return output;
      };

      const [maybeReference] = dictionary.usesReference(token.original.value)
        ? dictionary.getReferences(token.original.value)
        : [];

      // If the token isn't themeable and it doesn't reference
      // a themeable token, use the hard-coded value
      if (!token.themeable && !maybeReference?.themeable) {
        return line();
      }

      // If the token isn't themeable and it references a themeable
      // value, use the custom property for the referenced token
      //
      // If the token is themeable, use it's custom property reference
      // Include the hard-coded value as a fallback for primitive and semantic tokens only
      const isComponentToken = token.path[0] === "component";

      return !token.themeable
        ? line(
            isComponentToken
              ? `var(--${prefix}-${maybeReference.path[0]}-${maybeReference.name})`
              : `var(--${prefix}-${maybeReference.path[0]}-${maybeReference.name}, ${maybeReference.value})`,
          )
        : line(
            isComponentToken
              ? `var(--${prefix}-${token.path[0]}-${token.name})`
              : `var(--${prefix}-${token.path[0]}-${token.name}, ${token.value})`,
          );
    }),
  ].join("\n");
};
