import * as React from 'react';
import {ViewProps} from 'react-native';

import {Spinner} from '../../next/components/Spinner';
import {getThemeFrom, ThemeContext} from '../../theme/theme-provider';
import {composed as defaultTheme} from '../theme';

import BaseButton, {
  BaseButtonExternalSizeProps,
  BaseButtonExternalSmallProps,
  BaseButtonLoadingProps,
  BaseButtonTheme,
} from './button';

export type ThemedButtonProps = ViewProps &
  BaseButtonExternalSmallProps &
  BaseButtonExternalSizeProps &
  BaseButtonLoadingProps & {
    type: string;
    /** @ignore */
    iconNoMargin?: boolean;
  };

export type ThemedButtonTheme = BaseButtonTheme;
export type ThemedButtonLoadingProps = BaseButtonLoadingProps;
export type ThemedButtonExternalSmallProps = BaseButtonExternalSmallProps;
export type ThemedButtonExternalSizeProps = BaseButtonExternalSizeProps;

/**
 * @internal
 */
export default class ThemedButton extends React.Component<ThemedButtonProps> {
  static contextTypes = ThemeContext;

  render() {
    const {type, ...props} = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'buttons',
      type,
    ) as BaseButtonTheme;
    return (
      <BaseButton
        {...props}
        theme={theme}
        loadingIndicator={<Spinner size="small" />}
      />
    );
  }
}
