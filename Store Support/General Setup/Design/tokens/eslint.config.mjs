import globals from "globals";
import js from "@eslint/js";
import tseslint from "typescript-eslint";
import tsParser from "@typescript-eslint/parser";
import eslintPluginPrettierRecommended from "eslint-plugin-prettier/recommended";
import customRules from "./custom-eslint-rules/index.js";

export default tseslint.config(
  {
    ignores: ["**/dist"],
  },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  eslintPluginPrettierRecommended,
  {
    plugins: {
      "custom-rules": customRules,
    },

    languageOptions: {
      globals: {
        ...globals.node,
        ...globals.jest,
      },

      parser: tsParser,
      ecmaVersion: 11,
      sourceType: "commonjs",
    },

    rules: {
      curly: "error",

      quotes: [
        "error",
        "double",
        {
          avoidEscape: true,
        },
      ],
    },
  },
  {
    files: ["**/src/**/*.ts"],

    rules: {
      "custom-rules/double-newline-between-properties": "error",
    },
  },
);
