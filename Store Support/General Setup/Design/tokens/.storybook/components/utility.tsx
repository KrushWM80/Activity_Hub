import { kebabCase } from "lodash";

export interface Token {
  comment?: string;
  darkValue?: string;
  darkValueReference?: {
    name: string;
    path: string[];
  };
  name: string;
  path: string[];
  themeable?: boolean;
  value: string;
  valueReference?: {
    name: string;
    path: string[];
  };
}

export type Platform = "css" | "js" | "json" | "scss";

const sanitizePath = (path: string[]): string[] =>
  path.filter((piece) => piece !== "_");

export const platformTokenName: Record<
  Platform,
  (token: { path: string[] }) => string
> = {
  css(token) {
    return `--ld-${kebabCase(sanitizePath(token.path).join(" "))}`;
  },

  js(token) {
    return sanitizePath(token.path)
      .map((piece, index) =>
        index === 0 ? piece : `${piece[0].toUpperCase()}${piece.slice(1)}`,
      )
      .join("");
  },

  json(token) {
    return token.path.join(".");
  },

  scss(token) {
    return `$${sanitizePath(token.path)
      .join("-")
      .replace(
        /([a-z])([A-Z])/g,
        (_substring, a, b) => `${a}-${b.toLowerCase()}`,
      )}`;
  },
};
