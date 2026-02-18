import * as React from 'react';
import {Platform, Switch as ReactNativeSwitch, SwitchProps} from 'react-native';

import {getThemeFrom, ThemeContext} from '../../theme/theme-provider';
import {composed as defaultTheme} from '../theme';

export type ToggleProps = Omit<
  SwitchProps,
  'thumbColor' | 'trackColor' | 'ios_backgroundColor'
> & {
  /** Whether to use the `small` variant */
  small?: boolean;
};

export type ToggleExternalProps = ToggleProps;

export default class Toggle extends React.Component<ToggleProps> {
  static contextTypes = ThemeContext;
  render() {
    const {disabled, small, value, style, ...rootProps} = this.props;
    const props = {
      ...rootProps,
      disabled,
      value,
      trackColor: {
        true: 'white',
        false: 'white',
      },
      thumbColor: undefined,
      ios_backgroundColor: undefined,
    };

    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'form',
      `toggle${small ? 'Small' : ''}`,
      disabled ? 'disabled' : 'default',
    );

    props.trackColor = {
      true: theme.part('on.tintColor'),
      false: theme.part('off.tintColor'),
    };

    if (Platform.OS === 'android') {
      props.thumbColor = theme.part(value ? 'on' : 'off', 'thumbTintColor');
    } else {
      props.ios_backgroundColor = theme.part(
        value ? 'on' : 'off',
        'background',
      );
    }

    return (
      <ReactNativeSwitch {...props} style={[theme.part('container'), style]} />
    );
  }
}
