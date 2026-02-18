import * as React from 'react';
import {TextProps} from 'react-native';

import {removeChildren} from '../next/utils';
import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import BaseButton, {BaseButtonExternalSizeProps} from './base/button';
import {composed as defaultTheme} from './theme';

export type TertiaryButtonProps = Omit<
  BaseButtonExternalSizeProps,
  'icon' | 'iconRight'
> & {
  textProps?: TextProps;
};

/**
 * @deprecated: use <Button variant="tertiary" .../> instead
 */
export default class TertiaryButton extends React.Component<TertiaryButtonProps> {
  static contextTypes = ThemeContext;
  static displayName = 'TertiaryButton';
  render() {
    const {size, children, ...props} = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      `buttons.tertiary${
        size === 'medium' ? 'Medium' : size === 'large' ? 'Large' : 'Small'
      }`,
    );

    return (
      <BaseButton theme={theme} {...removeChildren(props)}>
        {children}
      </BaseButton>
    );
  }
}
