import * as React from 'react';
import {GestureResponderEvent, TextProps} from 'react-native';

import {removeChildren} from '../next/utils';
import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import BaseButton, {BaseButtonExternalSmallProps} from './base/button';
import {composed as defaultTheme} from './theme';

export type LinkButtonProps = Omit<
  BaseButtonExternalSmallProps,
  'icon' | 'iconRight'
> & {
  white?: boolean;
  textProps?: TextProps;
};

export type LinkProps =
  | {
      link?: false | null;
      onLinkPress?: false | null;
    }
  | {
      /** The text for this link */
      link: string;
      /** This link's press handler */
      onLinkPress: (event: GestureResponderEvent) => void;
    };

/**
 * @deprecated use Link instead
 */
export default class LinkButton extends React.Component<LinkButtonProps> {
  static contextTypes = ThemeContext;
  static displayName = 'LinkButton';
  render() {
    const {white, small, children, ...props} = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      `buttons.link${white ? 'White' : ''}${small ? 'Small' : ''}`,
    );

    return (
      <BaseButton theme={theme} {...removeChildren(props)}>
        {children}
      </BaseButton>
    );
  }
}
