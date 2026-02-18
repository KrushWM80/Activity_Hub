import * as React from 'react';
import {AccessibilityRole, Platform} from 'react-native';

import moment from 'moment';

// DO NOT USE THIS! See CEEMP-2787
// const isAndroid: boolean = Platform.OS === 'android';

const isObject = (obj: Object) => obj === Object(obj);
const isUndefined = (obj: any) => obj === void 0; // eslint-disable-line no-void

const removeChildren = (props: any) => {
  const {children, ...rest} = props;
  return rest;
};

const findKey = (object: {[key: string]: any}, value: any) => {
  return Object.keys(object).find((key) => object[key] === value);
};

const capitalize = (string: string) =>
  string.charAt(0).toUpperCase() + string.slice(1);

/**
 * Checks if an element's name ends with the given substring
 * @param element React.ReactNode
 * @returns boolean
 */
const checkElement = (element: React.ReactNode, subString: string) => {
  if (!React.isValidElement(element)) {
    return false;
  }

  /* element?.type?.toString() not returning the expected value when its running as ios release build
   returning function with single char
   for Ex:
    1) <Icons.StarIcon /> the it returning function o(a0){} expected function StarIcon(...)
    2) <Icons.PlusIcon /> the it returning function I(a0){} expected function PlusIcon(...)
    React.ReactNode.type or valueOf is not working as expected in ios release build only
   */
  const elementName = /^function\s+([\w$]+)\s*\(/.exec(
    element?.type?.toString(),
  );
  if (!elementName) {
    return false;
  } else if (elementName?.[1].endsWith(subString) === false) {
    return false;
  } else {
    return true;
  }
};

/**
 * Sleep for the given nr of milliseconds
 * @param ms - number of ms
 * @returns a new Promise
 */
const delay = (ms: number | undefined) => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};

/**
 * Silences accessibilityRole when rendered by Styleguidist
 * @param role
 * @returns role or undefined
 */
const a11yRole = (role: AccessibilityRole): AccessibilityRole | undefined => {
  return !process.env.STYLEGUIDIST_ENV ? role : undefined;
};

const loremIpsum = (repeat: number) => {
  const lIpsum =
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.';
  const result = [...Array(repeat).keys()].map(() => {
    return lIpsum;
  });
  return result.join('');
};

const calculatePercentageOf = (total: number, percentage = 0) => {
  if (total !== 0 && percentage !== 0) {
    return (percentage * total) / 100;
  }
  return 0;
};

//1rem = 16 pixel
const convertRemToPixel = (rem: string) => {
  const remValue = parseFloat(rem);
  return Math.round(remValue * 16);
};
/**
 * The function `convertStringToMS` converts a string representing a number to milliseconds by
 * multiplying it by 1000.
 * @param {string} value - The `convertStringToMS` function takes a string value as input and converts
 * it to milliseconds.
 * @returns The function `convertStringToMS` returns the value of the input string converted to
 * milliseconds.
 */
const convertStringToMS = (value: string) => {
  const convertedValue = parseFloat(value) * 1000;
  return convertedValue;
};

const convertDateToString = (
  value: Date | undefined,
  dateFormat = 'MM / DD / YYYY',
) => {
  if (value) {
    return moment(value).format(dateFormat);
  }
  return '';
};

/**
 * The function calculates the percentage value of a given device height considering additional layout
 * heights and padding.
 * @param {number} deviceHeight - The `deviceHeight` parameter represents the height of the device
 * screen in pixels.
 * @param {string | number} percentage - The `percentage` parameter can be either a string representing
 * a percentage value (e.g., '50%') or a number representing a specific value.
 * @param {number} [actionsLayoutHeight=0] - The `actionsLayoutHeight` parameter represents the height
 * of any actions or buttons layout that may be present in the container. It is used in the calculation
 * to adjust the final percentage value based on the layout height.
 * @param {number} BSContentPadding - BSContentPadding is the padding value for the Bottom Sheet
 * content. It is used in the calculation to determine the final percentage value for the Bottom Sheet
 * container.
 * @returns The function `calculateBSContainerPercentageValue` returns a calculated value based on the
 * input parameters. If the `percentage` parameter is a string, it calculates a percentage value based
 * on the `deviceHeight`, subtracts `actionsLayoutHeight` and `BSContentPadding`, and returns the
 * result. If the `percentage` parameter is a number, it simply subtracts `actionsLayoutHeight` from
 * the
 */
const calculateBSContainerPercentageValue = (
  deviceHeight: number,
  percentage: string | number,
  BSContentPadding: number,
  actionsLayoutHeight: number = 0,
) => {
  if (typeof percentage === 'string') {
    const percentageValue = parseFloat(percentage);
    return (
      deviceHeight * (percentageValue / 100.0) -
      actionsLayoutHeight -
      BSContentPadding
    );
  } else {
    return percentage - actionsLayoutHeight;
  }
};
// TODO: Refactor getPadding logic after upgrading react-native to >= 0.76 (CEEMP-3802)
/**
 * Returns the paddingBottom style based on the RN version.
 * For RN versions >= 0.76, it returns 0 for Android and bottomHeight for iOS.
 * For older versions, it returns bottomHeight for both platforms.
 */
const getBSPaddingBottomBasedOnRNVersion = (
  RNVersion: string,
  bottomHeight: number,
) => {
  // Example: compare major version number of RNVersion
  const majorVersion = parseInt(RNVersion.split('.')[1], 10);
  if (majorVersion >= 76) {
    return {paddingBottom: Platform.OS === 'android' ? 0 : bottomHeight};
  } else {
    return {paddingBottom: bottomHeight};
  }
};

export {
  isObject,
  isUndefined,
  removeChildren,
  findKey,
  capitalize,
  checkElement,
  delay,
  a11yRole,
  loremIpsum,
  calculatePercentageOf,
  convertRemToPixel,
  convertDateToString,
  convertStringToMS,
  calculateBSContainerPercentageValue,
  getBSPaddingBottomBasedOnRNVersion,
};
