import * as React from 'react';
import {TouchableHighlight, View, ViewProps} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import {Body} from '../../../next/components/Body';
import {getThemeFrom, ThemeContext} from '../../../theme/theme-provider';
import {composed as defaultTheme} from '../../theme';

export type AlertExternalProps = ViewProps & {
  /** Icon component to display on this alert */
  icon?: React.JSX.Element;
  /** This alert's dismiss press event handler */
  onDismiss: () => void;
  children: React.ReactNode;
};

type AlertProps = AlertExternalProps & {
  type?: 'info' | 'info2' | 'info3' | 'error';
};

export default class BaseAlert extends React.Component<AlertProps> {
  static contextTypes = ThemeContext;
  render() {
    const {icon, children, type, onDismiss, ...rootProps} = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'messaging',
      'alert',
      type ?? 'default',
    );
    return (
      <View {...rootProps} style={theme.part('container')}>
        {icon &&
          React.cloneElement(icon, {
            style: [theme.part('icon'), icon.props.style],
          })}
        <Body UNSAFE_style={theme.part('text')}>{children}</Body>
        <TouchableHighlight
          underlayColor={theme.part('underlayColor')}
          accessibilityLabel="Dismiss Alert"
          accessibilityRole={
            !process.env.STYLEGUIDIST_ENV ? 'button' : undefined
          }
          style={theme.part('closeContainer')}
          onPress={onDismiss}>
          <Icons.CloseIcon UNSAFE_style={theme.part('close')} />
        </TouchableHighlight>
      </View>
    );
  }
}
