import {Color, ColorNumber, colors} from './colors';

/**
 * Converts a hexadecimal color code to its RGB representation.
 *
 * @param {string} hex - The hexadecimal color code to convert.
 * @return {Object} An object containing the RGB values of the color code.
 */
const hexToRgb = (hex: string) => {
  // Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
  var shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
  hex = hex.replace(shorthandRegex, function (m, r, g, b) {
    return r + r + g + g + b + b;
  });

  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result
    ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16),
      }
    : null;
};

/**
 * Calculates the relative luminance of a color.
 *
 * @param {Object} rgb - An object containing the red, green, and blue color values.
 * @param {number} rgb.r - The red color value.
 * @param {number} rgb.g - The green color value.
 * @param {number} rgb.b - The blue color value.
 * @return {number} The relative luminance of the color.
 */
const lum = ({r, g, b}: {r: number; g: number; b: number}) => {
  var a = [r, g, b].map(function (v) {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
};

/**
 * Calculates the contrast ratio between two colors.
 *
 * @param {string} color1 - The first color in hexadecimal format.
 * @param {string} color2 - The second color in hexadecimal format.
 * @return {number} The contrast ratio between the two colors.
 */
const colorContrast = (color1: string, color2: string) => {
  const rgb1 = hexToRgb(color1);
  const rgb2 = hexToRgb(color2);
  if (rgb1 && rgb2) {
    const lum1 = lum(rgb1);
    const lum2 = lum(rgb2);
    return (Math.max(lum1, lum2) + 0.05) / (Math.min(lum1, lum2) + 0.05);
  } else {
    return 0;
  }
};

/**
 * Calculates the contrast colors based on a given color.
 *
 * @param {string} color - The color to calculate contrast colors for.
 * @param {string} lightColor - The light color to use for contrast calculation. Defaults to '#ffffff'.
 * @param {string} darkColor - The dark color to use for contrast calculation. Defaults to '#000000'.
 * @return {string} The contrast color that has the highest contrast ratio with the input color.
 */
const contrastColors = (
  color: string,
  lightColor = '#ffffff',
  darkColor = '#000000',
) =>
  colorContrast(color, darkColor) >= colorContrast(color, lightColor)
    ? darkColor
    : lightColor;

/**
 * Color matcher, it will match the given color string and return useful color code.
 *
 * @param {string} color - The color string to get the color value from listed color object.
 * @returns {string} The useful color code.
 */
const formatColor = (color: string) => {
  let colorNameVal = color.match(/[a-zA-Z]{3,}/g)?.toString() as Color;
  let colorCodeVal = color.match(/\d{1,}/g)?.toString() as ColorNumber;

  if (colorNameVal) {
    if (colorCodeVal) {
      return colors[colorNameVal][colorCodeVal];
    }
    return colors[colorNameVal];
  }
  return color;
};

export {contrastColors, colorContrast, formatColor};
