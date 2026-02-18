import * as React from 'react';

import get from 'lodash/get';
import PropTypes from 'prop-types';

import {composeTheme, deepMerge} from '../next/utils';
import {isObject} from '../next/utils';

export type Theme = Record<string, any>;
export type ThemeObject = {
  theme?: Theme;
  part: Function;
  extend: Function;
};

export type ThemeContextProps = {theme?: Theme};
export const ThemeContext = {theme: PropTypes.object};

const flatten = (...path: string[]) =>
  Array.isArray(path) ? path.join('.') : path;
// const defaultTheme = composeTheme(styles)

const getTheme = (
  context: any,
  defaultTheme: ThemeContextProps,
  ...currentPath: string[]
): ThemeObject => {
  const {theme} = context;
  const basePath = flatten(...currentPath);
  if (!basePath) {
    return {
      theme: theme,
      part: (...path: any) =>
        get(theme, flatten(...path)) ?? get(defaultTheme, flatten(...path)),
      extend: (...path: any) =>
        getTheme(context, defaultTheme, flatten(...path)),
    };
  }
  return {
    theme: get(theme, basePath) || get(defaultTheme, basePath),
    part: (...path: any) =>
      get(theme, flatten(basePath, ...path)) ??
      get(defaultTheme, flatten(basePath, ...path)),
    extend: (...path: any) =>
      getTheme(context, defaultTheme, flatten(basePath, ...path)),
  };
};

export const getThemeFrom = (
  context: any,
  baseTheme: Theme,
  ...path: string[]
): ThemeObject => {
  return getTheme(context, baseTheme, ...path);
};

export const updateThemeParts = (
  theme: Theme,
  replacements: Record<any, any>,
): Theme => {
  const updatedTheme: Theme = {};
  if (theme && isObject(theme)) {
    Object.keys(theme).forEach((component) => {
      if (isObject(theme[component])) {
        updatedTheme[component] = updateThemeParts(
          theme[component],
          replacements,
        );
      } else {
        updatedTheme[component] =
          theme[component] in replacements
            ? replacements[theme[component]]
            : theme[component];
      }
    });
  }
  return updatedTheme;
};

export type ThemeProviderProps = {
  theme: Theme;
  children: React.ReactNode;
};
/**
 * @deprecated
 */
export default class ThemeProvider extends React.Component<ThemeProviderProps> {
  static childContextTypes = {
    theme: PropTypes.object,
  };
  static contextTypes = ThemeContext;

  getChildContext() {
    const theme = this.context;
    return {
      theme: composeTheme(
        theme ? deepMerge(theme, this.props.theme) : this.props.theme,
      ),
    };
  }
  render() {
    return this.props.children;
  }
}
