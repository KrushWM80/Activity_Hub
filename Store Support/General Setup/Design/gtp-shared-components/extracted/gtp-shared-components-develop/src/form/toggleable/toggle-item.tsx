import * as React from 'react';
import {TouchableOpacity, View} from 'react-native';

import {Body} from '../../next/components/Body';
import {getThemeFrom, ThemeContext} from '../../theme/theme-provider';
import {composed as defaultTheme} from '../theme';

import Toggle, {ToggleExternalProps} from './toggle';

export type ToggleItemProps = ToggleExternalProps & {
  children?: React.ReactNode;
};

/**
 * @deprecated use Switch instead
 */
export default class ToggleItem extends React.Component<ToggleItemProps> {
  static contextTypes = ThemeContext;
  static defaultProps: Partial<ToggleItemProps> = {
    accessibilityElementsHidden: true,
    accessibilityRole: 'checkbox',
  };

  private inputRef = React.createRef<View>();
  public focus = () => {
    this.inputRef.current?.focus();
  };
  render() {
    const {
      children,
      disabled,
      value,
      style,
      small,
      accessibilityElementsHidden,
      accessibilityLabel,
      accessibilityRole,
      accessible,
      ...props
    } = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'form',
      `toggleItem${small ? 'Small' : ''}`,
      disabled ? 'disabled' : 'default',
    );
    return (
      <TouchableOpacity
        activeOpacity={1}
        {...{
          accessibilityElementsHidden,
          accessibilityLabel,
          accessibilityRole,
          accessible,
        }}
        accessibilityState={{selected: value, disabled}}
        onPress={() => this.props.onValueChange?.(!this.props.value)}
        disabled={disabled}
        style={style}>
        <View style={theme.part('container')}>
          {!small && <Body UNSAFE_style={theme.part('label')}>{children}</Body>}
          <Toggle
            small={small}
            value={value}
            disabled={disabled}
            style={theme.part('toggle')}
            {...props}
          />
          {small && <Body UNSAFE_style={theme.part('label')}>{children}</Body>}
        </View>
      </TouchableOpacity>
    );
  }
}
