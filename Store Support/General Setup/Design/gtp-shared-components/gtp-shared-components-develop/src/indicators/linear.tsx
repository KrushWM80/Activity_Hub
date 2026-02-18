import * as React from 'react';
import {View, ViewProps} from 'react-native';

import {getThemeFrom, ThemeContext} from '../theme/theme-provider';

import {composed as defaultTheme} from './theme';

export type LinearProgressIndicatorProps = ViewProps & {
  /** Color for the foreground of the indicator */
  color?: string;
  /** Whether to use the `small` variant */
  small?: boolean;
  /** Current value, 0-100 */
  value: number;
};

/**
 * @deprecated use <strong><ProgressIndicator /></strong> instead
 */
export default class LinearProgressIndicator extends React.Component<LinearProgressIndicatorProps> {
  static contextTypes = ThemeContext;

  render() {
    const {color, small, style, value, ...rootProps} = this.props;

    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'indicator',
      'linear',
      small ? 'small' : 'default',
    );

    return (
      <View {...rootProps} style={[theme.part('container'), style]}>
        <View
          style={[
            theme.part('indicator'),
            {width: `${Math.max(0, Math.min(value, 100))}%`},
            color && {
              backgroundColor: color,
            },
          ]}
        />
      </View>
    );
  }
}
