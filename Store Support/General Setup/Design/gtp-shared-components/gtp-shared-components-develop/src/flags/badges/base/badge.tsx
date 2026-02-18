import * as React from 'react';
import {View, ViewProps} from 'react-native';

import {Body} from '../../../next/components/Body';
import {getThemeFrom, ThemeContext} from '../../../theme/theme-provider';
import {composed as defaultTheme} from '../../theme';

type ExternalProps = ViewProps & {
  children: React.ReactNode;
};

export type BaseBadgeProps = ExternalProps & {
  type?: 'availability' | 'informational' | 'media' | 'count';
};

export default class BaseBadge extends React.Component<BaseBadgeProps> {
  static contextTypes = ThemeContext;

  render() {
    const {children, style, type, ...rootProps} = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'flags',
      'badges',
      type ?? 'default',
    );
    return (
      <View {...rootProps} style={[theme.part('container'), style]}>
        <Body UNSAFE_style={theme.part('text')}>{children}</Body>
      </View>
    );
  }
}
