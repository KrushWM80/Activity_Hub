import * as React from 'react';
import {View, ViewProps} from 'react-native';

import {Body} from '../../../next/components/Body';
import {capitalize} from '../../../next/utils';
import {getThemeFrom, ThemeContext} from '../../../theme/theme-provider';
import {composed as defaultTheme} from '../../theme';

export type TagBaseExternalProps = ViewProps & {
  children: React.ReactNode;
  /** Variant color -- the default color is blue. */
  color?: 'red' | 'spark' | 'green' | 'purple' | 'gray';
  /**
   * Leading icon serves for aesthetic purposes.
   */
  leadingIcon?: React.ReactElement;
};

export type TagBaseProps = TagBaseExternalProps & {
  type: 'primary' | 'secondary' | 'tertiary';
};

export default class TabBase extends React.Component<TagBaseProps> {
  static contextTypes = ThemeContext;

  render() {
    const {children, style, leadingIcon, type, color, ...rootProps} =
      this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'flags',
      'tags',
      `${type}${capitalize(color ?? '')}`,
    );
    const {color: iconColor, size: iconSize, ...iconStyle} = theme.part('icon');
    return (
      <View {...rootProps} style={[theme.part('container'), style]}>
        {leadingIcon
          ? React.cloneElement(leadingIcon, {
              color: iconColor,
              size: iconSize,
              UNSAFE_style: iconStyle,
            })
          : null}
        <Body UNSAFE_style={theme.part('text')}>{children}</Body>
      </View>
    );
  }
}
