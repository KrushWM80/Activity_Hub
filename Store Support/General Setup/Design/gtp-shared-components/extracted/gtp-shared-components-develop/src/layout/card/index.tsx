import * as React from 'react';
import {StyleProp, View, ViewProps, ViewStyle} from 'react-native';

import {getThemeFrom, ThemeContext} from '../../theme/theme-provider';
import {composed as defaultTheme} from '../theme';

type ContentInsets = 'none' | 'tiny' | 'small' | 'normal';
type Roundness = 'small' | 'large';

export type SolidCardBaseProps = {
  type: 'solid';
  /** Card color */
  color: 'white' | 'blue';
  /** Card elevation - determines the size of the shadow. */
  elevation: 0 | 1 | 2 | 3;
  /** Content inset amount */
  contentInset?: ContentInsets;
  /** Corner roundness */
  roundness?: Roundness;
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
};

export type OutlineCardBaseProps = {
  type: 'outline';
  /** Card color */
  color: 'black' | 'gray' | 'blue';
  /** Content inset amount */
  contentInset?: ContentInsets;
  /** Corner roundness */
  roundness?: Roundness;
  elevation: undefined;
  children: React.ReactNode;
  style?: StyleProp<ViewStyle>;
};

export type CardProps = ViewProps & (SolidCardBaseProps | OutlineCardBaseProps);

export default class Card extends React.Component<CardProps> {
  static defaultProps: Partial<CardProps> = {
    contentInset: 'normal',
    roundness: 'small',
  };
  static contextTypes = ThemeContext;
  render() {
    const {
      type,
      color,
      elevation,
      contentInset,
      roundness,
      children,
      style,
      ...rootProps
    } = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'layout',
      `${type}Card`,
      `${color}${elevation ?? ''}`,
    );
    const themeStatic = getThemeFrom(
      this.context,
      defaultTheme,
      'layout',
      `${type}Card`,
      'static',
    );
    return (
      <View
        {...rootProps}
        style={[
          theme.part('container'),
          themeStatic.part('roundness', roundness),
          style,
        ]}>
        <View
          style={[
            contentInset && themeStatic.part('contentInset', contentInset),
          ]}>
          {children}
        </View>
      </View>
    );
  }
}
