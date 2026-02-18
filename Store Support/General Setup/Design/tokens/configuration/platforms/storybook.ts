import { Platform, TransformedToken } from "style-dictionary";

import PlatformOptions from "../types/platformOptions";

const storybookPlatformConfig = ({ buildPath }: PlatformOptions): Platform => ({
  buildPath,
  files: [
    {
      destination: "primitive.stories.js",
      filter: (prop) => {
        return prop.filePath.startsWith("src/primitive");
      },
      format: "storybook",
      options: {
        group: (token: TransformedToken) => {
          return token.path[1];
        },
        storybookTitle: "Primitive",
      },
    },
    {
      destination: "semantic.stories.js",
      filter: (prop) => {
        return (
          prop.filePath.startsWith("src/semantic") &&
          !prop.filePath.startsWith("src/semantic/icon")
        );
      },
      format: "storybook",
      options: {
        group: (token: TransformedToken) => {
          return token.path[1];
        },
        storybookTitle: "Semantic",
      },
    },
    {
      destination: "components.stories.js",
      filter: (prop) => {
        return prop.filePath.startsWith("src/components");
      },
      format: "storybook",
      options: {
        group: (token: TransformedToken) => {
          return token.path[1];
        },
        storybookTitle: "Components",
      },
    },
  ],
  transforms: [
    "alignment/web",
    "attribute/cti",
    "elevation/web",
    "name/cti/kebab",
    "pxSize/web",
    "text/wrap/web",
    "width/toPercent",
    "time/seconds",
  ],
});

export default storybookPlatformConfig;
