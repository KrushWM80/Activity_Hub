import * as _ from "lodash";
import { Platform, TransformedToken } from "style-dictionary";
import PlatformOptions from "../types/platformOptions";

const jsonPlatformConfig = ({
  buildPath,
  components,
  isMega,
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
  ];

  if (isMega) {
    transforms.unshift("mega");
  }

  return {
    transforms,
    buildPath,
    files: [
      {
        destination: "primitive.json",
        filter: (prop) => {
          return prop.filePath.startsWith("src/primitive");
        },
        format: "json",
      },
      {
        destination: "semantic.json",
        filter: (prop) => {
          return prop.filePath.startsWith("src/semantic");
        },
        format: "json",
      },

      ...components.map((name) => {
        return {
          destination: `components/${name}.json`,
          filter(token: TransformedToken) {
            return (
              token.path[0] === "component" &&
              token.path[1] === _.camelCase(name)
            );
          },
          format: "json",
        };
      }),
    ],
  };
};

export default jsonPlatformConfig;
