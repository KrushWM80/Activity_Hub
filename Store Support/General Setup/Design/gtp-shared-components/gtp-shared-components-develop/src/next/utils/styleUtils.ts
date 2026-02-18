import flattenDeep from 'lodash/flattenDeep';

import {isObject, isUndefined} from './commonUtils';

type Theme = Record<string, any>;

const deepMerge = (obj1: Theme, obj2: Theme) => {
  if (
    !isObject(obj1) ||
    !isObject(obj2) ||
    Array.isArray(obj1) ||
    Array.isArray(obj2)
  ) {
    return isUndefined(obj2) ? obj1 : obj2;
  }
  const keys1 = Object.keys(obj1);
  const keys2 = Object.keys(obj2);
  const keys = [...new Set([...keys1, ...keys2])] || [];
  const built = {};
  keys.forEach((key) => {
    Object.assign(built, {[key]: deepMerge(obj1[key], obj2[key])});
  });
  return built;
};

const createCompositeStyles = (styles: Theme) => {
  if (styles && isObject(styles)) {
    Object.keys(styles).forEach((component) => {
      if (styles[component].default) {
        const states = Object.keys(styles[component]);
        states.forEach((state) => {
          if (state !== 'default' && state !== 'static') {
            styles[component][state] = deepMerge(
              styles[component].default,
              styles[component][state],
            );
          }
        });
      }
    });
  }
  return styles;
};

const composeTheme = (theme: Theme) => {
  const composedTheme: Theme = {};
  if (theme && isObject(theme)) {
    Object.keys(theme).forEach((component) => {
      composedTheme[component] = createCompositeStyles(theme[component]);
    });
  }
  return composedTheme;
};

const mergeStyles = (...styles: Array<any>): any => {
  if (!styles.length) {
    return;
  }

  const flatStyles = flattenDeep(styles);
  if (flatStyles.length === 1) {
    return flatStyles[0];
  }

  const allStyles: Array<any> = [];
  let mergedStyles = {};

  flatStyles.forEach((style) => {
    if (style) {
      if (isObject(style)) {
        mergedStyles = {...mergedStyles, ...style};
      } else {
        allStyles.push(style);
      }
    }
  });

  if (allStyles.length > 0) {
    if (flatStyles.length > allStyles.length) {
      return [...allStyles, mergedStyles];
    }
    return allStyles;
  }
  if (flatStyles.length) {
    return mergedStyles;
  }
};

const interpolatable = [
  'color',
  'backgroundColor',
  'fontSize',
  'left',
  'right',
  'top',
  'bottom',
  'padding',
  'paddingVertical',
  'paddingHorizontal',
  'paddingLeft',
  'paddingRight',
  'paddingTop',
  'paddingBottom',
  'margin',
  'marginVertical',
  'marginHorizontal',
  'marginLeft',
  'marginRight',
  'marginTop',
  'marginBottom',
  'borderColor',
  'borderWidth',
  'borderLeftWidth',
  'borderRightWidth',
  'borderTopWidth',
  'borderBottomWidth',
  'opacity',
  'elevation',
  'tintColor',
];

const interpolateStyles = (interpolater: any, from: any, to: any) => {
  const interpolated: Record<string, any> = {};
  const cleaned = {...from};

  if (!from || !to) {
    return {
      cleaned,
      interpolated,
    };
  }

  interpolatable.forEach((prop) => {
    if (
      (from.hasOwnProperty(prop) || to.hasOwnProperty(prop)) &&
      from[prop] !== to[prop]
    ) {
      const fromHasProp = from.hasOwnProperty(prop);
      const toHasProp = to.hasOwnProperty(prop);
      if (!fromHasProp || !toHasProp) {
        if (process.env.NODE_ENV === 'development') {
          // eslint-disable-next-line no-console
          console.warn(
            `Cannot interpolate property "${prop}" from ${from[prop]} to ${to[prop]}.\n\nMissing property in style object`,
            fromHasProp ? to : from,
          );
        }
      } else if (
        (from.hasOwnProperty(prop) || to.hasOwnProperty(prop)) &&
        from[prop] !== to[prop]
      ) {
        interpolated[prop] = interpolater.interpolate({
          inputRange: [0, 1],
          outputRange: [from[prop], to[prop]],
        });
        delete cleaned[prop];
      }
    }
  });

  return {
    interpolated,
    cleaned,
  };
};

export {
  deepMerge,
  createCompositeStyles,
  composeTheme,
  mergeStyles,
  interpolateStyles,
};
