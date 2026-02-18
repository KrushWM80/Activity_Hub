import * as React from 'react';
import {View, ViewProps} from 'react-native';

import {Body} from '../next/components/Body';
import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import {composed as defaultTheme} from './theme';

export type SupportiveTextProps = ViewProps & {
  color?: string;
  icon: React.JSX.Element;
};

/**
 * @deprecated use StyledText instead
 */
export default class SupportiveText extends React.Component<SupportiveTextProps> {
  static contextTypes = ThemeContext;

  static displayName = 'SupportiveText';

  render() {
    const {color, icon, style, children, ...rootProps} = this.props;

    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'flags',
      'supportive',
      'default',
    );

    return (
      <View {...rootProps} style={[theme.part('container'), style]}>
        {React.cloneElement(icon, {color: color})}
        <Body numberOfLines={1} UNSAFE_style={[theme.part('text'), {color}]}>
          {children}
        </Body>
      </View>
    );
  }
}
