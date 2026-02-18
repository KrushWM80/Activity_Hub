import * as React from 'react';
import {TouchableOpacity, View, ViewProps, ViewStyle} from 'react-native';

import {Body} from '../next/components/Body';
import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import {composed as defaultTheme} from './theme';

export type TabExternalProps = {
  textStyle?: any;
  style?: ViewStyle;
  title: string;
};

export type TabProps = TabExternalProps &
  ViewProps & {
    onPress: (event: any) => void;
    selected: boolean;
    indicatorWidth?: number;
  };

export default class Tab extends React.Component<TabProps> {
  static contextTypes = ThemeContext;
  render() {
    const {title, style, indicatorWidth, textStyle, selected, ...rootProps} =
      this.props;

    const theme = getThemeFrom(this.context, defaultTheme, 'navigation', 'tab');
    const themeState = theme.extend(selected ? 'selected' : 'default');

    return (
      <TouchableOpacity
        style={[themeState.part('container'), style]}
        accessibilityRole="tab"
        accessibilityState={{selected}}
        {...rootProps}
        activeOpacity={1}>
        <Body
          numberOfLines={1}
          UNSAFE_style={[themeState.part('text'), textStyle]}>
          {title}
        </Body>
        <View
          style={[
            themeState.part('indicator'),
            indicatorWidth && {height: indicatorWidth},
          ]}
        />
      </TouchableOpacity>
    );
  }
}
