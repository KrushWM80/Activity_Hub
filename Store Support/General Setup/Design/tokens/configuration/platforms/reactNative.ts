import * as _ from "lodash";
import { File, Platform, TransformedToken } from "style-dictionary";

import PlatformOptions from "../types/platformOptions";

const reactNativePlatformConfig = ({
  buildPath,
  components,
  isDarkMode,
  isMega,
}: PlatformOptions): Platform => {
  const transforms = [
    "attribute/cti",
    "name/custom/camel",
    "pxSize/reactnative",
    "width/toPercent",
  ];

  if (isMega) {
    transforms.unshift("mega");
  }

  return {
    transforms,
    buildPath,
    files: [
      {
        destination: "primitive.js",
        filter(prop) {
          return prop.filePath.startsWith("src/primitive");
        },
        format: "javascript/module-flat/custom-react-native",
        options: { isDarkMode },
      },
      {
        destination: "primitive.d.ts",
        filter: (prop) => {
          return prop.filePath.startsWith("src/primitive");
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
        format: "javascript/module-flat/custom-react-native",
        options: { isDarkMode },
      },
      {
        destination: "semantic.d.ts",
        filter: (prop) => {
          return (
            prop.filePath.startsWith("src/semantic") &&
            !prop.filePath.startsWith("src/semantic/icon")
          );
        },
        format: "typescript/es6-declarations/custom",
        options: {
          outputLiteralTypes: true,
          isDarkMode,
        },
      },

      ...components.reduce<File[]>((accum, name) => {
        const filter = (token: TransformedToken) => {
          return (
            token.path[0] === "component" && token.path[1] === _.camelCase(name)
          );
        };

        return accum.concat(
          {
            destination: `components/${name}.js`,
            filter,
            format: "javascript/module-flat/custom-react-native",
            options: { isDarkMode },
          },
          {
            destination: `components/${name}.d.ts`,
            filter,
            format: "typescript/es6-declarations/custom",
            options: {
              outputLiteralTypes: true,
            },
          },
        );
      }, []),
    ],
  };
};

export default reactNativePlatformConfig;
