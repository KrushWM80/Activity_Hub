import * as _ from "lodash";
import { NameTransform } from "style-dictionary/types/Transform";

const createTransformer =
  (toCase: (value: string) => string): NameTransform["transformer"] =>
  (token, options) => {
    const path = token.path.slice(
      token.path[0] === "component" ? 2 : 1,
      token.path.length,
    );

    return toCase([options?.prefix, ...path].join(" "));
  };

export const name: Record<string, NameTransform> = {
  /**
   * A camelCase name transformer that is similar to style-dictionary's built-in
   * `name/ti/camel`:
   *
   * - category and type for component tokens
   * - category for non-component tokens
   *
   * {@see https://amzn.github.io/style-dictionary/#/transforms?id=nameticamel}
   */
  "name/custom/camel": {
    transformer: createTransformer(_.camelCase),

    type: "name",
  },

  /**
   * A kebab-case name transformer that is similar to style-dictionary's built-in
   * `name/ti/camel`:
   *
   * - category and type for component tokens
   * - category for non-component tokens
   *
   * {@see https://amzn.github.io/style-dictionary/#/transforms?id=nameticamel}
   */
  "name/custom/kebab": {
    transformer: createTransformer(_.kebabCase),

    type: "name",
  },
};
