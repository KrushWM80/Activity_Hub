import path from "path";
import { Platform, TransformedToken } from "style-dictionary";
import PlatformOptions from "../types/platformOptions";
import toPascalCase from "../util/toPascalCase";

const iosPlatformConfig = ({
  buildPath,
  globals,
}: PlatformOptions): Platform => ({
  // @see {@link https://github.com/amzn/style-dictionary/blob/master/lib/common/transformGroups.js#L184}
  transforms: [
    "attribute/cti",
    "color/UIColorSwift",
    "pxSize/ios",
    "content/swift/literal",
    "asset/swift/literal",
    "font/family/ios",
    "duration/ios",
    "elevation/ios",
    "text/align/ios",
    "text/decoration/ios",
    "text/wrap/ios",
    "timing/ios",
    "width/toPercent",
  ],

  buildPath,

  files: [
    ...globals.map((name) => {
      const className = toPascalCase(`living design ${name}`);

      return {
        className,
        destination: path.join("globals", `${className}.swift`),
        format: "ios-swift/class.swift",
        filter(prop: TransformedToken) {
          return prop.filePath.startsWith(path.join("src/globals", name));
        },
      };
    }),
  ],
});

export default iosPlatformConfig;
