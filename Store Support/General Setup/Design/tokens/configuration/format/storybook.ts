import {
  Dictionary,
  Formatter,
  TransformedToken,
  formatHelpers,
} from "style-dictionary";
import path from "node:path";
import _ from "lodash";

const rootDirname = path.resolve(__dirname, "../../");

interface MappedToken {
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

/* eslint-disable @typescript-eslint/no-explicit-any */
const getReference = (
  value: TransformedToken,
  unwrap: (value: any) => any,
  dictionary: Dictionary,
) => {
  if (!dictionary.usesReference(unwrap(value))) {
    return;
  }

  const references = dictionary.getReferences(unwrap(value));

  /**
   * @note This is a sanity check to ensure style-dictionary behaves as expected.
   */
  if (references.length > 1 || !references[0]) {
    throw new Error("Expected a single reference from style-dictionary");
  }

  return {
    name: references[0].name,
    path: references[0].path,
  };
};
/* eslint-enable @typescript-eslint/no-explicit-any */

const getMappedToken = (token: TransformedToken, dictionary: Dictionary) => {
  const mappedToken: MappedToken = {
    name: token.name,
    path: token.path,
    value: token.value,
    valueReference: getReference(
      token,
      (value) => value.original.value,
      dictionary,
    ),
  };

  if (token.comment) {
    mappedToken.comment = token.comment;
  }
  if (token.darkValue) {
    mappedToken.darkValue = token.darkValue;
    mappedToken.darkValueReference = getReference(
      token,
      (value) => value.original.darkValue,
      dictionary,
    );
  }
  if ("themeable" in token) {
    mappedToken.themeable = token.themeable;
  }

  return mappedToken;
};

/**
 * Emits Storybook stories.
 */
export const storybookFormatter: Formatter = (args) => {
  const { dictionary, file, options, platform } = args;
  const { group, storybookTitle } = options;

  const groupedTokens = new Map<string, MappedToken[]>();

  dictionary.allTokens.forEach((token) => {
    const key = group(token);
    const mappedToken = getMappedToken(token, dictionary);

    if (groupedTokens.has(key)) {
      groupedTokens.get(key)!.push(mappedToken);
    } else {
      groupedTokens.set(key, [mappedToken]);
    }
  });

  const relative = (filename: string) =>
    path.relative(
      path.join(rootDirname, platform.buildPath!),
      path.join(rootDirname, filename),
    );

  return `${formatHelpers.fileHeader({ file, commentStyle: "short" })}
import { TokenTable } from "${relative(".storybook/components/TokenTable")}";
import "${relative("dist/css/light/regular/primitive.css")}";
import "${relative("dist/css/light/regular/semantic.css")}";
import "${relative("dist/css/dark/regular/primitive.css")}";
import "${relative("dist/css/dark/regular/semantic.css")}";

export default {
  component: TokenTable,
  title: "${storybookTitle}",
};

${Array.from(groupedTokens.entries())
  .map(([name, tokens]) => {
    return `export const ${_.camelCase("component " + name)} = {
  args: {
    tokens: ${JSON.stringify(tokens, null, 2)}
  },
  name: "${_.startCase(name)}",
};`;
  })
  .join("\n")}`;
};
