import * as _ from "lodash";
import { File, Platform, TransformedToken } from "style-dictionary";

import PlatformOptions from "../types/platformOptions";

const jsPlatformConfig = ({
  buildPath,
  components,
  isMega,
}: PlatformOptions): Platform => {
  const transforms = [
    "alignment/web",
    "attribute/cti",
    "elevation/web",
    "name/custom/camel",
    "pxSize/web",
    "text/wrap/web",
    "width/toPercent",
    "font/family/web",
  ];

  if (isMega) {
    transforms.unshift("mega");
  }

  return {
    transforms,
    buildPath,
    files: [
      {
        destination: "primitive.esm.js",
        filter(prop) {
          return prop.filePath.startsWith("src/primitive");
        },
        format: "javascript/es6/custom",
      },
      {
        destination: "primitive.d.ts",
        filter(prop) {
          return prop.filePath.startsWith("src/primitive");
        },
        format: "typescript/es6-declarations/custom",
        options: {
          outputLiteralTypes: true,
        },
      },
      {
        destination: "primitive.js",
        filter(prop) {
          return prop.filePath.startsWith("src/primitive");
        },
        format: "javascript/module-flat/custom",
      },
      {
        destination: "semantic.esm.js",
        filter(prop) {
          return (
            prop.filePath.startsWith("src/semantic") &&
            !prop.filePath.startsWith("src/semantic/icon")
          );
        },
        format: "javascript/es6/custom",
      },
      {
        destination: "semantic.d.ts",
        filter(prop) {
          return (
            prop.filePath.startsWith("src/semantic") &&
            !prop.filePath.startsWith("src/semantic/icon")
          );
        },
        format: "typescript/es6-declarations/custom",
        options: {
          outputLiteralTypes: true,
        },
      },
      {
        destination: "semantic.js",
        filter(prop) {
          return (
            prop.filePath.startsWith("src/semantic") &&
            !prop.filePath.startsWith("src/semantic/icon")
          );
        },
        format: "javascript/module-flat/custom",
      },
      {
        destination: "icons/semantic.esm.js",
        filter(prop) {
          return prop.filePath.startsWith("src/semantic/icon");
        },
        format: "javascript/es6/custom/icon",
        options: {
          isMega,
        },
      },
      {
        destination: "icons/semantic.d.ts",
        filter(prop) {
          return prop.filePath.startsWith("src/semantic/icon");
        },
        format: "typescript/es6-declarations/custom/icon",
        options: {
          isMega,
        },
      },
      {
        destination: "icons/semantic.js",
        filter(prop) {
          return prop.filePath.startsWith("src/semantic/icon");
        },
        format: "javascript/module-flat/custom/icon",
        options: {
          isMega,
        },
      },

      ...components.reduce<File[]>((accum, name) => {
        const filter = (token: TransformedToken) => {
          return (
            token.path[0] === "component" && token.path[1] === _.camelCase(name)
          );
        };

        return accum.concat([
          {
            destination: `components/${name}.esm.js`,
            filter,
            format: "javascript/es6/custom",
          },
          {
            destination: `components/${name}.d.ts`,
            filter,
            format: "typescript/es6-declarations/custom",
            options: {
              outputLiteralTypes: true,
            },
          },
          {
            destination: `components/${name}.js`,
            filter,
            format: "javascript/module-flat/custom",
          },
        ]);
      }, []),
    ],
  };
};

export default jsPlatformConfig;
