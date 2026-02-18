import * as _ from "lodash";
import { Platform, TransformedToken } from "style-dictionary";

import PlatformOptions from "../types/platformOptions";

const cssPlatformConfig = ({
  buildPath,
  components,
  isMega,
  isDarkMode,
}: PlatformOptions): Platform => {
  const transforms = [
    "alignment/web",
    "attribute/cti",
    "elevation/web",
    "name/cti/kebab",
    "pxSize/web",
    "text/wrap/web",
    "width/toPercent",
    "time/seconds",
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
        destination: "primitive.css",
        filter: (prop) => {
          return prop.filePath.startsWith("src/primitive");
        },
        format: "css/variables/custom",
        options: {
          isDarkMode,
          selector: isDarkMode ? ".dark" : undefined,
        },
      },

      {
        destination: "semantic.css",
        filter: (prop) => {
          return (
            prop.filePath.startsWith("src/semantic") &&
            !prop.filePath.startsWith("src/semantic/icon")
          );
        },
        format: "css/variables/custom",
        options: {
          isDarkMode,
          selector: isDarkMode ? ".dark" : undefined,
        },
      },

      ...components.map((name) => {
        return {
          destination: `components/${name}.css`,
          filter(token: TransformedToken) {
            return (
              token.path[0] === "component" &&
              token.path[1] === _.camelCase(name)
            );
          },
          format: "css/variables/custom",
          options: {
            isDarkMode,
            selector: isDarkMode ? ".dark" : undefined,
          },
        };
      }),
    ],
  };
};

export default cssPlatformConfig;
