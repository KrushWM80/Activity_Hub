import * as _ from "lodash";
import fs from "fs";
import path from "path";
import styleDictionary, {
  Config as StyleDictionaryConfig,
  Formatter,
} from "style-dictionary";

import {
  customTypescriptFormatter,
  customTypescriptIconModuleFormatter,
  customEs6ModuleFormatter,
  customCommonJsModuleFormatter,
  customReactNativeCommonJsModuleFormatter,
  customScssFormatter,
  customCssFormatter,
  storybookFormatter,
  customEs6IconModuleFormatter,
  customCommonJsIconModuleFormatter,
} from "./format";
import { transform } from "./transform";
import PlatformOptions from "./types/platformOptions";
import androidPlatformConfig from "./platforms/android";
import cssPlatformConfig from "./platforms/css";
import iosPlatformConfig from "./platforms/ios";
import jsPlatformConfig from "./platforms/js";
import jsonPlatformConfig from "./platforms/json";
import reactNativePlatformConfig from "./platforms/reactNative";
import scssPlatformConfig from "./platforms/scss";
import storybookPlatformConfig from "./platforms/storybook";

const options: Omit<PlatformOptions, "buildPath"> = {
  components: fs.readdirSync(path.join(__dirname, "../src/components")),
  globals: [],
};

const configuration: StyleDictionaryConfig = {
  format: {
    /**
     * Customize the "android/resources" template to work with the token
     * structure, which doesn't strictly follow Style Dictionary's assumptions.
     *
     * @see {@link https://github.com/amzn/style-dictionary/blob/6724dd671d62ff37b203b6779831894d8769b7ae/lib/common/formats.js#L509-L540}
     *
     * @type {import("style-dictionary").Format["formatter"]}
     */
    "android/customResources": ({
      dictionary,
      file,
      options,
    }: Parameters<Formatter>[0]) => {
      const compiled = _.template(
        fs.readFileSync(
          path.join(__dirname, "format/templates/androidCustomResources.ejs"),
          "utf-8",
        ),
      );

      return compiled({
        dictionary,
        file,
        fileHeader: styleDictionary.formatHelpers.fileHeader,
        options,
      });
    },
    "typescript/es6-declarations/custom": customTypescriptFormatter,
    "typescript/es6-declarations/custom/icon":
      customTypescriptIconModuleFormatter,
    "javascript/es6/custom": customEs6ModuleFormatter,
    "javascript/es6/custom/icon": customEs6IconModuleFormatter,
    "javascript/module-flat/custom": customCommonJsModuleFormatter,
    "javascript/module-flat/custom/icon": customCommonJsIconModuleFormatter,
    "javascript/module-flat/custom-react-native":
      customReactNativeCommonJsModuleFormatter,
    "scss/variables/custom": customScssFormatter,
    "css/variables/custom": customCssFormatter,
    storybook: storybookFormatter,
  },

  transform,

  source: [
    "src/primitive/**/*.ts",
    "src/semantic/**/*.ts",
    "src/components/**/*.ts",
  ],

  platforms: {
    android: androidPlatformConfig({
      buildPath: path.join(__dirname, "../library/src/main/res/values/"),
      ...options,
    }),
    cssMegaDark: cssPlatformConfig({
      buildPath: "dist/css/dark/mega/",
      isDarkMode: true,
      isMega: true,
      ...options,
    }),
    cssMegaLight: cssPlatformConfig({
      buildPath: "dist/css/light/mega/",
      isMega: true,
      ...options,
    }),
    cssRegularDark: cssPlatformConfig({
      buildPath: "dist/css/dark/regular/",
      isDarkMode: true,
      ...options,
    }),
    cssRegularLight: cssPlatformConfig({
      buildPath: "dist/css/light/regular/",
      ...options,
    }),
    ios: iosPlatformConfig({
      buildPath: path.join(
        __dirname,
        "../Sources/LivingDesignTokens/generated/",
      ),
      ...options,
    }),
    jsMega: jsPlatformConfig({
      buildPath: "dist/js/light/mega/",
      isMega: true,
      ...options,
    }),
    jsRegular: jsPlatformConfig({
      buildPath: "dist/js/light/regular/",
      ...options,
    }),
    jsonMega: jsonPlatformConfig({
      buildPath: "dist/json/light/mega/",
      isMega: true,
      ...options,
    }),
    jsonRegular: jsonPlatformConfig({
      buildPath: "dist/json/light/regular/",
      ...options,
    }),
    reactNativeMegaDark: reactNativePlatformConfig({
      buildPath: "dist/react-native/dark/mega/",
      isDarkMode: true,
      isMega: true,
      ...options,
    }),
    reactNativeMegaLight: reactNativePlatformConfig({
      buildPath: "dist/react-native/light/mega/",
      isMega: true,
      ...options,
    }),
    reactNativeRegularDark: reactNativePlatformConfig({
      buildPath: "dist/react-native/dark/regular/",
      isDarkMode: true,
      ...options,
    }),
    reactNativeRegularLight: reactNativePlatformConfig({
      buildPath: "dist/react-native/light/regular/",
      ...options,
    }),
    scssMega: scssPlatformConfig({
      buildPath: "dist/scss/light/mega/",
      isMega: true,
      ...options,
    }),
    scssRegular: scssPlatformConfig({
      buildPath: "dist/scss/light/regular/",
      ...options,
    }),
    storybook: storybookPlatformConfig({
      buildPath: "dist/storybook/",
      ...options,
    }),
  },
};

export default configuration;
