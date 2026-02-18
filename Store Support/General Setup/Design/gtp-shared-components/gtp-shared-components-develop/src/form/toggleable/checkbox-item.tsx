import * as React from 'react';
import {TouchableOpacity, View} from 'react-native';

import {Body} from '../../next/components/Body';
import {getThemeFrom, ThemeContext} from '../../theme/theme-provider';
import {composed as defaultTheme} from '../theme';

import Checkbox, {CheckboxExternalProps} from './checkbox';

export type CheckboxItemProps = CheckboxExternalProps & {
  label: string;
};

/**
 * @deprecated use Checkbox instead
 */
export default class CheckboxItem extends React.Component<CheckboxItemProps> {
  static contextTypes = ThemeContext;
  static defaultProps: Partial<CheckboxItemProps> = {
    accessible: true,
    accessibilityElementsHidden: true,
    accessibilityRole: 'checkbox',
  };

  private inputRef = React.createRef<View>();
  currentState = () => {
    if (this.props.value) {
      if (this.props.indeterminate) {
        if (this.props.disabled) {
          return 'indeterminateDisabled';
        }
        return 'indeterminate';
      }
      if (this.props.disabled) {
        return 'checkedDisabled';
      }
      return 'checked';
    }
    if (this.props.disabled) {
      return 'disabled';
    }
    return 'default';
  };
  private setValue = (value: boolean) => {
    this.props.onChange?.(value);
  };
  public focus = () => {
    this.inputRef.current?.focus();
  };
  render() {
    const {
      disabled,
      label,
      value,
      style,
      accessibilityRole,
      accessibilityLabel,
      accessibilityElementsHidden,
      accessible,
      testID,
      hitSlop,
      ...props
    } = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'form',
      'checkboxItem',
      this.currentState(),
    );
    return (
      <TouchableOpacity
        activeOpacity={1}
        {...{
          accessibilityLabel,
          accessibilityRole,
          accessible,
          hitSlop,
          testID,
        }}
        accessibilityState={{selected: value, disabled}}
        onPress={() => this.setValue(!value)}
        disabled={disabled}
        style={style}>
        <View
          style={theme.part('container')}
          accessibilityElementsHidden={accessibilityElementsHidden}>
          <Checkbox
            onChange={this.setValue}
            disabled={disabled}
            style={theme.part('checkbox')}
            {...props}
            value={value}
          />
          <Body UNSAFE_style={theme.part('label')}>{label}</Body>
        </View>
      </TouchableOpacity>
    );
  }
}
