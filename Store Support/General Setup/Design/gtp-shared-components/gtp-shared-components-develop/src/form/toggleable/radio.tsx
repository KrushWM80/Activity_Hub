import * as React from 'react';
import {TouchableOpacity, View, ViewProps} from 'react-native';

import {getThemeFrom, ThemeContext} from '../../theme/theme-provider';
import {composed as defaultTheme} from '../theme';

export type RadioProps = ViewProps & {
  children?: never;
  /** Invoked with the new value when the value changes. */
  onChange?: (value: boolean) => void;
  /** If true the user won't be able to activate the radio button. Default value is false. */
  disabled?: boolean;
  /** The value of the checkbox. If true the radio button will be turned on. Default value is false. */
  value?: boolean;
};

export type RadioExternalProps = RadioProps;

/**
 * Radios represent a group of mutually exclusive choices, compared to Checkboxes that allow users to make one or more selections from a group. In use cases where only one selection of a group is allowed, use the `Radio` instead of the `Checkbox`.
 */
export default class Radio extends React.Component<RadioProps> {
  static contextTypes = ThemeContext;
  private inputRef = React.createRef<View>();
  currentState = () => {
    if (this.props.value) {
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
    const {disabled, value, style, ...props} = this.props;
    const theme = getThemeFrom(
      this.context,
      defaultTheme,
      'form',
      'radio',
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
          <View style={[theme.part('indicator')]} />
        </View>
      </TouchableOpacity>
    );
  }
}
