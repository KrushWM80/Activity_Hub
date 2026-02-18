import * as React from 'react';
import {View, ViewProps} from 'react-native';

import {Body} from '../../../next/components/Body';
import {getThemeFrom, ThemeContext} from '../../../theme/theme-provider';
import {composed as defaultTheme} from '../../theme';

export type BaseFlagExternalProps = ViewProps & {
  children: React.ReactNode;
};

export type BaseFlagProps = BaseFlagExternalProps & {
  type?: 'rollback' | 'general' | 'filled';
};

export default class BaseFlag extends React.Component<BaseFlagProps> {
  static contextTypes = ThemeContext;

  render() {
    const {children, style, type, ...props} = this.props;
    const theme = getThemeFrom(this.context, defaultTheme, 'flags', 'flags');
    return (
      <View
        style={[theme.part(type ?? 'default', 'container'), style]}
        {...props}>
        <Body UNSAFE_style={theme.part(type ?? 'default', 'text')}>
          {children}
        </Body>
      </View>
    );
  }
}
