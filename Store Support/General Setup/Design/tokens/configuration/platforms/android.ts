import * as _ from "lodash";
import { File, Platform, TransformedToken } from "style-dictionary";
import PlatformOptions from "../types/platformOptions";

interface AndroidPlatformFile extends File {
  format: string;
  resourceType?: string;
}

interface AndroidPlatform extends Platform {
  files: Array<AndroidPlatformFile | File>;
}

const androidPlatformConfig = ({
  buildPath,
  components,
}: PlatformOptions): AndroidPlatform => ({
  buildPath,
  files: [
    {
      destination: "ld_border_radius.xml",
      filter: {
        attributes: {
          category: "border",
        },
      },
      resourceType: "dimen",
      format: "android/resources",
    },
    {
      destination: "ld_color.xml",
      format: "android/colors",
    },
    {
      destination: "ld_duration.xml",
      filter: {
        attributes: {
          category: "duration",
        },
      },
      format: "android/resources",
      resourceType: "integer",
    },
    {
      destination: "ld_elevation.xml",
      filter: {
        attributes: {
          category: "elevation",
        },
      },
      format: "android/resources",
      resourceType: "dimen",
    },
    {
      destination: "ld_font.xml",
      filter: {
        attributes: {
          category: "font",
        },
      },
      format: "android/customResources",
    },
    {
      destination: "ld_size.xml",
      format: "android/dimens",
    },
    {
      destination: "ld_timing.xml",
      filter: {
        attributes: {
          category: "timing",
        },
      },
      format: "android/resources",
    },
    {
      destination: "ld_zIndex.xml",
      filter: {
        attributes: {
          category: "zIndex",
        },
      },
      format: "android/resources",
      resourceType: "integer",
    },
    ...components.map((name) => {
      return {
        destination: `ld_${_.snakeCase(name)}.xml`,
        filter(prop: TransformedToken) {
          return prop.filePath.startsWith(`src/components/${name}/`);
        },
        format: "android/customResources",
        options: {
          outputReferences: true,
        },
      };
    }),
  ],

  prefix: "ld",

  transforms: [
    "attribute/cti",
    "name/cti/snake",
    "color/hex8android",
    "pxSize/android",
    "duration/android",
    "elevation/android",
    "font/family/android",
    "iconName/android",
    "iconSize/android",
    "text/wrap/android",
    "width/toPercent",
  ],
});

export default androidPlatformConfig;
