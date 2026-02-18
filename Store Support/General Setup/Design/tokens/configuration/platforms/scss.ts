import * as _ from "lodash";
import { Platform, TransformedToken } from "style-dictionary";

import PlatformOptions from "../types/platformOptions";

const scssPlatformConfig = ({
  buildPath,
  components,
  isMega,
}: PlatformOptions): Platform => {
  const transforms = [
    "alignment/web",
    "alias/sass",
    "attribute/cti",
    "elevation/web",
    "name/custom/kebab",
    "pxSize/web",
    "text/wrap/web",
    "width/toPercent",
    "time/seconds",
  ];

  if (isMega) {
    transforms.unshift("mega");
  }

  return {
    transforms,
    buildPath,
    files: [
      {
        destination: "_primitive.scss",
        filter: (prop) => {
          return prop.filePath.startsWith("src/primitive");
        },
        format: "scss/variables/custom",
      },
      {
        destination: "_semantic.scss",
        filter: (prop) => {
          return (
            prop.filePath.startsWith("src/semantic") &&
            !prop.filePath.startsWith("src/semantic/icon")
          );
        },
        format: "scss/variables/custom",
      },

      ...components.map((name) => {
        return {
          destination: `components/_${name}.scss`,
          filter(token: TransformedToken) {
            return (
              token.path[0] === "component" &&
              token.path[1] === _.camelCase(name)
            );
          },
          format: "scss/variables/custom",
        };
      }),
    ],
  };
};

export default scssPlatformConfig;
