import {AccessibilityRole} from 'react-native';

export const removeChildren = (props: any) => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const {children, ...rest} = props;
  return rest;
};

export const capitalize = (string: string) =>
  string.charAt(0).toUpperCase() + string.slice(1);

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

const lum = ({r, g, b}: {r: number; g: number; b: number}) => {
  var a = [r, g, b].map(function (v) {
    v /= 255;
    return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
  });
  return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
};

/** Determines the contrast between two colors. */
export const colorContrast = (color1: string, color2: string) => {
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

/** Select the best contrasting color between two colors. */
export const contrastColors = (
  color: string,
  lightColor = '#ffffff',
  darkColor = '#000000',
) =>
  colorContrast(color, darkColor) >= colorContrast(color, lightColor)
    ? darkColor
    : lightColor;

/**
 * Silences accessibilityRole when rendered by Styleguidist
 * @param role
 * @returns role or undefined
 */
export const a11yRole = (
  role: AccessibilityRole,
): AccessibilityRole | undefined => {
  return !process.env.STYLEGUIDIST_ENV ? role : undefined;
};
