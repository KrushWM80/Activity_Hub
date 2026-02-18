import { promises as fs } from "fs";
import path from "path";

const toPascalCase = (value: string) =>
  value.replace(/\b\w/g, (v) => v.toUpperCase()).replace(/ +/g, "");

module.exports = {
  extends: ["@commitlint/config-conventional"],
  /**
   * Customize commit scope rules:
   * @see {@link https://commitlint.js.org/#/reference-rules}
   */
  rules: {
    "scope-enum": async () => {
      const [components, primitive] = await Promise.all([
        fs.readdir(path.join(__dirname, "src/components/")),
        fs.readdir(path.join(__dirname, "src/primitive/")),
      ]);

      const componentScopes = components.map((name) =>
        name.replace(/\.experimental/, ""),
      );

      const primitiveScopes = primitive.map((name) => toPascalCase(name));

      return [
        2,
        "always",
        [
          // Modifications to ./configuration/platforms/
          "Android",
          "Ios",
          "ReactNative",
          "Web",

          // Modifications to ./configuration/transform/
          "Animation",
          "Transition",

          // Modifications to ./src/components/
          ...componentScopes,

          // Modifications to ./src/primitive/
          ...primitiveScopes,

          // Modifications to release
          "release",
        ],
      ];
    },
  },
};
