import StyleDictionary from "style-dictionary";
import { alias } from "./alias";
import { alignment } from "./alignment";
import { cti } from "./cti";
import { duration } from "./duration";
import { elevation } from "./elevation";
import { font } from "./font";
import { icon } from "./icon";
import { mega } from "./mega";
import { name } from "./name";
import { pxSize } from "./pxSize";
import { text } from "./text";
import { timing } from "./timing";
import { width } from "./width";

/**
 * Custom transforms.
 *
 * @see {@link https://amzn.github.io/style-dictionary/#/transforms?id=defining-custom-transforms}
 */
export const transform: StyleDictionary.Core["transform"] = {
  ...alias,
  ...alignment,
  ...cti,
  ...duration,
  ...elevation,
  ...font,
  ...icon,
  ...mega,
  ...name,
  ...pxSize,
  ...text,
  ...timing,
  ...width,
};
