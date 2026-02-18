import * as React from 'react';
import {View, ViewProps} from 'react-native';

import {Body} from '../../../next/components/Body';
import {getThemeFrom, ThemeContext} from '../../../theme/theme-provider';
import {composed as defaultTheme} from '../../theme';

export type MessageBaseExternalProps = ViewProps & {
  children: React.ReactNode;
  /** Icon component to display on this message */
  icon?: React.JSX.Element;
};

export type MessageBaseProps = MessageBaseExternalProps & {
  type?: 'info' | 'warning' | 'success' | 'error';
};

export default class MessageBase extends React.Component<MessageBaseProps> {
  static contextTypes = ThemeContext;

  render() {
    const {children, icon, type, ...rootProps} = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'messaging',
      'message',
      type ?? 'info',
    );
    return (
      <View {...rootProps} style={theme.part('container')}>
        <View style={theme.part('containerInner')}>
          {icon &&
            React.cloneElement(icon, {
              style: [theme.part('icon'), icon.props.style],
            })}
          <Body UNSAFE_style={theme.part('text')}>{children}</Body>
        </View>
      </View>
    );
  }
}
