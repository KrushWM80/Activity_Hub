import * as React from 'react';
import {TouchableOpacity, View, ViewProps} from 'react-native';

import {Icons} from '@walmart/gtp-shared-icons';

import {
  getThemeFrom,
  ThemeContext,
  ThemeObject,
} from '../../theme/theme-provider';
import {composed as defaultTheme} from '../theme';

export type CheckboxProps = Omit<ViewProps, 'children'> & {
  /** Whether this checkbox is indeterminate (has checked and unchecked children) */
  indeterminate?: boolean;
  children?: never;
  /** Invoked with the new value when the value changes. */
  onChange?: (value: boolean) => void;
  /** If true the user won't be able to toggle the checkbox. Default value is false. */
  disabled?: boolean;
  /** The value of the checkbox. If true the checkbox will be turned on. Default value is false. */
  value?: boolean;
};

export type CheckboxExternalProps = CheckboxProps;

/**
 * Checkboxes are used for a list of options where the user may select multiple options, including all or none.
 */
export default class Checkbox extends React.Component<CheckboxProps> {
  static contextTypes = ThemeContext;

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
  icon = (iconSize: 16 | 24 | 32, theme: ThemeObject) => {
    if (this.props.value) {
      if (this.props.indeterminate) {
        return (
          <Icons.MinusIcon size={iconSize} UNSAFE_style={theme.part('icon')} />
        );
      }
      return (
        <Icons.CheckIcon size={iconSize} UNSAFE_style={theme.part('icon')} />
      );
    }
    return null;
  };
  private setValue = (value: boolean) => {
    this.props.onChange?.(value);
  };
  public focus = () => {
    this.inputRef.current?.focus();
  };
  render() {
    const {disabled, value, indeterminate, style, ...props} = this.props;
    const iconSize = getThemeFrom(
      this.context,
      defaultTheme,
      'form',
      'checkbox',
    ).part('static.iconSize');
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'form',
      'checkbox',
      this.currentState(),
    );
    return (
      <TouchableOpacity
        activeOpacity={1}
        onPress={() => this.setValue(!value)}
        {...props}
        disabled={disabled}
        style={style}>
        <View style={[theme.part('container')]}>
          {this.icon(iconSize, theme)}
        </View>
      </TouchableOpacity>
    );
  }
}
